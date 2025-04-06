import sqlite3
import pandas as pd
import os

print("🚀 Starting database initialization...")

# Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, '../loans.db')
csv_path = os.path.join(current_dir, '../data/farmers.csv')

print(f"📂 Database will be created at: {db_path}")

# Create database and tables
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            region TEXT,
            crop TEXT,
            practices TEXT,
            language TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loans (
            farmer_id INTEGER,
            amount REAL,
            interest_rate REAL,
            status TEXT
        )
    ''')
    
    # Insert data from CSV
    if os.path.exists(csv_path):
        farmers_df = pd.read_csv(csv_path)
        farmers_df.to_sql('farmers', conn, if_exists='replace', index=False)
        print(f"✅ Inserted {len(farmers_df)} farmers from CSV!")
    else:
        print(f"⚠️ Warning: {csv_path} not found - creating empty tables")
    
    conn.commit()
    print("🎉 Database initialized successfully!")

except Exception as e:
    print(f"❌ Error: {str(e)}")
finally:
    if 'conn' in locals():
        conn.close()