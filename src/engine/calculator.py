import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/database.sqlite')

class CarbonCalculator:
    def __init__(self):
        self.factors = self._load_factors()

    def _load_factors(self):
        """Loads emission factors from the database into a dictionary for quick lookup."""
        conn = sqlite3.connect(DB_PATH)
        query = "SELECT activity_type, scope, emission_factor FROM emission_factors"
        df = pd.read_sql_query(query, conn)
        conn.close()
        # Create a nested dict: {activity_type: {'scope': scope, 'factor': factor}}
        return df.set_index('activity_type').T.to_dict()

    def calculate_emissions(self, activity_type, quantity):
        """
        Calculates metric tons of CO2e (tCO2e) for a given activity.
        Formula: (Quantity * Factor) / 1000 (to convert kg to metric tons)
        """
        if activity_type not in self.factors:
            print(f"Warning: No factor found for activity type '{activity_type}'")
            return 0, 0
        
        factor_info = self.factors[activity_type]
        factor = factor_info['emission_factor']
        scope = factor_info['scope']
        
        t_co2e = (quantity * factor) / 1000
        return scope, t_co2e

def run_calculation_pipeline():
    """Processes all raw logs in activity_logs and populates calculated_emissions."""
    conn = sqlite3.connect(DB_PATH)
    calc = CarbonCalculator()
    
    # Load all logs
    logs_df = pd.read_sql_query("SELECT * FROM activity_logs", conn)
    
    # Calculate for each log
    results = []
    for _, log in logs_df.iterrows():
        scope, t_co2e = calc.calculate_emissions(log['activity_type'], log['quantity'])
        results.append((
            int(log['unit_id']),
            log['activity_date'],
            scope,
            log['activity_type'],
            t_co2e
        ))
    
    # Clear existing results (for demo idempotency)
    conn.execute("DELETE FROM calculated_emissions")
    
    # Insert new results
    conn.executemany(
        "INSERT INTO calculated_emissions (unit_id, activity_date, scope, category, t_co2e) VALUES (?,?,?,?,?)",
        results
    )
    
    conn.commit()
    conn.close()
    print(f"Processed {len(results)} calculation records.")

if __name__ == "__main__":
    run_calculation_pipeline()
