-- =============================================
-- Sample Data for Advanced Fuel Consumption Forecasting System
-- =============================================

USE FuelControlV2;
GO

-- =============================================
-- FUEL TYPES
-- =============================================
INSERT INTO FuelTypes (fuel_name, fuel_code, density, energy_content, carbon_factor) VALUES
('Diesel', 'DSL', 0.832, 35.86, 2.68),
('Gasoline', 'GSL', 0.745, 32.18, 2.31),
('Jet A-1', 'JET', 0.775, 35.30, 2.52),
('Heavy Fuel Oil', 'HFO', 0.960, 40.50, 3.15),
('Biodiesel B20', 'BD20', 0.840, 33.50, 2.20),
('Natural Gas', 'NG', 0.717, 38.70, 1.87);

-- =============================================
-- SITES
-- =============================================
INSERT INTO Sites (site_name, site_code, site_type, location_address, contact_person, contact_phone, storage_capacity, safety_stock_days) VALUES
('Main Warehouse', 'WH001', 'Warehouse', '123 Industrial Zone, Yangon', 'John Manager', '+95-1-234567', 500000.00, 10),
('Construction Site Alpha', 'CS001', 'Site', 'Highway Project KM 45, Mandalay', 'Site Supervisor A', '+95-2-345678', 50000.00, 7),
('Construction Site Beta', 'CS002', 'Site', 'Bridge Project, Bago', 'Site Supervisor B', '+95-3-456789', 75000.00, 7),
('Mining Operation Gamma', 'MO001', 'Site', 'Copper Mine, Monywa', 'Mining Chief', '+95-4-567890', 100000.00, 14),
('Distribution Center North', 'DC001', 'Distribution Center', 'North Industrial Park, Mandalay', 'DC Manager', '+95-5-678901', 300000.00, 5),
('Power Plant Delta', 'PP001', 'Site', 'Thermal Power Station, Thanlyin', 'Plant Engineer', '+95-6-789012', 200000.00, 21);

-- =============================================
-- SUPPLIERS
-- =============================================
INSERT INTO Suppliers (supplier_name, supplier_code, contact_person, phone, email, payment_terms, lead_time_days, minimum_order_quantity, is_preferred, rating) VALUES
('Myanmar Petroleum Corporation', 'MPC001', 'Sales Manager', '+95-1-111111', 'sales@mpc.com.mm', 'Net 30', 2, 10000.00, 1, 4.5),
('Asia Fuel Trading', 'AFT001', 'Account Manager', '+95-1-222222', 'orders@asiafuel.com', 'Net 15', 3, 5000.00, 1, 4.2),
('Global Energy Solutions', 'GES001', 'Regional Director', '+95-1-333333', 'myanmar@globalenergy.com', 'Net 45', 5, 20000.00, 0, 3.8),
('Local Fuel Depot', 'LFD001', 'Owner', '+95-1-444444', 'info@localfuel.mm', 'COD', 1, 1000.00, 0, 4.0),
('Premium Oil Company', 'POC001', 'Business Development', '+95-1-555555', 'bd@premiumoil.com', 'Net 30', 4, 15000.00, 1, 4.7);

-- =============================================
-- EQUIPMENT
-- =============================================
INSERT INTO Equipment (site_id, equipment_name, equipment_code, fuel_type_id, consumption_rate, equipment_type, manufacturer, model) VALUES
-- Main Warehouse Equipment
(1, 'Forklift Unit 1', 'FL001', 1, 3.5, 'Forklift', 'Toyota', 'FD25'),
(1, 'Backup Generator', 'GEN001', 1, 12.0, 'Generator', 'Caterpillar', 'C9'),
(1, 'Delivery Truck 1', 'TRK001', 1, 8.5, 'Vehicle', 'Isuzu', 'NPR75'),

-- Construction Site Alpha Equipment
(2, 'Excavator Alpha 1', 'EX001', 1, 18.5, 'Excavator', 'Komatsu', 'PC200'),
(2, 'Bulldozer Alpha 1', 'BD001', 1, 22.0, 'Bulldozer', 'Caterpillar', 'D6T'),
(2, 'Generator Alpha 1', 'GEN002', 1, 15.0, 'Generator', 'Cummins', 'C250'),
(2, 'Concrete Mixer 1', 'CM001', 1, 6.5, 'Concrete Mixer', 'Volvo', 'FM400'),

-- Construction Site Beta Equipment
(3, 'Excavator Beta 1', 'EX002', 1, 19.2, 'Excavator', 'Hitachi', 'ZX200'),
(3, 'Crane Beta 1', 'CR001', 1, 25.0, 'Crane', 'Liebherr', 'LTM1070'),
(3, 'Generator Beta 1', 'GEN003', 1, 18.0, 'Generator', 'Perkins', 'P275'),

-- Mining Operation Gamma Equipment
(4, 'Mining Truck 1', 'MT001', 1, 45.0, 'Mining Truck', 'Caterpillar', '777D'),
(4, 'Mining Truck 2', 'MT002', 1, 47.5, 'Mining Truck', 'Komatsu', 'HD785'),
(4, 'Excavator Gamma 1', 'EX003', 1, 35.0, 'Excavator', 'Caterpillar', '390F'),
(4, 'Generator Gamma 1', 'GEN004', 1, 30.0, 'Generator', 'Caterpillar', 'C15'),

-- Power Plant Delta Equipment
(6, 'Main Generator 1', 'PG001', 4, 180.0, 'Power Generator', 'GE', 'LM6000'),
(6, 'Main Generator 2', 'PG002', 4, 185.0, 'Power Generator', 'Siemens', 'SGT-800'),
(6, 'Auxiliary Generator', 'AG001', 1, 25.0, 'Auxiliary Generator', 'Caterpillar', 'C18');

-- =============================================
-- FUEL STOCK
-- =============================================
INSERT INTO FuelStock (site_id, fuel_type_id, current_quantity, minimum_threshold, maximum_capacity, reorder_point, optimal_order_quantity) VALUES
-- Main Warehouse
(1, 1, 350000.00, 50000.00, 500000.00, 100000.00, 150000.00), -- Diesel
(1, 2, 80000.00, 10000.00, 100000.00, 20000.00, 30000.00),    -- Gasoline

-- Construction Site Alpha
(2, 1, 25000.00, 5000.00, 50000.00, 10000.00, 20000.00),      -- Diesel

-- Construction Site Beta
(3, 1, 40000.00, 7500.00, 75000.00, 15000.00, 25000.00),      -- Diesel

-- Mining Operation Gamma
(4, 1, 65000.00, 15000.00, 100000.00, 25000.00, 40000.00),    -- Diesel

-- Distribution Center North
(5, 1, 180000.00, 30000.00, 300000.00, 60000.00, 100000.00),  -- Diesel
(5, 2, 45000.00, 8000.00, 80000.00, 15000.00, 25000.00),      -- Gasoline

-- Power Plant Delta
(6, 4, 120000.00, 25000.00, 200000.00, 50000.00, 75000.00);   -- Heavy Fuel Oil

-- =============================================
-- FUEL PRICES
-- =============================================
INSERT INTO FuelPrices (fuel_type_id, supplier_id, price_per_liter, effective_date, price_type, volume_discount_threshold, volume_discount_rate) VALUES
-- Current Diesel Prices
(1, 1, 1850.00, '2025-01-01', 'Purchase', 50000.00, 0.05),  -- MPC Diesel
(1, 2, 1820.00, '2025-01-01', 'Purchase', 30000.00, 0.03),  -- AFT Diesel
(1, 5, 1800.00, '2025-01-01', 'Purchase', 100000.00, 0.08), -- POC Diesel

-- Current Gasoline Prices
(2, 1, 1950.00, '2025-01-01', 'Purchase', 20000.00, 0.04),  -- MPC Gasoline
(2, 2, 1920.00, '2025-01-01', 'Purchase', 15000.00, 0.03),  -- AFT Gasoline

-- Heavy Fuel Oil Prices
(4, 1, 1650.00, '2025-01-01', 'Purchase', 100000.00, 0.10), -- MPC HFO
(4, 3, 1680.00, '2025-01-01', 'Purchase', 75000.00, 0.08);  -- GES HFO

-- =============================================
-- OPERATIONAL HOURS LOG (Sample Data)
-- =============================================
INSERT INTO OperationalHoursLog (site_id, equipment_id, log_date, running_hours, recorded_by) VALUES
-- Recent operational hours for various equipment
(2, 4, '2025-01-01', 8.5, 'Site Supervisor A'),  -- Excavator Alpha 1
(2, 5, '2025-01-01', 7.0, 'Site Supervisor A'),  -- Bulldozer Alpha 1
(2, 6, '2025-01-01', 10.0, 'Site Supervisor A'), -- Generator Alpha 1

(3, 8, '2025-01-01', 9.2, 'Site Supervisor B'),  -- Excavator Beta 1
(3, 9, '2025-01-01', 6.5, 'Site Supervisor B'),  -- Crane Beta 1
(3, 10, '2025-01-01', 12.0, 'Site Supervisor B'), -- Generator Beta 1

(4, 11, '2025-01-01', 12.0, 'Mining Chief'),     -- Mining Truck 1
(4, 12, '2025-01-01', 11.5, 'Mining Chief'),     -- Mining Truck 2
(4, 13, '2025-01-01', 10.0, 'Mining Chief'),     -- Excavator Gamma 1

(6, 15, '2025-01-01', 24.0, 'Plant Engineer'),   -- Main Generator 1
(6, 16, '2025-01-01', 20.0, 'Plant Engineer'),   -- Main Generator 2
(6, 17, '2025-01-01', 8.0, 'Plant Engineer');    -- Auxiliary Generator

-- =============================================
-- ALERT CONFIGURATIONS
-- =============================================
INSERT INTO AlertConfigurations (alert_name, alert_type, site_id, fuel_type_id, threshold_value, threshold_days, notification_emails) VALUES
('Main Warehouse Low Diesel Stock', 'Low Stock', 1, 1, 75000.00, NULL, 'manager@company.com,logistics@company.com'),
('Construction Alpha Forecast Shortage', 'Forecast Shortage', 2, 1, NULL, 5, 'supervisor.alpha@company.com,manager@company.com'),
('Mining Operation Critical Stock', 'Low Stock', 4, 1, 20000.00, NULL, 'mining.chief@company.com,manager@company.com'),
('Power Plant Fuel Shortage Warning', 'Forecast Shortage', 6, 4, NULL, 7, 'plant.engineer@company.com,operations@company.com');

-- =============================================
-- SYSTEM SETTINGS
-- =============================================
INSERT INTO SystemSettings (setting_key, setting_value, setting_description, data_type) VALUES
('default_safety_factor', '1.2', 'Default safety factor for consumption forecasting', 'decimal'),
('forecast_calculation_frequency', '24', 'Hours between automatic forecast calculations', 'integer'),
('low_stock_alert_threshold', '0.2', 'Percentage of maximum capacity to trigger low stock alerts', 'decimal'),
('email_notification_enabled', 'true', 'Enable email notifications for alerts', 'boolean'),
('default_currency', 'MMK', 'Default currency for pricing', 'string'),
('maintenance_reminder_days', '30', 'Days before maintenance due to send reminder', 'integer'),
('consumption_variance_threshold', '0.15', 'Acceptable variance in consumption before flagging anomaly', 'decimal'),
('forecast_confidence_minimum', '0.75', 'Minimum confidence level required for forecasts', 'decimal');

-- =============================================
-- SAMPLE REFILL TRANSACTIONS
-- =============================================
INSERT INTO RefillTransactions (transaction_id, site_id, fuel_type_id, supplier_id, quantity, unit_cost, total_cost, refill_date, created_by) VALUES
('REF-2025-001', 1, 1, 1, 100000.00, 1850.00, 185000000.00, '2025-01-01 08:00:00', 'System'),
('REF-2025-002', 2, 1, 2, 25000.00, 1820.00, 45500000.00, '2025-01-01 10:30:00', 'Site Supervisor A'),
('REF-2025-003', 4, 1, 1, 50000.00, 1800.00, 90000000.00, '2025-01-01 14:00:00', 'Mining Chief'),
('REF-2025-004', 6, 4, 1, 75000.00, 1650.00, 123750000.00, '2025-01-01 16:00:00', 'Plant Engineer');

-- =============================================
-- SAMPLE USAGE TRANSACTIONS
-- =============================================
INSERT INTO UsageTransactions (transaction_id, site_id, fuel_type_id, equipment_id, department, quantity, usage_date, purpose, created_by) VALUES
('USE-2025-001', 2, 1, 4, 'Construction', 157.25, '2025-01-01 18:00:00', 'Excavation work', 'Site Supervisor A'),
('USE-2025-002', 2, 1, 5, 'Construction', 154.00, '2025-01-01 18:00:00', 'Land clearing', 'Site Supervisor A'),
('USE-2025-003', 3, 1, 8, 'Construction', 176.64, '2025-01-01 18:00:00', 'Foundation work', 'Site Supervisor B'),
('USE-2025-004', 4, 1, 11, 'Mining', 540.00, '2025-01-01 18:00:00', 'Material transport', 'Mining Chief'),
('USE-2025-005', 6, 4, 15, 'Power Generation', 4320.00, '2025-01-01 18:00:00', 'Electricity generation', 'Plant Engineer');

PRINT 'Sample data inserted successfully!';
GO
