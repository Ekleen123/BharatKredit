# agents/gemma_agent.py

import requests

class GemmaAgent:
    def __init__(self, base_url="http://localhost:11434/api/generate"):
        self.base_url = base_url

    def translate(self, text, target_language):
        """Translate text to target_language using Gemma model."""
        prompt = (
            f"Translate the following message to {target_language}:\n\n"
            f"{text}"
        )
        response = requests.post(self.base_url, json={
            "model": "gemma",
            "prompt": prompt,
            "stream": False
        })
        if response.status_code == 200:
            return response.json()['response'].strip()
        else:
            raise Exception(f"Gemma API error: {response.text}")
