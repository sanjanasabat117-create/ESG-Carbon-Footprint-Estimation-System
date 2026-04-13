import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/database.sqlite')

def seed_reference_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Seed Business Units
    units = [
        ('Factory Alpha', 'North America', 'Manufacturing', 500, 120000000),
        ('Regional Hub Beta', 'Europe', 'Logistics', 200, 45000000),
        ('Corporate HQ', 'Asia', 'Corporate', 800, 300000000),
        ('Warehouse Gamma', 'South America', 'Logistics', 150, 15000000)
    ]
    cursor.executemany("INSERT INTO business_units (unit_name, region, industry_segment, employee_count, annual_revenue) VALUES (?,?,?,?,?)", units)

    # Seed Emission Factors (Rough EPA/DEFRA 2023 factors in kg CO2e)
    # Reference: 1 kWh Electricity (US Avg) ~ 0.37 kg CO2e
    # Reference: 1 gallon Diesel ~ 10.18 kg CO2e
    # Reference: 1 mile Business Travel (Short haul) ~ 0.2 kg CO2e/mile
    factors = [
        # Scope 1
        ('Natural Gas Stationary', 1, 'scf', 0.0545, 'EPA Hub 2023', 2023),
        ('Diesel Mobile', 1, 'gallon', 10.21, 'EPA Hub 2023', 2023),
        ('Gasoline Mobile', 1, 'gallon', 8.78, 'EPA Hub 2023', 2023),
        
        # Scope 2
        ('Electricity - Grid', 2, 'kWh', 0.37, 'EPA eGRID 2023', 2023),
        
        # Scope 3
        ('Air Travel - Long Haul', 3, 'mile', 0.16, 'DEFRA 2023', 2023),
        ('Air Travel - Short Haul', 3, 'mile', 0.24, 'DEFRA 2023', 2023),
        ('Waste - Landfill', 3, 'metric ton', 500.0, 'EPA WasteHub 2023', 2023),
        ('Hotel Stay', 3, 'night', 15.0, 'GHG Protocol', 2023)
    ]
    cursor.executemany("INSERT INTO emission_factors (activity_type, scope, unit, emission_factor, source, year) VALUES (?,?,?,?,?,?)", factors)

    conn.commit()
    conn.close()
    print("Reference data seeded successfully.")

if __name__ == "__main__":
    seed_reference_data()
