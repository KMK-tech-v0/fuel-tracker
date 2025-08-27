-- =============================================
-- Advanced Fuel Consumption Forecasting System Database
-- Version 2.0 - Enhanced with Forecasting Capabilities
-- =============================================

USE master;
GO

-- Drop database if exists
IF EXISTS (SELECT name FROM sys.databases WHERE name = 'FuelControlV2')
BEGIN
    ALTER DATABASE FuelControlV2 SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE FuelControlV2;
END
GO

-- Create new database
CREATE DATABASE FuelControlV2;
GO

USE FuelControlV2;
GO

-- =============================================
-- CORE TABLES
-- =============================================

-- Fuel Types Table
CREATE TABLE FuelTypes (
    fuel_type_id INT IDENTITY(1,1) PRIMARY KEY,
    fuel_name NVARCHAR(100) NOT NULL UNIQUE,
    fuel_code NVARCHAR(20) NOT NULL UNIQUE,
    density DECIMAL(5,3) DEFAULT 0.850, -- kg/liter
    energy_content DECIMAL(8,2), -- MJ/liter
    carbon_factor DECIMAL(8,4), -- kg CO2/liter
    is_active BIT DEFAULT 1,
    created_date DATETIME2 DEFAULT GETDATE(),
    updated_date DATETIME2 DEFAULT GETDATE()
);

-- Sites Table (Enhanced)
CREATE TABLE Sites (
    site_id INT IDENTITY(1,1) PRIMARY KEY,
    site_name NVARCHAR(200) NOT NULL,
    site_code NVARCHAR(20) NOT NULL UNIQUE,
    site_type NVARCHAR(50) NOT NULL CHECK (site_type IN ('Site', 'Warehouse', 'Distribution Center')),
    location_address NVARCHAR(500),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    contact_person NVARCHAR(100),
    contact_phone NVARCHAR(20),
    contact_email NVARCHAR(100),
    storage_capacity DECIMAL(15,2), -- Total storage capacity in liters
    safety_stock_days INT DEFAULT 7, -- Days of safety stock to maintain
    is_active BIT DEFAULT 1,
    created_date DATETIME2 DEFAULT GETDATE(),
    updated_date DATETIME2 DEFAULT GETDATE()
);

-- Suppliers Table (Enhanced)
CREATE TABLE Suppliers (
    supplier_id INT IDENTITY(1,1) PRIMARY KEY,
    supplier_name NVARCHAR(200) NOT NULL,
    supplier_code NVARCHAR(20) NOT NULL UNIQUE,
    contact_person NVARCHAR(100),
    phone NVARCHAR(20),
    email NVARCHAR(100),
    address NVARCHAR(500),
    payment_terms NVARCHAR(100),
    lead_time_days INT DEFAULT 3, -- Standard delivery lead time
    minimum_order_quantity DECIMAL(15,2) DEFAULT 0,
    is_preferred BIT DEFAULT 0,
    rating DECIMAL(3,2) CHECK (rating >= 0 AND rating <= 5), -- Supplier rating 0-5
    is_active BIT DEFAULT 1,
    created_date DATETIME2 DEFAULT GETDATE(),
    updated_date DATETIME2 DEFAULT GETDATE()
);

-- =============================================
-- EQUIPMENT AND CONSUMPTION TRACKING
-- =============================================

-- Equipment Table (NEW)
CREATE TABLE Equipment (
    equipment_id INT IDENTITY(1,1) PRIMARY KEY,
    site_id INT NOT NULL,
    equipment_name NVARCHAR(200) NOT NULL,
    equipment_code NVARCHAR(50) NOT NULL,
    fuel_type_id INT NOT NULL,
    consumption_rate DECIMAL(10,3) NOT NULL, -- liters per hour
    equipment_type NVARCHAR(100), -- Generator, Vehicle, Machinery, etc.
    manufacturer NVARCHAR(100),
    model NVARCHAR(100),
    serial_number NVARCHAR(100),
    installation_date DATE,
    last_maintenance_date DATE,
    next_maintenance_date DATE,
    efficiency_rating DECIMAL(5,2), -- Fuel efficiency rating
    is_active BIT DEFAULT 1,
    created_date DATETIME2 DEFAULT GETDATE(),
    updated_date DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (site_id) REFERENCES Sites(site_id),
    FOREIGN KEY (fuel_type_id) REFERENCES FuelTypes(fuel_type_id),
    UNIQUE (site_id, equipment_code)
);

-- Operational Hours Log (NEW)
CREATE TABLE OperationalHoursLog (
    log_id INT IDENTITY(1,1) PRIMARY KEY,
    site_id INT NOT NULL,
    equipment_id INT NOT NULL,
    log_date DATE NOT NULL,
    running_hours DECIMAL(8,2) NOT NULL,
    fuel_consumed DECIMAL(12,3), -- Actual fuel consumed (if available)
    recorded_by NVARCHAR(100),
    notes NVARCHAR(500),
    is_estimated BIT DEFAULT 0, -- Whether the hours are estimated
    created_date DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (site_id) REFERENCES Sites(site_id),
    FOREIGN KEY (equipment_id) REFERENCES Equipment(equipment_id),
    UNIQUE (site_id, equipment_id, log_date)
);

-- =============================================
-- INVENTORY AND STOCK MANAGEMENT
-- =============================================

-- Fuel Stock Table (Enhanced)
CREATE TABLE FuelStock (
    stock_id INT IDENTITY(1,1) PRIMARY KEY,
    site_id INT NOT NULL,
    fuel_type_id INT NOT NULL,
    current_quantity DECIMAL(15,3) NOT NULL DEFAULT 0,
    reserved_quantity DECIMAL(15,3) DEFAULT 0, -- Reserved for planned usage
    available_quantity AS (current_quantity - reserved_quantity) PERSISTED,
    minimum_threshold DECIMAL(15,3) NOT NULL DEFAULT 0,
    maximum_capacity DECIMAL(15,3) NOT NULL,
    reorder_point DECIMAL(15,3), -- Automatic reorder trigger point
    optimal_order_quantity DECIMAL(15,3), -- Economic order quantity
    last_updated DATETIME2 DEFAULT GETDATE(),
    updated_by NVARCHAR(100),
    FOREIGN KEY (site_id) REFERENCES Sites(site_id),
    FOREIGN KEY (fuel_type_id) REFERENCES FuelTypes(fuel_type_id),
    UNIQUE (site_id, fuel_type_id)
);

-- Fuel Prices Table (Enhanced)
CREATE TABLE FuelPrices (
    price_id INT IDENTITY(1,1) PRIMARY KEY,
    fuel_type_id INT NOT NULL,
    supplier_id INT,
    price_per_liter DECIMAL(10,4) NOT NULL,
    currency NVARCHAR(10) DEFAULT 'MMK',
    effective_date DATE NOT NULL,
    expiry_date DATE,
    price_type NVARCHAR(50) DEFAULT 'Purchase' CHECK (price_type IN ('Purchase', 'Market', 'Contract')),
    volume_discount_threshold DECIMAL(15,2), -- Minimum quantity for discount
    volume_discount_rate DECIMAL(5,4), -- Discount rate for bulk purchases
    is_active BIT DEFAULT 1,
    created_date DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (fuel_type_id) REFERENCES FuelTypes(fuel_type_id),
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
);

-- =============================================
-- FORECASTING AND PLANNING
-- =============================================

-- Consumption Forecast Table (NEW)
CREATE TABLE ConsumptionForecast (
    forecast_id INT IDENTITY(1,1) PRIMARY KEY,
    site_id INT NOT NULL,
    fuel_type_id INT NOT NULL,
    forecast_date DATE NOT NULL,
    current_balance DECIMAL(15,3) NOT NULL,
    daily_consumption_rate DECIMAL(12,3) NOT NULL,
    safety_factor DECIMAL(5,3) DEFAULT 1.2, -- Safety multiplier for consumption
    forecast_days_remaining INT,
    next_refill_date_estimate DATE,
    recommended_order_quantity DECIMAL(15,3),
    confidence_level DECIMAL(5,2), -- Forecast confidence percentage
    calculation_method NVARCHAR(100), -- Method used for calculation
    last_calculated DATETIME2 DEFAULT GETDATE(),
    calculated_by NVARCHAR(100),
    FOREIGN KEY (site_id) REFERENCES Sites(site_id),
    FOREIGN KEY (fuel_type_id) REFERENCES FuelTypes(fuel_type_id),
    UNIQUE (site_id, fuel_type_id, forecast_date)
);

-- Forecast Scenarios Table (NEW)
CREATE TABLE ForecastScenarios (
    scenario_id INT IDENTITY(1,1) PRIMARY KEY,
    forecast_id INT NOT NULL,
    scenario_name NVARCHAR(100) NOT NULL,
    adjusted_consumption_rate DECIMAL(12,3),
    adjusted_safety_factor DECIMAL(5,3),
    scenario_days_remaining INT,
    scenario_refill_date DATE,
    scenario_order_quantity DECIMAL(15,3),
    created_date DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (forecast_id) REFERENCES ConsumptionForecast(forecast_id)
);

-- =============================================
-- TRANSACTIONS AND HISTORY
-- =============================================

-- Refill Transactions (Enhanced)
CREATE TABLE RefillTransactions (
    refill_id INT IDENTITY(1,1) PRIMARY KEY,
    transaction_id NVARCHAR(50) NOT NULL UNIQUE,
    site_id INT NOT NULL,
    fuel_type_id INT NOT NULL,
    supplier_id INT,
    source_site_id INT, -- For inter-site transfers
    quantity DECIMAL(15,3) NOT NULL,
    unit_cost DECIMAL(10,4),
    transportation_cost DECIMAL(12,2) DEFAULT 0,
    loading_unloading_cost DECIMAL(12,2) DEFAULT 0,
    total_cost DECIMAL(15,2),
    refill_date DATETIME2 NOT NULL,
    delivery_date DATETIME2,
    invoice_number NVARCHAR(100),
    purchase_order_number NVARCHAR(100),
    quality_check_passed BIT DEFAULT 1,
    notes NVARCHAR(500),
    created_by NVARCHAR(100),
    created_date DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (site_id) REFERENCES Sites(site_id),
    FOREIGN KEY (fuel_type_id) REFERENCES FuelTypes(fuel_type_id),
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id),
    FOREIGN KEY (source_site_id) REFERENCES Sites(site_id)
);

-- Usage Transactions (Enhanced)
CREATE TABLE UsageTransactions (
    usage_id INT IDENTITY(1,1) PRIMARY KEY,
    transaction_id NVARCHAR(50) NOT NULL UNIQUE,
    site_id INT NOT NULL,
    fuel_type_id INT NOT NULL,
    equipment_id INT,
    department NVARCHAR(100),
    quantity DECIMAL(15,3) NOT NULL,
    usage_date DATETIME2 NOT NULL,
    purpose NVARCHAR(200),
    operator_name NVARCHAR(100),
    meter_reading_before DECIMAL(12,2),
    meter_reading_after DECIMAL(12,2),
    efficiency_rating DECIMAL(5,2), -- Actual vs expected consumption
    notes NVARCHAR(500),
    created_by NVARCHAR(100),
    created_date DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (site_id) REFERENCES Sites(site_id),
    FOREIGN KEY (fuel_type_id) REFERENCES FuelTypes(fuel_type_id),
    FOREIGN KEY (equipment_id) REFERENCES Equipment(equipment_id)
);

-- =============================================
-- ALERTS AND NOTIFICATIONS
-- =============================================

-- Alert Configurations (NEW)
CREATE TABLE AlertConfigurations (
    alert_id INT IDENTITY(1,1) PRIMARY KEY,
    alert_name NVARCHAR(100) NOT NULL,
    alert_type NVARCHAR(50) NOT NULL CHECK (alert_type IN ('Low Stock', 'Forecast Shortage', 'Equipment Efficiency', 'Maintenance Due', 'Price Change')),
    site_id INT,
    fuel_type_id INT,
    equipment_id INT,
    threshold_value DECIMAL(15,3),
    threshold_days INT,
    notification_emails NVARCHAR(1000), -- Comma-separated email list
    is_active BIT DEFAULT 1,
    created_date DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (site_id) REFERENCES Sites(site_id),
    FOREIGN KEY (fuel_type_id) REFERENCES FuelTypes(fuel_type_id),
    FOREIGN KEY (equipment_id) REFERENCES Equipment(equipment_id)
);

-- Alert History (NEW)
CREATE TABLE AlertHistory (
    alert_history_id INT IDENTITY(1,1) PRIMARY KEY,
    alert_id INT NOT NULL,
    alert_message NVARCHAR(500),
    severity_level NVARCHAR(20) CHECK (severity_level IN ('Low', 'Medium', 'High', 'Critical')),
    triggered_date DATETIME2 DEFAULT GETDATE(),
    acknowledged_date DATETIME2,
    acknowledged_by NVARCHAR(100),
    resolved_date DATETIME2,
    resolution_notes NVARCHAR(500),
    FOREIGN KEY (alert_id) REFERENCES AlertConfigurations(alert_id)
);

-- =============================================
-- AUDIT AND SYSTEM TABLES
-- =============================================

-- Audit Log (NEW)
CREATE TABLE AuditLog (
    audit_id INT IDENTITY(1,1) PRIMARY KEY,
    table_name NVARCHAR(100) NOT NULL,
    record_id INT NOT NULL,
    action_type NVARCHAR(20) NOT NULL CHECK (action_type IN ('INSERT', 'UPDATE', 'DELETE')),
    old_values NVARCHAR(MAX),
    new_values NVARCHAR(MAX),
    changed_by NVARCHAR(100),
    changed_date DATETIME2 DEFAULT GETDATE(),
    ip_address NVARCHAR(50),
    user_agent NVARCHAR(500)
);

-- System Settings (NEW)
CREATE TABLE SystemSettings (
    setting_id INT IDENTITY(1,1) PRIMARY KEY,
    setting_key NVARCHAR(100) NOT NULL UNIQUE,
    setting_value NVARCHAR(1000),
    setting_description NVARCHAR(500),
    data_type NVARCHAR(20) DEFAULT 'string',
    is_system BIT DEFAULT 0, -- System settings cannot be deleted
    updated_by NVARCHAR(100),
    updated_date DATETIME2 DEFAULT GETDATE()
);

-- =============================================
-- INDEXES FOR PERFORMANCE
-- =============================================

-- Equipment indexes
CREATE INDEX IX_Equipment_Site_FuelType ON Equipment(site_id, fuel_type_id);
CREATE INDEX IX_Equipment_Active ON Equipment(is_active) WHERE is_active = 1;

-- Operational Hours Log indexes
CREATE INDEX IX_OperationalHours_Site_Date ON OperationalHoursLog(site_id, log_date);
CREATE INDEX IX_OperationalHours_Equipment_Date ON OperationalHoursLog(equipment_id, log_date);

-- Forecast indexes
CREATE INDEX IX_Forecast_Site_FuelType_Date ON ConsumptionForecast(site_id, fuel_type_id, forecast_date);
CREATE INDEX IX_Forecast_RefillDate ON ConsumptionForecast(next_refill_date_estimate);

-- Transaction indexes
CREATE INDEX IX_RefillTransactions_Site_Date ON RefillTransactions(site_id, refill_date);
CREATE INDEX IX_UsageTransactions_Site_Date ON UsageTransactions(site_id, usage_date);
CREATE INDEX IX_UsageTransactions_Equipment_Date ON UsageTransactions(equipment_id, usage_date);

-- Stock indexes
CREATE INDEX IX_FuelStock_Site_FuelType ON FuelStock(site_id, fuel_type_id);
CREATE INDEX IX_FuelStock_CurrentQuantity ON FuelStock(current_quantity);
CREATE INDEX IX_FuelStock_ReorderPoint ON FuelStock(reorder_point);

PRINT 'Advanced Fuel Consumption Forecasting Database Created Successfully!';
GO
