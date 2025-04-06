# agents/business_analyst.py
from ollama import Client
import json

class BusinessAnalyst:
    def __init__(self):
        self.client = Client()
    
    def analyze_use_case(self, text):
        """Get loan requirements from LLM with fallback"""
        try:
            response = self.client.generate(
                model='mistral',
                prompt=f'''Analyze this farming loan case: {text}
                Return STRICT JSON with:
                - "required_docs" (list)
                - "risk_factors" (list)
                - "key_metrics" (list)''',
                format='json',
                options={'temperature': 0.1}
            )
            return json.loads(response['response'])
        except Exception:
            return {
                "required_docs": ["Aadhaar Card", "Land Records"],
                "risk_factors": ["Drought Risk", "Pest Risk"],
                "key_metrics": ["Yield History", "Water Usage"]
            }