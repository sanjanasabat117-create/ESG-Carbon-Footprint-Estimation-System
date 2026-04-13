import pandas as pd
import sqlite3
import os
import glob

DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/database.sqlite')
RAW_DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data/raw')

def ingest_raw_logs():
    """Reads all CSV files in data/raw and loads them into activity_logs table."""
    conn = sqlite3.connect(DB_PATH)
    
    csv_files = glob.glob(os.path.join(RAW_DATA_PATH, "*.csv"))
    
    total_rows = 0
    for file in csv_files:
        df = pd.read_csv(file)
        
        # Simple validation/cleaning
        df['activity_date'] = pd.to_datetime(df['activity_date']).dt.strftime('%Y-%m-%d')
        
        # Load into SQL (append)
        df.to_sql('activity_logs', conn, if_exists='append', index=False)
        total_rows += len(df)
        print(f"Ingested {len(df)} rows from {os.path.basename(file)}")
    
    conn.commit()
    conn.close()
    print(f"Ingestion complete. Total rows added: {total_rows}")

if __name__ == "__main__":
    ingest_raw_logs()
