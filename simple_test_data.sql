-- Simple Test Data for Carbon Emissions Platform
-- This creates realistic test data for 2023 and 2024

-- ============================================
-- 1. EMISSION FACTORS
-- ============================================

-- Natural Gas (2023 and 2024 versions)
INSERT INTO emission_factors (activity_name, scope, co2e_per_unit, activity_unit, valid_from, valid_to, source)
VALUES ('Natural Gas', 1, 2.03, 'cubic meters', '2023-01-01', '2023-12-31', 'EPA 2023');

INSERT INTO emission_factors (activity_name, scope, co2e_per_unit, activity_unit, valid_from, valid_to, source)
VALUES ('Natural Gas', 1, 2.05, 'cubic meters', '2024-01-01', NULL, 'EPA 2024');

-- Gasoline (2023 and 2024 versions)
INSERT INTO emission_factors (activity_name, scope, co2e_per_unit, activity_unit, valid_from, valid_to, source)
VALUES ('Gasoline', 1, 2.31, 'litres', '2023-01-01', '2023-12-31', 'DEFRA 2023');

INSERT INTO emission_factors (activity_name, scope, co2e_per_unit, activity_unit, valid_from, valid_to, source)
VALUES ('Gasoline', 1, 2.33, 'litres', '2024-01-01', NULL, 'DEFRA 2024');

-- Grid Electricity (2023 and 2024 versions)
INSERT INTO emission_factors (activity_name, scope, co2e_per_unit, activity_unit, valid_from, valid_to, source)
VALUES ('Grid Electricity', 2, 0.45, 'kWh', '2023-01-01', '2023-12-31', 'National Grid 2023');

INSERT INTO emission_factors (activity_name, scope, co2e_per_unit, activity_unit, valid_from, valid_to, source)
VALUES ('Grid Electricity', 2, 0.42, 'kWh', '2024-01-01', NULL, 'National Grid 2024');

-- Scope 3 factors
INSERT INTO emission_factors (activity_name, scope, co2e_per_unit, activity_unit, valid_from, valid_to, source)
VALUES ('Business Travel - Air', 3, 0.25, 'km', '2023-01-01', NULL, 'DEFRA 2023');

INSERT INTO emission_factors (activity_name, scope, co2e_per_unit, activity_unit, valid_from, valid_to, source)
VALUES ('Employee Commute', 3, 0.17, 'km', '2023-01-01', NULL, 'EPA 2023');

INSERT INTO emission_factors (activity_name, scope, co2e_per_unit, activity_unit, valid_from, valid_to, source)
VALUES ('Waste Disposal', 3, 0.52, 'kg', '2023-01-01', NULL, 'EPA 2023');

-- ============================================
-- 2. EMISSION RECORDS FOR 2023
-- ============================================

-- Q1 2023 - Diesel (using existing factor_id 1)
INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2023-01-15', 'Diesel', 500, 'litres', 500 * 2.73, 1, 'Factory A', 'Operations', 'January diesel';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2023-02-15', 'Diesel', 480, 'litres', 480 * 2.73, 1, 'Factory A', 'Operations', 'February diesel';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2023-03-15', 'Diesel', 520, 'litres', 520 * 2.73, 1, 'Factory A', 'Operations', 'March diesel';

-- Q1 2023 - Natural Gas
INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2023-01-20', 'Natural Gas', 1000, 'cubic meters', 1000 * 2.03, 1, 'Factory A', 'Operations', 'January heating'
FROM emission_factors WHERE activity_name = 'Natural Gas' AND valid_from = '2023-01-01';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2023-02-20', 'Natural Gas', 950, 'cubic meters', 950 * 2.03, 1, 'Factory A', 'Operations', 'February heating'
FROM emission_factors WHERE activity_name = 'Natural Gas' AND valid_from = '2023-01-01';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, 'Factory A', department, notes)
SELECT factor_id, '2023-03-20', 'Natural Gas', 900, 'cubic meters', 900 * 2.03, 1, 'Factory A', 'Operations', 'March heating'
FROM emission_factors WHERE activity_name = 'Natural Gas' AND valid_from = '2023-01-01';

-- Q1 2023 - Gasoline
INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2023-01-25', 'Gasoline', 300, 'litres', 300 * 2.31, 1, 'Fleet', 'Logistics', 'January fleet fuel'
FROM emission_factors WHERE activity_name = 'Gasoline' AND valid_from = '2023-01-01';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2023-02-25', 'Gasoline', 280, 'litres', 280 * 2.31, 1, 'Fleet', 'Logistics', 'February fleet fuel'
FROM emission_factors WHERE activity_name = 'Gasoline' AND valid_from = '2023-01-01';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2023-03-25', 'Gasoline', 320, 'litres', 320 * 2.31, 1, 'Fleet', 'Logistics', 'March fleet fuel'
FROM emission_factors WHERE activity_name = 'Gasoline' AND valid_from = '2023-01-01';

-- Q1 2023 - Grid Electricity (Scope 2)
INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2023-01-10', 'Grid Electricity', 5000, 'kWh', 5000 * 0.45, 2, 'Factory A', 'Operations', 'January electricity'
FROM emission_factors WHERE activity_name = 'Grid Electricity' AND valid_from = '2023-01-01';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2023-02-10', 'Grid Electricity', 4800, 'kWh', 4800 * 0.45, 2, 'Factory A', 'Operations', 'February electricity'
FROM emission_factors WHERE activity_name = 'Grid Electricity' AND valid_from = '2023-01-01';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2023-03-10', 'Grid Electricity', 5200, 'kWh', 5200 * 0.45, 2, 'Factory A', 'Operations', 'March electricity'
FROM emission_factors WHERE activity_name = 'Grid Electricity' AND valid_from = '2023-01-01';

-- Q1 2023 - Scope 3 emissions
INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2023-01-30', 'Business Travel - Air', 2000, 'km', 2000 * 0.25, 3, 'HQ', 'Sales', 'Client meetings'
FROM emission_factors WHERE activity_name = 'Business Travel - Air';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2023-02-15', 'Employee Commute', 3000, 'km', 3000 * 0.17, 3, 'HQ', 'All', 'Commute tracking'
FROM emission_factors WHERE activity_name = 'Employee Commute';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2023-03-20', 'Waste Disposal', 500, 'kg', 500 * 0.52, 3, 'Factory A', 'Operations', 'Monthly waste'
FROM emission_factors WHERE activity_name = 'Waste Disposal';

-- Q2-Q4 2023 (Additional months)
INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2023-04-15', 'Diesel', 510, 'litres', 510 * 2.73, 1, 'Factory A', 'Operations', 'April diesel';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2023-05-15', 'Diesel', 490, 'litres', 490 * 2.73, 1, 'Factory A', 'Operations', 'May diesel';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2023-06-15', 'Diesel', 505, 'litres', 505 * 2.73, 1, 'Factory A', 'Operations', 'June diesel';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2023-07-15', 'Diesel', 530, 'litres', 530 * 2.73, 1, 'Factory A', 'Operations', 'July diesel';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2023-08-15', 'Diesel', 540, 'litres', 540 * 2.73, 1, 'Factory A', 'Operations', 'August diesel';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2023-09-15', 'Diesel', 525, 'litres', 525 * 2.73, 1, 'Factory A', 'Operations', 'September diesel';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2023-10-15', 'Diesel', 515, 'litres', 515 * 2.73, 1, 'Factory A', 'Operations', 'October diesel';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2023-11-15', 'Diesel', 520, 'litres', 520 * 2.73, 1, 'Factory A', 'Operations', 'November diesel';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2023-12-15', 'Diesel', 510, 'litres', 510 * 2.73, 1, 'Factory A', 'Operations', 'December diesel';

-- ============================================
-- 3. EMISSION RECORDS FOR 2024 (Lower emissions)
-- ============================================

-- Q1 2024 - Diesel (showing improvement)
INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2024-01-15', 'Diesel', 450, 'litres', 450 * 2.73, 1, 'Factory A', 'Operations', 'January diesel - reduced';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2024-02-15', 'Diesel', 430, 'litres', 430 * 2.73, 1, 'Factory A', 'Operations', 'February diesel - reduced';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2024-03-15', 'Diesel', 440, 'litres', 440 * 2.73, 1, 'Factory A', 'Operations', 'March diesel - reduced';

-- Q1 2024 - Natural Gas (using 2024 factor)
INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2024-01-20', 'Natural Gas', 900, 'cubic meters', 900 * 2.05, 1, 'Factory A', 'Operations', 'January heating - improved'
FROM emission_factors WHERE activity_name = 'Natural Gas' AND valid_from = '2024-01-01';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2024-02-20', 'Natural Gas', 850, 'cubic meters', 850 * 2.05, 1, 'Factory A', 'Operations', 'February heating - improved'
FROM emission_factors WHERE activity_name = 'Natural Gas' AND valid_from = '2024-01-01';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2024-03-20', 'Natural Gas', 800, 'cubic meters', 800 * 2.05, 1, 'Factory A', 'Operations', 'March heating - improved'
FROM emission_factors WHERE activity_name = 'Natural Gas' AND valid_from = '2024-01-01';

-- Q1 2024 - Gasoline (using 2024 factor)
INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2024-01-25', 'Gasoline', 250, 'litres', 250 * 2.33, 1, 'Fleet', 'Logistics', 'January fleet - EV adoption'
FROM emission_factors WHERE activity_name = 'Gasoline' AND valid_from = '2024-01-01';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2024-02-25', 'Gasoline', 230, 'litres', 230 * 2.33, 1, 'Fleet', 'Logistics', 'February fleet - EV adoption'
FROM emission_factors WHERE activity_name = 'Gasoline' AND valid_from = '2024-01-01';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2024-03-25', 'Gasoline', 240, 'litres', 240 * 2.33, 1, 'Fleet', 'Logistics', 'March fleet - EV adoption'
FROM emission_factors WHERE activity_name = 'Gasoline' AND valid_from = '2024-01-01';

-- Q1 2024 - Grid Electricity (Scope 2, using 2024 factor - cleaner grid)
INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2024-01-10', 'Grid Electricity', 4500, 'kWh', 4500 * 0.42, 2, 'Factory A', 'Operations', 'January electricity - solar panels'
FROM emission_factors WHERE activity_name = 'Grid Electricity' AND valid_from = '2024-01-01';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2024-02-10', 'Grid Electricity', 4300, 'kWh', 4300 * 0.42, 2, 'Factory A', 'Operations', 'February electricity - efficiency'
FROM emission_factors WHERE activity_name = 'Grid Electricity' AND valid_from = '2024-01-01';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2024-03-10', 'Grid Electricity', 4400, 'kWh', 4400 * 0.42, 2, 'Factory A', 'Operations', 'March electricity - LED lighting'
FROM emission_factors WHERE activity_name = 'Grid Electricity' AND valid_from = '2024-01-01';

-- Q1 2024 - Scope 3 emissions (reduced)
INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2024-01-30', 'Business Travel - Air', 1500, 'km', 1500 * 0.25, 3, 'HQ', 'Sales', 'Virtual meetings policy'
FROM emission_factors WHERE activity_name = 'Business Travel - Air';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2024-02-15', 'Employee Commute', 2500, 'km', 2500 * 0.17, 3, 'HQ', 'All', 'Remote work policy'
FROM emission_factors WHERE activity_name = 'Employee Commute';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT factor_id, '2024-03-20', 'Waste Disposal', 400, 'kg', 400 * 0.52, 3, 'Factory A', 'Operations', 'Recycling program'
FROM emission_factors WHERE activity_name = 'Waste Disposal';

-- Q2-Q3 2024
INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2024-04-15', 'Diesel', 420, 'litres', 420 * 2.73, 1, 'Factory A', 'Operations', 'April diesel';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2024-05-15', 'Diesel', 410, 'litres', 410 * 2.73, 1, 'Factory A', 'Operations', 'May diesel';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2024-06-15', 'Diesel', 415, 'litres', 415 * 2.73, 1, 'Factory A', 'Operations', 'June diesel';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2024-07-15', 'Diesel', 425, 'litres', 425 * 2.73, 1, 'Factory A', 'Operations', 'July diesel';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2024-08-15', 'Diesel', 430, 'litres', 430 * 2.73, 1, 'Factory A', 'Operations', 'August diesel';

INSERT INTO emission_records (factor_id, activity_date, activity_name, activity_value, activity_unit, calculated_co2e, scope, location, department, notes)
SELECT 1, '2024-09-15', 'Diesel', 420, 'litres', 420 * 2.73, 1, 'Factory A', 'Operations', 'September diesel';

-- ============================================
-- 4. BUSINESS METRICS (Production Data)
-- ============================================

-- 2023 Production Metrics
INSERT INTO business_metrics (metric_name, value, unit, metric_date, notes)
VALUES 
    ('Tons of Steel Produced', 12000, 'tons', '2023-01-31', 'Q1 production'),
    ('Tons of Steel Produced', 11500, 'tons', '2023-02-28', 'Q1 production'),
    ('Tons of Steel Produced', 12500, 'tons', '2023-03-31', 'Q1 production'),
    ('Tons of Steel Produced', 12200, 'tons', '2023-04-30', 'Q2 production'),
    ('Tons of Steel Produced', 11800, 'tons', '2023-05-31', 'Q2 production'),
    ('Tons of Steel Produced', 12300, 'tons', '2023-06-30', 'Q2 production'),
    ('Tons of Steel Produced', 12600, 'tons', '2023-07-31', 'Q3 production'),
    ('Tons of Steel Produced', 12800, 'tons', '2023-08-31', 'Q3 production'),
    ('Tons of Steel Produced', 12400, 'tons', '2023-09-30', 'Q3 production'),
    ('Tons of Steel Produced', 12100, 'tons', '2023-10-31', 'Q4 production'),
    ('Tons of Steel Produced', 12000, 'tons', '2023-11-30', 'Q4 production'),
    ('Tons of Steel Produced', 11700, 'tons', '2023-12-31', 'Q4 production');

-- 2024 Production Metrics (Higher production, lower emissions = better intensity)
INSERT INTO business_metrics (metric_name, value, unit, metric_date, notes)
VALUES 
    ('Tons of Steel Produced', 13000, 'tons', '2024-01-31', 'Improved efficiency'),
    ('Tons of Steel Produced', 12800, 'tons', '2024-02-29', 'Process optimization'),
    ('Tons of Steel Produced', 13200, 'tons', '2024-03-31', 'New equipment'),
    ('Tons of Steel Produced', 13100, 'tons', '2024-04-30', 'Sustained improvement'),
    ('Tons of Steel Produced', 12900, 'tons', '2024-05-31', 'Maintenance period'),
    ('Tons of Steel Produced', 13300, 'tons', '2024-06-30', 'Peak efficiency'),
    ('Tons of Steel Produced', 13400, 'tons', '2024-07-31', 'Summer production'),
    ('Tons of Steel Produced', 13500, 'tons', '2024-08-31', 'Record output'),
    ('Tons of Steel Produced', 13200, 'tons', '2024-09-30', 'Consistent performance');

-- Revenue Metrics
INSERT INTO business_metrics (metric_name, value, unit, metric_date, notes)
VALUES 
    ('Revenue', 2400000, 'USD', '2023-01-31', 'Q1 revenue'),
    ('Revenue', 2350000, 'USD', '2023-02-28', 'Q1 revenue'),
    ('Revenue', 2500000, 'USD', '2023-03-31', 'Q1 revenue'),
    ('Revenue', 2600000, 'USD', '2024-01-31', 'Growth year'),
    ('Revenue', 2580000, 'USD', '2024-02-29', 'Steady growth'),
    ('Revenue', 2650000, 'USD', '2024-03-31', 'Strong quarter');
