from abc import ABC, abstractmethod
from typing import Any, Dict, List

class LLMProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    async def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        """Generate simple text response."""
        pass

    @abstractmethod
    async def generate_json(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured JSON response."""
        pass
