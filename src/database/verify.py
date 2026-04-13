import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/database.sqlite')

def verify_system_state():
    conn = sqlite3.connect(DB_PATH)
    
    print("--- Business Units ---")
    print(pd.read_sql_query("SELECT * FROM business_units", conn))
    
    print("\n--- Emission Factors Sample ---")
    print(pd.read_sql_query("SELECT * FROM emission_factors LIMIT 5", conn))
    
    print("\n--- Calculated Emissions (Total by Scope) ---")
    print(pd.read_sql_query("SELECT scope, SUM(t_co2e) as total_tco2e FROM calculated_emissions GROUP BY scope", conn))
    
    conn.close()

if __name__ == "__main__":
    verify_system_state()
