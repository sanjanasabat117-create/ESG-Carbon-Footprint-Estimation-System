import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data/raw')

def generate_activity_logs():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    units = [1, 2, 3, 4] # IDs mapped from seed_data
    activity_types = [
        ('Natural Gas Stationary', 'scf', 1000, 5000),
        ('Diesel Mobile', 'gallon', 50, 200),
        ('Electricity - Grid', 'kWh', 5000, 20000),
        ('Air Travel - Long Haul', 'mile', 1000, 5000),
        ('Waste - Landfill', 'metric ton', 1, 5)
    ]

    data = []
    start_date = datetime(2023, 1, 1)
    
    # Generate 12 months of data for each unit
    for unit_id in units:
        for month in range(12):
            date = start_date + timedelta(days=month*30)
            for act_type, unit, min_q, max_q in activity_types:
                quantity = np.random.uniform(min_q, max_q)
                data.append({
                    'unit_id': unit_id,
                    'activity_date': date.strftime('%Y-%m-%d'),
                    'activity_type': act_type,
                    'quantity': round(quantity, 2),
                    'original_unit': unit
                })

    df = pd.DataFrame(data)
    file_path = os.path.join(DATA_DIR, 'activity_logs_2023.csv')
    df.to_csv(file_path, index=False)
    print(f"Generated synthetic logs at {file_path}")

if __name__ == "__main__":
    generate_activity_logs()
