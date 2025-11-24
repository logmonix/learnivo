import json
from typing import Any, Dict
import openai
from app.core.config import settings
from app.services.ai.base import LLMProvider

class OpenAIProvider(LLMProvider):
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-3.5-turbo" # Default cost-effective model

    async def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content

    async def generate_json(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Forces JSON output. For GPT-3.5/4, we can use response_format={"type": "json_object"}
        """
        system_prompt = "You are a helpful AI assistant that outputs strictly valid JSON."
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{prompt}\n\nOutput JSON matching this schema: {json.dumps(schema)}"}
        ]

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        content = response.choices[0].message.content
        return json.loads(content)
