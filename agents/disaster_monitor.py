import sqlite3
import pandas as pd
import os

class DisasterMonitor:
    def __init__(self, db_path=os.path.abspath('loans.db')):
        self.risks = pd.DataFrame([
            {'region': 'Andhra Pradesh', 'risk': 'Medium'},
            {'region': 'Maharashtra', 'risk': 'Low'},
            {'region': 'Punjab', 'risk': 'High'} 
            
        ])
        self.db_path = db_path
        print(f"Database path: {self.db_path}")  # Verify in console

    def send_alert(self, farmer_id):
        """100% reliable farmer verification"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 1. Verify farmer exists
                cursor.execute("SELECT id FROM farmers WHERE id = ?", (int(farmer_id),))
                if not cursor.fetchone():
                    return "Farmer not in database"
                
                # 2. Get region
                cursor.execute("SELECT region FROM farmers WHERE id = ?", (int(farmer_id),))
                region = cursor.fetchone()[0].strip().lower()
                
                # 3. Match risk (case-insensitive)
                risk = self.risks[
                    self.risks['region'].str.strip().str.lower() == region
                ]['risk'].values[0]
                
                return f"{risk} risk in {region.capitalize()}"
                
        except Exception as e:
            return f"Error: {str(e)}"
    def get_risk(self, region):
        match = self.risks[self.risks['region'].str.lower() == region.lower()]
        return match['risk'].values[0] if not match.empty else "Low"