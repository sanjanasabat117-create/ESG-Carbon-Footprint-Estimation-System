import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/database.sqlite')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

def initialize_db():
    """Initializes the SQLite database with the schema."""
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SCHEMA_PATH, 'r') as f:
        schema = f.read()
        cursor.executescript(schema)

    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == "__main__":
    initialize_db()
