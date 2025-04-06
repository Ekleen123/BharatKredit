from ollama import Client

class CarbonScorer:
    def calculate_score(self, practices):
        """Complete implementation"""
        practice_scores = {
            'organic': 9.5,
            'drip irrigation': 8.0,
            'chemical fertilizers': 2.5,
            'crop rotation': 7.0
        }
        total = sum(practice_scores.get(p.strip().lower(), 0) 
                   for p in practices.split(','))
        return {'score': min(total, 10)}  # Cap score at 10