# agents/documentation.py
from ollama import Client
import json

class DocumentationAgent:
    def __init__(self):
        self.client = Client()

    def generate_report(self, schema, mappings, certification):
        try:
            prompt = f"""
            Generate a concise report summarizing the following system setup:

            Schema:
            {json.dumps(schema, indent=2)}

            Mappings:
            {json.dumps(mappings, indent=2)}

            Certification Result: {certification}

            Include status and brief justification.
            """
            response = self.client.generate(
                model="mistral",
                prompt=prompt,
                format="json"
            )
            # Ensure response is dict, else fallback
            if isinstance(response, dict) and "response" in response:
                return response["response"]
            else:
                return self._fallback_report(schema, mappings, certification)
        except Exception:
            return self._fallback_report(schema, mappings, certification)

    def _fallback_report(self, schema, mappings, certification):
        return f"""
        System Report:

        ✅ Schema with {len(schema.get('tables', []))} tables generated.
        ✅ Attribute mappings created.
        ✅ Certification Status: {certification}

        System is ready for deployment based on the above configuration.
        """
