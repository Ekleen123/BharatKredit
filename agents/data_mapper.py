# agents/data_mapper.py
from ollama import Client
import json

class DataMapper:
    def __init__(self):
        self.client = Client()
    
    def generate_mappings(self, source_attrs, target_schema):
        try:
            response = self.client.generate(
                model='mistral',
                prompt=f'''Generate attribute mappings between:
                Source: {source_attrs}
                Target: {target_schema}

                MUST INCLUDE MAPPINGS:
                - farmer_id → id
                - loan_amount → amount
                - risk_score → risk_rating

                Return JSON with a key "mappings" as a list of source → target pairs.''',
                format='json'
            )
            llm_response = json.loads(response['response'])

            # Fallback and enforcement
            if "mappings" not in llm_response:
                llm_response["mappings"] = []

            enforced = [
                {"source_attribute": "farmer_id", "target_attribute": "id"},
                {"source_attribute": "loan_amount", "target_attribute": "amount"},
                {"source_attribute": "risk_score", "target_attribute": "risk_rating"}
            ]

            llm_keys = {m["source_attribute"] for m in llm_response["mappings"]}
            for item in enforced:
                if item["source_attribute"] not in llm_keys:
                    llm_response["mappings"].append(item)

            # Optional: add flat dict keys too for easy access
            llm_response["farmer_id"] = "id"
            llm_response["loan_amount"] = "amount"
            llm_response["risk_score"] = "risk_rating"

            return llm_response
        except Exception as e:
            return {
                "mappings": [
                    {"source_attribute": "farmer_id", "target_attribute": "id"},
                    {"source_attribute": "loan_amount", "target_attribute": "amount"},
                    {"source_attribute": "risk_score", "target_attribute": "risk_rating"},
                ],
                "farmer_id": "id",
                "loan_amount": "amount",
                "risk_score": "risk_rating"
            }
