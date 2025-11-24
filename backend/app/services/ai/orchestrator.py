from app.core.config import settings
from app.services.ai.base import LLMProvider
from app.services.ai.openai_provider import OpenAIProvider
from app.services.ai.mock_provider import MockProvider

class AIOrchestrator:
    def __init__(self):
        self.providers: Dict[str, LLMProvider] = {}
        
        # Initialize providers based on available keys
        if settings.OPENAI_API_KEY:
            self.providers["openai"] = OpenAIProvider()
        
        # Always have a mock fallback
        self.providers["mock"] = MockProvider()

    def get_provider(self, preferred: str = "openai") -> LLMProvider:
        if preferred in self.providers:
            return self.providers[preferred]
        return self.providers["mock"]

    async def generate_curriculum(self, grade: int, subject: str) -> dict:
        """
        Orchestrates the generation of a curriculum (list of chapters).
        """
        provider = self.get_provider()
        
        prompt = f"""
        Generate a fun and engaging curriculum for {subject} for a Grade {grade} student.
        Create 5-8 chapters.
        Each chapter should have a 'title' (fun name) and 'description'.
        """
        
        schema = {
            "type": "object",
            "properties": {
                "chapters": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "description": {"type": "string"}
                        }
                    }
                }
            }
        }
        
        return await provider.generate_json(prompt, schema)

    async def generate_lesson(self, chapter_title: str, chapter_description: str, grade: int) -> dict:
        """Generate lesson content and quiz for a chapter."""
        from app.services.ai.prompts import PromptManager
        
        provider = self.get_provider()
        
        # 1. Generate lesson text
        lesson_prompt = PromptManager.lesson_prompt(chapter_title, chapter_description, grade)
        lesson_text = await provider.generate_text(lesson_prompt)
        
        # 2. Generate quiz based on lesson
        quiz_prompt = PromptManager.quiz_prompt(chapter_title, lesson_text, grade)
        quiz_schema = {
            "type": "object",
            "properties": {
                "questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "options": {"type": "object"},
                            "correct_answer": {"type": "string"},
                            "explanation": {"type": "string"}
                        }
                    }
                }
            }
        }
        
        quiz_data = await provider.generate_json(quiz_prompt, quiz_schema)
        
        return {
            "lesson_text": lesson_text,
            "quiz": quiz_data
        }

# Singleton instance
ai_orchestrator = AIOrchestrator()
