# agents/data_governance.py
import pandas as pd
from pathlib import Path

class DataGovernanceAgent:
    def __init__(self):
        self.catalog = self._load_catalog()
    
    def _load_catalog(self):
        """Load or create governance catalog"""
        path = Path('data/governance_catalog.csv')
        if not path.exists():
            path.parent.mkdir(exist_ok=True)
            pd.DataFrame({
                'source_system': ['UPI', 'Aadhaar'],
                'attribute': ['txn_id', 'uid'],
                'data_type': ['string', 'number'],
                'sensitivity': ['high', 'critical']
            }).to_csv(path, index=False)
        return pd.read_csv(path)

    def get_attribute_info(self, system):
        """Get attributes for a system"""
        results = self.catalog[self.catalog['source_system'] == system]
        return results.to_dict('records')