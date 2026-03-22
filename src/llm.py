"""OpenRouter API client for LLM interactions."""

import json
import os
import time

import httpx


class LLMClient:
    """Generic OpenRouter API client with retry logic."""

    def __init__(self):
        """Initialize LLM client with configuration from environment."""
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise Exception("OPENROUTER_API_KEY environment variable not set")

        self.model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3-haiku")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.timeout = 30.0
        self.max_retries = 3

    def complete(self, prompt: str) -> str:
        """Send prompt to LLM, return response text with retry logic."""
        for attempt in range(self.max_retries):
            try:
                response = httpx.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [{"role": "user", "content": prompt}]
                    },
                    timeout=self.timeout
                )

                if response.status_code == 401:
                    raise Exception("Invalid OpenRouter API key")

                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        print("Rate limited. Waiting 60 seconds...")
                        time.sleep(60)
                        continue
                    raise Exception("Rate limited")

                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]

            except httpx.TimeoutException:
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise Exception("Request timeout")

            except httpx.NetworkError:
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise Exception("Network error")

        raise Exception("Max retries exceeded")

    def parse_json(self, response: str) -> dict:
        """Extract and parse JSON from response (handle markdown blocks)."""
        response = response.strip()

        # Remove markdown code blocks if present
        if response.startswith("```"):
            lines = response.split("\n")
            # Remove first line (```json or ```) and last line (```)
            if len(lines) > 2:
                response = "\n".join(lines[1:-1])

        return json.loads(response)
