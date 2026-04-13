-- Schema for Carbon Footprint Estimation System

-- Business Units Table
CREATE TABLE IF NOT EXISTS business_units (
    unit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    unit_name TEXT NOT NULL,
    region TEXT NOT NULL,
    industry_segment TEXT,
    employee_count INTEGER,
    annual_revenue REAL -- USD
);

-- Emission Factors Table (EPA/DEFRA reference)
CREATE TABLE IF NOT EXISTS emission_factors (
    factor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    activity_type TEXT NOT NULL, -- e.g., 'Stationary Combustion - Natural Gas'
    scope INTEGER NOT NULL,      -- 1, 2, or 3
    unit TEXT NOT NULL,          -- e.g., 'scf', 'kWh', 'mile'
    emission_factor REAL NOT NULL, -- kg CO2e per unit
    source TEXT,                -- 'EPA Hub 2023', 'DEFRA'
    year INTEGER
);

-- Activity Logs Table (Raw data)
CREATE TABLE IF NOT EXISTS activity_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    unit_id INTEGER,
    activity_date DATE NOT NULL,
    activity_type TEXT NOT NULL,
    quantity REAL NOT NULL,
    original_unit TEXT NOT NULL,
    FOREIGN KEY (unit_id) REFERENCES business_units(unit_id)
);

-- Calculated Emissions Table (Aggregated for Reporting)
CREATE TABLE IF NOT EXISTS calculated_emissions (
    emission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    unit_id INTEGER,
    activity_date DATE,
    scope INTEGER,
    category TEXT,
    t_co2e REAL, -- metric tons of CO2e
    FOREIGN KEY (unit_id) REFERENCES business_units(unit_id)
);
