-- ============================================================================
-- Carbon Emissions Platform - Database Schema
-- ============================================================================
-- This schema supports versioned emission factors, business metrics tracking,
-- comprehensive audit trails, and scalable analytics for GHG emissions reporting.
-- Designed for PostgreSQL 15+
-- ============================================================================

-- ============================================================================
-- TABLE: emission_factors
-- Purpose: Store versioned emission factors for various activities
-- This is the master data that drives all emission calculations
-- ============================================================================
CREATE TABLE emission_factors (
    factor_id SERIAL PRIMARY KEY,
    
    -- Activity identification
    activity_name VARCHAR(255) NOT NULL,  -- e.g., 'Diesel', 'Grid Electricity', 'Natural Gas'
    scope INT NOT NULL CHECK (scope IN (1, 2, 3)),  -- GHG Protocol Scope (1=Direct, 2=Indirect Energy, 3=Value Chain)
    
    -- Emission factor details
    activity_unit VARCHAR(50) NOT NULL,  -- e.g., 'litres', 'kWh', 'tonnes', 'm3'
    co2e_per_unit NUMERIC(12, 6) NOT NULL,  -- The emission factor value (kgCO2e per unit)
    source VARCHAR(255),  -- e.g., 'IPCC 2006 Guidelines', 'CEA India 2023', 'EPA 2024'
    
    -- Versioning and validity
    valid_from DATE NOT NULL,  -- Date this factor becomes valid
    valid_to DATE,  -- Date this factor expires (NULL = currently active)
    
    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by VARCHAR(100),  -- User who created this factor
    
    -- Constraints
    CONSTRAINT valid_date_range CHECK (valid_to IS NULL OR valid_to >= valid_from),
    CONSTRAINT positive_emission_factor CHECK (co2e_per_unit >= 0),
    CONSTRAINT unique_factor_version UNIQUE (activity_name, scope, valid_from)
);

-- Indexes for performance optimization
CREATE INDEX idx_emission_factors_lookup ON emission_factors(activity_name, scope, valid_from, valid_to);
CREATE INDEX idx_emission_factors_active ON emission_factors(activity_name, scope) WHERE valid_to IS NULL;
CREATE INDEX idx_emission_factors_date_range ON emission_factors(valid_from, valid_to);

-- ============================================================================
-- TABLE: business_metrics
-- Purpose: Store key business metrics for emission intensity calculations
-- ============================================================================
CREATE TABLE business_metrics (
    metric_id SERIAL PRIMARY KEY,
    
    -- Metric identification
    metric_name VARCHAR(255) NOT NULL,  -- e.g., 'Tons of Steel Produced', 'Number of Employees', 'Revenue'
    metric_category VARCHAR(100),  -- e.g., 'Production', 'Financial', 'Operational'
    
    -- Metric value
    value NUMERIC(15, 4) NOT NULL,
    unit VARCHAR(50) NOT NULL,  -- e.g., 'tons', 'employees', 'USD'
    
    -- Temporal tracking
    metric_date DATE NOT NULL,  -- The date this metric applies to (e.g., end of month)
    reporting_period VARCHAR(50),  -- e.g., 'Monthly', 'Quarterly', 'Annual'
    
    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by VARCHAR(100),
    notes TEXT,
    
    -- Constraints
    CONSTRAINT positive_metric_value CHECK (value >= 0),
    CONSTRAINT unique_metric_date UNIQUE (metric_name, metric_date)
);

-- Indexes for performance
CREATE INDEX idx_business_metrics_date ON business_metrics(metric_date);
CREATE INDEX idx_business_metrics_name ON business_metrics(metric_name);
CREATE INDEX idx_business_metrics_lookup ON business_metrics(metric_name, metric_date);

-- ============================================================================
-- TABLE: emission_records
-- Purpose: Store every calculated emission record with activity data
-- Links activity data to the specific emission factor version used
-- ============================================================================
CREATE TABLE emission_records (
    record_id SERIAL PRIMARY KEY,
    
    -- Activity details
    activity_date DATE NOT NULL,  -- The date the activity actually occurred
    activity_name VARCHAR(255) NOT NULL,  -- Must match an emission factor
    scope INT NOT NULL CHECK (scope IN (1, 2, 3)),
    
    -- Activity measurement
    activity_value NUMERIC(15, 4) NOT NULL,  -- User-provided value (e.g., 1000 litres)
    activity_unit VARCHAR(50) NOT NULL,  -- Must match the factor's unit
    
    -- Calculation results
    factor_id INT NOT NULL REFERENCES emission_factors(factor_id),  -- FK to exact factor version used
    calculated_co2e NUMERIC(15, 4) NOT NULL,  -- System-calculated result (kgCO2e)
    
    -- Override mechanism
    is_overridden BOOLEAN DEFAULT FALSE,  -- Flag for manual overrides
    overridden_co2e NUMERIC(15, 4),  -- Manually entered value (if overridden)
    override_reason TEXT,  -- Justification for override
    overridden_by VARCHAR(100),  -- User who made the override
    overridden_at TIMESTAMPTZ,  -- When the override occurred
    
    -- Additional context
    location VARCHAR(255),  -- Optional: facility, site, or geographic location
    department VARCHAR(100),  -- Optional: organizational unit
    notes TEXT,  -- Additional comments or context
    
    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by VARCHAR(100),
    
    -- Constraints
    CONSTRAINT positive_activity_value CHECK (activity_value >= 0),
    CONSTRAINT positive_calculated_co2e CHECK (calculated_co2e >= 0),
    CONSTRAINT positive_overridden_co2e CHECK (overridden_co2e IS NULL OR overridden_co2e >= 0),
    CONSTRAINT override_consistency CHECK (
        (is_overridden = FALSE AND overridden_co2e IS NULL) OR
        (is_overridden = TRUE AND overridden_co2e IS NOT NULL)
    )
);

-- Indexes for performance and analytics
CREATE INDEX idx_emission_records_date ON emission_records(activity_date);
CREATE INDEX idx_emission_records_scope ON emission_records(scope);
CREATE INDEX idx_emission_records_activity ON emission_records(activity_name);
CREATE INDEX idx_emission_records_factor ON emission_records(factor_id);
CREATE INDEX idx_emission_records_location ON emission_records(location);
CREATE INDEX idx_emission_records_department ON emission_records(department);
CREATE INDEX idx_emission_records_date_scope ON emission_records(activity_date, scope);
CREATE INDEX idx_emission_records_overridden ON emission_records(is_overridden) WHERE is_overridden = TRUE;

-- ============================================================================
-- TABLE: audit_log
-- Purpose: Comprehensive audit trail for all manual overrides and changes
-- ============================================================================
CREATE TABLE audit_log (
    log_id SERIAL PRIMARY KEY,
    
    -- Reference to the modified record
    record_id INT NOT NULL REFERENCES emission_records(record_id),
    
    -- Change tracking
    action_type VARCHAR(50) NOT NULL,  -- e.g., 'OVERRIDE', 'UPDATE', 'DELETE'
    original_value NUMERIC(15, 4),  -- Original calculated value
    new_value NUMERIC(15, 4),  -- New value after change
    
    -- Justification and context
    reason TEXT NOT NULL,  -- Required justification for the change
    change_category VARCHAR(100),  -- e.g., 'Data Correction', 'Measurement Update', 'Factor Adjustment'
    
    -- User tracking
    changed_by VARCHAR(100) NOT NULL,  -- User who made the change
    changed_at TIMESTAMPTZ DEFAULT NOW(),  -- When the change occurred
    
    -- Additional metadata
    ip_address VARCHAR(45),  -- Optional: IP address for security audit
    user_agent TEXT,  -- Optional: Browser/client information
    notes TEXT
);

-- Indexes for audit queries
CREATE INDEX idx_audit_log_record ON audit_log(record_id);
CREATE INDEX idx_audit_log_user ON audit_log(changed_by);
CREATE INDEX idx_audit_log_date ON audit_log(changed_at);
CREATE INDEX idx_audit_log_action ON audit_log(action_type);

-- ============================================================================
-- TABLE: emission_categories (Optional Enhancement)
-- Purpose: Categorize emission activities for better reporting and analysis
-- ============================================================================
CREATE TABLE emission_categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    category_description TEXT,
    parent_category_id INT REFERENCES emission_categories(category_id),  -- For hierarchical categories
    scope INT CHECK (scope IN (1, 2, 3)),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- TABLE: reporting_periods (Optional Enhancement)
-- Purpose: Define standard reporting periods for consistent analytics
-- ============================================================================
CREATE TABLE reporting_periods (
    period_id SERIAL PRIMARY KEY,
    period_name VARCHAR(100) NOT NULL,  -- e.g., 'Q1 2024', 'FY 2023-2024'
    period_type VARCHAR(50) NOT NULL,  -- e.g., 'Monthly', 'Quarterly', 'Annual'
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_closed BOOLEAN DEFAULT FALSE,  -- Lock period after finalization
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT valid_period_dates CHECK (end_date >= start_date),
    CONSTRAINT unique_period UNIQUE (period_name, period_type)
);

-- ============================================================================
-- VIEWS: Pre-computed views for common analytics queries
-- ============================================================================

-- View: Active emission factors (currently valid)
CREATE VIEW v_active_emission_factors AS
SELECT 
    factor_id,
    activity_name,
    scope,
    activity_unit,
    co2e_per_unit,
    source,
    valid_from,
    valid_to
FROM emission_factors
WHERE valid_to IS NULL OR valid_to >= CURRENT_DATE;

-- View: Emission records with effective CO2e (considering overrides)
CREATE VIEW v_effective_emissions AS
SELECT 
    record_id,
    activity_date,
    activity_name,
    scope,
    activity_value,
    activity_unit,
    factor_id,
    calculated_co2e,
    is_overridden,
    overridden_co2e,
    COALESCE(overridden_co2e, calculated_co2e) AS effective_co2e,
    location,
    department,
    created_at,
    created_by
FROM emission_records;

-- View: Monthly emission summary by scope
CREATE VIEW v_monthly_emissions_by_scope AS
SELECT 
    DATE_TRUNC('month', activity_date) AS month,
    scope,
    SUM(COALESCE(overridden_co2e, calculated_co2e)) AS total_co2e,
    COUNT(*) AS record_count
FROM emission_records
GROUP BY DATE_TRUNC('month', activity_date), scope
ORDER BY month DESC, scope;

-- View: Emission hotspots (top sources by activity)
CREATE VIEW v_emission_hotspots AS
SELECT 
    activity_name,
    scope,
    SUM(COALESCE(overridden_co2e, calculated_co2e)) AS total_co2e,
    COUNT(*) AS activity_count,
    AVG(COALESCE(overridden_co2e, calculated_co2e)) AS avg_co2e
FROM emission_records
GROUP BY activity_name, scope
ORDER BY total_co2e DESC;

-- ============================================================================
-- FUNCTIONS: Helper functions for common operations
-- ============================================================================

-- Function: Get the appropriate emission factor for a given date and activity
CREATE OR REPLACE FUNCTION get_emission_factor(
    p_activity_name VARCHAR,
    p_scope INT,
    p_activity_date DATE
) RETURNS TABLE (
    factor_id INT,
    co2e_per_unit NUMERIC,
    activity_unit VARCHAR,
    source VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ef.factor_id,
        ef.co2e_per_unit,
        ef.activity_unit,
        ef.source
    FROM emission_factors ef
    WHERE ef.activity_name = p_activity_name
      AND ef.scope = p_scope
      AND ef.valid_from <= p_activity_date
      AND (ef.valid_to IS NULL OR ef.valid_to >= p_activity_date)
    ORDER BY ef.valid_from DESC, ef.created_at DESC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;

-- Function: Calculate emission intensity for a period
CREATE OR REPLACE FUNCTION calculate_emission_intensity(
    p_start_date DATE,
    p_end_date DATE,
    p_metric_name VARCHAR
) RETURNS TABLE (
    total_emissions NUMERIC,
    total_metric_value NUMERIC,
    intensity NUMERIC,
    unit TEXT
) AS $$
DECLARE
    v_total_emissions NUMERIC;
    v_total_metric NUMERIC;
    v_metric_unit VARCHAR;
BEGIN
    -- Calculate total emissions
    SELECT SUM(COALESCE(overridden_co2e, calculated_co2e))
    INTO v_total_emissions
    FROM emission_records
    WHERE activity_date BETWEEN p_start_date AND p_end_date;
    
    -- Calculate total metric value
    SELECT SUM(value), MAX(unit)
    INTO v_total_metric, v_metric_unit
    FROM business_metrics
    WHERE metric_name = p_metric_name
      AND metric_date BETWEEN p_start_date AND p_end_date;
    
    -- Return results
    RETURN QUERY
    SELECT 
        COALESCE(v_total_emissions, 0),
        COALESCE(v_total_metric, 0),
        CASE 
            WHEN v_total_metric > 0 THEN v_total_emissions / v_total_metric
            ELSE 0
        END,
        'kgCO2e per ' || COALESCE(v_metric_unit, 'unit');
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- TRIGGERS: Automated data integrity and audit trail
-- ============================================================================

-- Trigger: Update timestamp on record modification
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_emission_factors_updated_at
    BEFORE UPDATE ON emission_factors
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_emission_records_updated_at
    BEFORE UPDATE ON emission_records
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_business_metrics_updated_at
    BEFORE UPDATE ON business_metrics
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger: Automatically log overrides to audit_log
CREATE OR REPLACE FUNCTION log_emission_override()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_overridden = TRUE AND (OLD.is_overridden = FALSE OR OLD.is_overridden IS NULL) THEN
        INSERT INTO audit_log (
            record_id,
            action_type,
            original_value,
            new_value,
            reason,
            changed_by,
            changed_at
        ) VALUES (
            NEW.record_id,
            'OVERRIDE',
            NEW.calculated_co2e,
            NEW.overridden_co2e,
            COALESCE(NEW.override_reason, 'Manual override'),
            NEW.overridden_by,
            NEW.overridden_at
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_log_emission_override
    AFTER UPDATE ON emission_records
    FOR EACH ROW
    WHEN (NEW.is_overridden = TRUE)
    EXECUTE FUNCTION log_emission_override();

-- ============================================================================
-- COMMENTS: Documentation for database objects
-- ============================================================================

COMMENT ON TABLE emission_factors IS 'Master table storing versioned emission factors for GHG calculations';
COMMENT ON TABLE emission_records IS 'Transactional table storing all emission activity records and calculations';
COMMENT ON TABLE business_metrics IS 'Business metrics for emission intensity calculations';
COMMENT ON TABLE audit_log IS 'Comprehensive audit trail for all data modifications';

COMMENT ON COLUMN emission_factors.valid_from IS 'Start date of factor validity period';
COMMENT ON COLUMN emission_factors.valid_to IS 'End date of factor validity (NULL = currently active)';
COMMENT ON COLUMN emission_records.is_overridden IS 'TRUE if calculated value was manually overridden';

-- ============================================================================
-- SAMPLE DATA: Initial seed data for testing and demonstration
-- ============================================================================

-- Insert sample emission factors with versioning
INSERT INTO emission_factors (activity_name, scope, activity_unit, co2e_per_unit, source, valid_from, valid_to, created_by) VALUES
-- Diesel factors (showing version history)
('Diesel', 1, 'litres', 2.68000, 'EPA 2022', '2022-01-01', '2022-12-31', 'system'),
('Diesel', 1, 'litres', 2.71000, 'EPA 2023', '2023-01-01', '2023-12-31', 'system'),
('Diesel', 1, 'litres', 2.73000, 'EPA 2024', '2024-01-01', NULL, 'system'),

-- Natural Gas factors
('Natural Gas', 1, 'm3', 2.03000, 'IPCC 2006', '2022-01-01', '2023-12-31', 'system'),
('Natural Gas', 1, 'm3', 2.05000, 'IPCC 2024', '2024-01-01', NULL, 'system'),

-- Grid Electricity factors (Scope 2)
('Grid Electricity', 2, 'kWh', 0.45000, 'CEA India 2023', '2023-01-01', '2023-12-31', 'system'),
('Grid Electricity', 2, 'kWh', 0.42000, 'CEA India 2024', '2024-01-01', NULL, 'system'),

-- Additional fuel types
('Petrol', 1, 'litres', 2.31000, 'EPA 2024', '2024-01-01', NULL, 'system'),
('LPG', 1, 'kg', 2.98000, 'IPCC 2006', '2022-01-01', NULL, 'system'),
('Coal', 1, 'tonnes', 2419.00000, 'IPCC 2006', '2022-01-01', NULL, 'system');

-- Insert sample business metrics
INSERT INTO business_metrics (metric_name, metric_category, value, unit, metric_date, reporting_period, created_by) VALUES
-- Production metrics
('Tons of Steel Produced', 'Production', 45000.00, 'tons', '2023-01-31', 'Monthly', 'system'),
('Tons of Steel Produced', 'Production', 48000.00, 'tons', '2023-02-28', 'Monthly', 'system'),
('Tons of Steel Produced', 'Production', 47500.00, 'tons', '2023-03-31', 'Monthly', 'system'),
('Tons of Steel Produced', 'Production', 50000.00, 'tons', '2024-01-31', 'Monthly', 'system'),
('Tons of Steel Produced', 'Production', 52000.00, 'tons', '2024-02-29', 'Monthly', 'system'),

-- Employee metrics
('Number of Employees', 'Operational', 1200.00, 'employees', '2023-12-31', 'Annual', 'system'),
('Number of Employees', 'Operational', 1250.00, 'employees', '2024-12-31', 'Annual', 'system');

-- ============================================================================
-- GRANTS: Security and access control (adjust based on your user roles)
-- ============================================================================

-- Example: Grant read-only access to reporting users
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO reporting_user;
-- GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO reporting_user;

-- Example: Grant full access to application users
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO app_user;

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
