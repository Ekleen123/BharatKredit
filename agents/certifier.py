# agents/certifier.py
class Certifier:
    def validate(self, schema, mappings):
        try:
            required_tables = {"Farmer", "Loan_Application", "Risk_Assessment", "Key_Metrics", "Loan"}
            required_mappings = {"farmer_id": "id", "loan_amount": "amount", "risk_score": "risk_rating"}

            schema_tables = {table['table_name'] for table in schema.get("tables", [])}
            if not required_tables.issubset(schema_tables):
                return "FAIL"

            mapping_dict = {}
            if isinstance(mappings, dict) and "mappings" in mappings:
                for m in mappings["mappings"]:
                    mapping_dict[m["source_attribute"]] = m["target_attribute"]
                mapping_dict.update({k: v for k, v in mappings.items() if k != "mappings"})
            elif isinstance(mappings, dict):  # fallback for older flat format
                mapping_dict = mappings

            for k, v in required_mappings.items():
                if mapping_dict.get(k) != v:
                    return "FAIL"

            return "PASS"
        except Exception as e:
            return f"FAIL ({str(e)})"
