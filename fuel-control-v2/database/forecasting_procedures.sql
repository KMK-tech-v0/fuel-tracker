-- =============================================
-- Forecasting Stored Procedures and Views
-- Advanced Fuel Consumption Forecasting System
-- =============================================

USE FuelControlV2;
GO

-- =============================================
-- VIEWS FOR REPORTING AND CALCULATIONS
-- =============================================

-- Equipment Consumption Summary View
CREATE VIEW vw_EquipmentConsumptionSummary AS
SELECT 
    e.equipment_id,
    e.equipment_name,
    e.equipment_code,
    s.site_name,
    ft.fuel_name,
    e.consumption_rate,
    ISNULL(AVG(oh.running_hours), 0) as avg_daily_hours,
    ISNULL(SUM(oh.running_hours), 0) as total_hours_30days,
    e.consumption_rate * ISNULL(AVG(oh.running_hours), 0) as estimated_daily_consumption,
    COUNT(oh.log_id) as days_logged
FROM Equipment e
JOIN Sites s ON e.site_id = s.site_id
JOIN FuelTypes ft ON e.fuel_type_id = ft.fuel_type_id
LEFT JOIN OperationalHoursLog oh ON e.equipment_id = oh.equipment_id 
    AND oh.log_date >= DATEADD(day, -30, GETDATE())
WHERE e.is_active = 1
GROUP BY e.equipment_id, e.equipment_name, e.equipment_code, s.site_name, 
         ft.fuel_name, e.consumption_rate;
GO

-- Site Consumption Summary View
CREATE VIEW vw_SiteConsumptionSummary AS
SELECT 
    s.site_id,
    s.site_name,
    s.site_code,
    ft.fuel_type_id,
    ft.fuel_name,
    fs.current_quantity,
    fs.minimum_threshold,
    fs.reorder_point,
    SUM(e.consumption_rate * ISNULL(oh_avg.avg_hours, 0)) as estimated_daily_consumption,
    COUNT(DISTINCT e.equipment_id) as active_equipment_count,
    CASE 
        WHEN SUM(e.consumption_rate * ISNULL(oh_avg.avg_hours, 0)) > 0 
        THEN fs.current_quantity / SUM(e.consumption_rate * ISNULL(oh_avg.avg_hours, 0))
        ELSE 999 
    END as days_remaining_estimate
FROM Sites s
JOIN FuelStock fs ON s.site_id = fs.site_id
JOIN FuelTypes ft ON fs.fuel_type_id = ft.fuel_type_id
LEFT JOIN Equipment e ON s.site_id = e.site_id AND ft.fuel_type_id = e.fuel_type_id AND e.is_active = 1
LEFT JOIN (
    SELECT equipment_id, AVG(running_hours) as avg_hours
    FROM OperationalHoursLog 
    WHERE log_date >= DATEADD(day, -30, GETDATE())
    GROUP BY equipment_id
) oh_avg ON e.equipment_id = oh_avg.equipment_id
WHERE s.is_active = 1
GROUP BY s.site_id, s.site_name, s.site_code, ft.fuel_type_id, ft.fuel_name,
         fs.current_quantity, fs.minimum_threshold, fs.reorder_point;
GO

-- Current Stock Status View
CREATE VIEW vw_CurrentStockStatus AS
SELECT 
    s.site_name,
    s.site_code,
    ft.fuel_name,
    fs.current_quantity,
    fs.available_quantity,
    fs.minimum_threshold,
    fs.maximum_capacity,
    fs.reorder_point,
    CASE 
        WHEN fs.current_quantity <= fs.minimum_threshold THEN 'Critical'
        WHEN fs.current_quantity <= fs.reorder_point THEN 'Low'
        WHEN fs.current_quantity >= fs.maximum_capacity * 0.9 THEN 'High'
        ELSE 'Normal'
    END as stock_status,
    (fs.current_quantity / fs.maximum_capacity) * 100 as fill_percentage,
    fs.last_updated
FROM Sites s
JOIN FuelStock fs ON s.site_id = fs.site_id
JOIN FuelTypes ft ON fs.fuel_type_id = ft.fuel_type_id
WHERE s.is_active = 1;
GO

-- =============================================
-- STORED PROCEDURES FOR FORECASTING
-- =============================================

-- Calculate Site Consumption Forecast
CREATE PROCEDURE sp_CalculateSiteForecast
    @site_id INT,
    @fuel_type_id INT,
    @forecast_date DATE = NULL,
    @safety_factor DECIMAL(5,3) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Set defaults
    IF @forecast_date IS NULL SET @forecast_date = CAST(GETDATE() AS DATE);
    IF @safety_factor IS NULL 
        SELECT @safety_factor = CAST(setting_value AS DECIMAL(5,3)) 
        FROM SystemSettings WHERE setting_key = 'default_safety_factor';
    
    DECLARE @current_balance DECIMAL(15,3);
    DECLARE @daily_consumption DECIMAL(12,3) = 0;
    DECLARE @days_remaining INT;
    DECLARE @next_refill_date DATE;
    DECLARE @recommended_quantity DECIMAL(15,3);
    DECLARE @confidence_level DECIMAL(5,2) = 85.0;
    
    -- Get current stock balance
    SELECT @current_balance = current_quantity
    FROM FuelStock 
    WHERE site_id = @site_id AND fuel_type_id = @fuel_type_id;
    
    -- Calculate daily consumption based on equipment and recent operational hours
    SELECT @daily_consumption = SUM(
        e.consumption_rate * ISNULL(oh_avg.avg_hours, 4.0) -- Default 4 hours if no data
    )
    FROM Equipment e
    LEFT JOIN (
        SELECT equipment_id, AVG(running_hours) as avg_hours
        FROM OperationalHoursLog 
        WHERE log_date >= DATEADD(day, -14, GETDATE()) -- Last 14 days average
        GROUP BY equipment_id
    ) oh_avg ON e.equipment_id = oh_avg.equipment_id
    WHERE e.site_id = @site_id 
      AND e.fuel_type_id = @fuel_type_id 
      AND e.is_active = 1;
    
    -- Apply safety factor
    SET @daily_consumption = @daily_consumption * @safety_factor;
    
    -- Calculate days remaining
    IF @daily_consumption > 0
        SET @days_remaining = FLOOR(@current_balance / @daily_consumption);
    ELSE
        SET @days_remaining = 999; -- Effectively unlimited
    
    -- Calculate next refill date estimate
    SET @next_refill_date = DATEADD(day, @days_remaining, @forecast_date);
    
    -- Calculate recommended order quantity (optimal order quantity from stock table)
    SELECT @recommended_quantity = optimal_order_quantity
    FROM FuelStock 
    WHERE site_id = @site_id AND fuel_type_id = @fuel_type_id;
    
    -- Adjust confidence based on data availability
    DECLARE @equipment_with_data INT;
    SELECT @equipment_with_data = COUNT(DISTINCT oh.equipment_id)
    FROM Equipment e
    JOIN OperationalHoursLog oh ON e.equipment_id = oh.equipment_id
    WHERE e.site_id = @site_id 
      AND e.fuel_type_id = @fuel_type_id 
      AND oh.log_date >= DATEADD(day, -14, GETDATE());
    
    DECLARE @total_equipment INT;
    SELECT @total_equipment = COUNT(*)
    FROM Equipment 
    WHERE site_id = @site_id AND fuel_type_id = @fuel_type_id AND is_active = 1;
    
    IF @total_equipment > 0
        SET @confidence_level = 50.0 + ((@equipment_with_data * 1.0 / @total_equipment) * 50.0);
    
    -- Insert or update forecast
    MERGE ConsumptionForecast AS target
    USING (SELECT @site_id as site_id, @fuel_type_id as fuel_type_id, @forecast_date as forecast_date) AS source
    ON target.site_id = source.site_id 
       AND target.fuel_type_id = source.fuel_type_id 
       AND target.forecast_date = source.forecast_date
    WHEN MATCHED THEN
        UPDATE SET
            current_balance = @current_balance,
            daily_consumption_rate = @daily_consumption,
            safety_factor = @safety_factor,
            forecast_days_remaining = @days_remaining,
            next_refill_date_estimate = @next_refill_date,
            recommended_order_quantity = @recommended_quantity,
            confidence_level = @confidence_level,
            calculation_method = 'Equipment-based with operational hours',
            last_calculated = GETDATE(),
            calculated_by = SYSTEM_USER
    WHEN NOT MATCHED THEN
        INSERT (site_id, fuel_type_id, forecast_date, current_balance, daily_consumption_rate,
                safety_factor, forecast_days_remaining, next_refill_date_estimate,
                recommended_order_quantity, confidence_level, calculation_method,
                last_calculated, calculated_by)
        VALUES (@site_id, @fuel_type_id, @forecast_date, @current_balance, @daily_consumption,
                @safety_factor, @days_remaining, @next_refill_date,
                @recommended_quantity, @confidence_level, 'Equipment-based with operational hours',
                GETDATE(), SYSTEM_USER);
    
    -- Return the forecast results
    SELECT 
        site_id,
        fuel_type_id,
        forecast_date,
        current_balance,
        daily_consumption_rate,
        safety_factor,
        forecast_days_remaining,
        next_refill_date_estimate,
        recommended_order_quantity,
        confidence_level,
        calculation_method,
        last_calculated
    FROM ConsumptionForecast
    WHERE site_id = @site_id 
      AND fuel_type_id = @fuel_type_id 
      AND forecast_date = @forecast_date;
END;
GO

-- Calculate All Site Forecasts
CREATE PROCEDURE sp_CalculateAllForecasts
    @forecast_date DATE = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    IF @forecast_date IS NULL SET @forecast_date = CAST(GETDATE() AS DATE);
    
    DECLARE @site_id INT, @fuel_type_id INT;
    
    -- Cursor to iterate through all active site-fuel combinations
    DECLARE forecast_cursor CURSOR FOR
    SELECT DISTINCT fs.site_id, fs.fuel_type_id
    FROM FuelStock fs
    JOIN Sites s ON fs.site_id = s.site_id
    WHERE s.is_active = 1;
    
    OPEN forecast_cursor;
    FETCH NEXT FROM forecast_cursor INTO @site_id, @fuel_type_id;
    
    WHILE @@FETCH_STATUS = 0
    BEGIN
        -- Calculate forecast for each site-fuel combination
        EXEC sp_CalculateSiteForecast @site_id, @fuel_type_id, @forecast_date;
        
        FETCH NEXT FROM forecast_cursor INTO @site_id, @fuel_type_id;
    END;
    
    CLOSE forecast_cursor;
    DEALLOCATE forecast_cursor;
    
    PRINT 'All forecasts calculated successfully for date: ' + CAST(@forecast_date AS VARCHAR(10));
END;
GO

-- Create Forecast Scenario
CREATE PROCEDURE sp_CreateForecastScenario
    @forecast_id INT,
    @scenario_name NVARCHAR(100),
    @adjusted_consumption_rate DECIMAL(12,3) = NULL,
    @adjusted_safety_factor DECIMAL(5,3) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @current_balance DECIMAL(15,3);
    DECLARE @original_consumption DECIMAL(12,3);
    DECLARE @original_safety_factor DECIMAL(5,3);
    DECLARE @scenario_consumption DECIMAL(12,3);
    DECLARE @scenario_days_remaining INT;
    DECLARE @scenario_refill_date DATE;
    DECLARE @scenario_order_quantity DECIMAL(15,3);
    
    -- Get original forecast data
    SELECT 
        @current_balance = current_balance,
        @original_consumption = daily_consumption_rate,
        @original_safety_factor = safety_factor,
        @scenario_order_quantity = recommended_order_quantity
    FROM ConsumptionForecast
    WHERE forecast_id = @forecast_id;
    
    -- Use adjusted values or original values
    SET @scenario_consumption = ISNULL(@adjusted_consumption_rate, @original_consumption);
    IF @adjusted_safety_factor IS NOT NULL
        SET @scenario_consumption = @scenario_consumption * @adjusted_safety_factor / @original_safety_factor;
    
    -- Calculate scenario results
    IF @scenario_consumption > 0
        SET @scenario_days_remaining = FLOOR(@current_balance / @scenario_consumption);
    ELSE
        SET @scenario_days_remaining = 999;
    
    SET @scenario_refill_date = DATEADD(day, @scenario_days_remaining, GETDATE());
    
    -- Insert scenario
    INSERT INTO ForecastScenarios (
        forecast_id, scenario_name, adjusted_consumption_rate, 
        adjusted_safety_factor, scenario_days_remaining, 
        scenario_refill_date, scenario_order_quantity
    )
    VALUES (
        @forecast_id, @scenario_name, @adjusted_consumption_rate,
        @adjusted_safety_factor, @scenario_days_remaining,
        @scenario_refill_date, @scenario_order_quantity
    );
    
    -- Return scenario results
    SELECT * FROM ForecastScenarios WHERE scenario_id = SCOPE_IDENTITY();
END;
GO

-- Check and Trigger Alerts
CREATE PROCEDURE sp_CheckForecastAlerts
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Check for forecast shortage alerts
    INSERT INTO AlertHistory (alert_id, alert_message, severity_level)
    SELECT 
        ac.alert_id,
        'Forecast shortage alert: ' + s.site_name + ' - ' + ft.fuel_name + 
        ' estimated to run out in ' + CAST(cf.forecast_days_remaining AS VARCHAR(10)) + ' days',
        CASE 
            WHEN cf.forecast_days_remaining <= 2 THEN 'Critical'
            WHEN cf.forecast_days_remaining <= 5 THEN 'High'
            WHEN cf.forecast_days_remaining <= ac.threshold_days THEN 'Medium'
            ELSE 'Low'
        END
    FROM AlertConfigurations ac
    JOIN Sites s ON ac.site_id = s.site_id
    JOIN FuelTypes ft ON ac.fuel_type_id = ft.fuel_type_id
    JOIN ConsumptionForecast cf ON s.site_id = cf.site_id AND ft.fuel_type_id = cf.fuel_type_id
    WHERE ac.alert_type = 'Forecast Shortage'
      AND ac.is_active = 1
      AND cf.forecast_days_remaining <= ac.threshold_days
      AND cf.forecast_date = CAST(GETDATE() AS DATE)
      AND NOT EXISTS (
          SELECT 1 FROM AlertHistory ah 
          WHERE ah.alert_id = ac.alert_id 
            AND CAST(ah.triggered_date AS DATE) = CAST(GETDATE() AS DATE)
      );
    
    -- Check for low stock alerts
    INSERT INTO AlertHistory (alert_id, alert_message, severity_level)
    SELECT 
        ac.alert_id,
        'Low stock alert: ' + s.site_name + ' - ' + ft.fuel_name + 
        ' current stock: ' + CAST(fs.current_quantity AS VARCHAR(20)) + ' liters',
        CASE 
            WHEN fs.current_quantity <= fs.minimum_threshold THEN 'Critical'
            WHEN fs.current_quantity <= ac.threshold_value THEN 'High'
            ELSE 'Medium'
        END
    FROM AlertConfigurations ac
    JOIN Sites s ON ac.site_id = s.site_id
    JOIN FuelTypes ft ON ac.fuel_type_id = ft.fuel_type_id
    JOIN FuelStock fs ON s.site_id = fs.site_id AND ft.fuel_type_id = fs.fuel_type_id
    WHERE ac.alert_type = 'Low Stock'
      AND ac.is_active = 1
      AND fs.current_quantity <= ac.threshold_value
      AND NOT EXISTS (
          SELECT 1 FROM AlertHistory ah 
          WHERE ah.alert_id = ac.alert_id 
            AND CAST(ah.triggered_date AS DATE) = CAST(GETDATE() AS DATE)
      );
    
    PRINT 'Alert check completed at: ' + CAST(GETDATE() AS VARCHAR(25));
END;
GO

-- Update Stock After Transaction
CREATE PROCEDURE sp_UpdateStockAfterTransaction
    @site_id INT,
    @fuel_type_id INT,
    @quantity_change DECIMAL(15,3), -- Positive for refill, negative for usage
    @transaction_type NVARCHAR(20) -- 'REFILL' or 'USAGE'
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRANSACTION;
    
    TRY
        -- Update stock quantity
        UPDATE FuelStock 
        SET current_quantity = current_quantity + @quantity_change,
            last_updated = GETDATE(),
            updated_by = SYSTEM_USER
        WHERE site_id = @site_id AND fuel_type_id = @fuel_type_id;
        
        -- Recalculate forecast after stock change
        EXEC sp_CalculateSiteForecast @site_id, @fuel_type_id;
        
        -- Check for alerts
        EXEC sp_CheckForecastAlerts;
        
        COMMIT TRANSACTION;
        
        PRINT 'Stock updated and forecast recalculated for Site ID: ' + CAST(@site_id AS VARCHAR(10));
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO

PRINT 'Forecasting procedures and views created successfully!';
GO
