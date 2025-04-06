import sqlite3
from agents.carbon_scorer import CarbonScorer

class LoanManager:
    def __init__(self, connection):
        self.conn = connection
        
    def approve_loan(self, farmer_id, amount):
        """Complete loan approval workflow"""
        cursor = self.conn.cursor()
        
        # 1. Get farming practices
        cursor.execute("SELECT practices FROM farmers WHERE id=?", (farmer_id,))
        practices = cursor.fetchone()[0]
        
        # 2. Calculate carbon score
        carbon_score = CarbonScorer().calculate_score(practices)['score']
        
        # 3. Calculate interest rate
        base_rate = 12.0
        final_rate = round(base_rate - (carbon_score * 0.1), 2)
        
        # 4. Insert loan record
        cursor.execute('''
            INSERT INTO loans (farmer_id, amount, interest_rate)
            VALUES (?, ?, ?)
        ''', (farmer_id, amount, final_rate))
        
        return final_rate