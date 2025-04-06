# agents/data_architecture.py
from ollama import Client
import json

class DataArchitect:
    def __init__(self):
        self.client = Client()
    
    def design_schema(self, requirements):
        try:
            response = self.client.generate(
                model='mistral',
                prompt=f'''Design a relational schema for:
                Requirements: {requirements}
                Tables: Farmer, Loan_Application, Risk_Assessment, Key_Metrics, Loan
                Include field names, types, keys
                Return JSON like: {{ "tables": [{{ "table_name": ..., "fields": [{{"name": ..., "data_type": ..., "is_key": ..., ...}}] }}] }}''',
                format='json'
            )
            return json.loads(response['response'])
        except Exception:
            return {
                "tables": [
                    {
                        "table_name": "Farmer",
                        "fields": [
                            {"name": "farmer_id", "data_type": "integer", "is_key": True},
                            {"name": "name", "data_type": "string"},
                            {"name": "region", "data_type": "string"}
                        ]
                    },
                    {
                        "table_name": "Loan",
                        "fields": [
                            {"name": "loan_id", "data_type": "integer", "is_key": True},
                            {"name": "farmer_id", "data_type": "integer", "foreign_key": True},
                            {"name": "loan_amount", "data_type": "decimal"},
                            {"name": "risk_score", "data_type": "decimal"}
                        ]
                    }
                ]
            }
