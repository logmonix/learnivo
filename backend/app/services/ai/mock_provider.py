from typing import Any, Dict
from app.services.ai.base import LLMProvider

class MockProvider(LLMProvider):
    """Used when no API keys are present or for testing."""
    
    async def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        if "lesson" in prompt.lower():
            return """
# Welcome to the World of Numbers! 🎉

Numbers are everywhere! From counting your toys to telling time, numbers help us understand the world.

## What are Numbers?
Numbers are symbols we use to count and measure things. The numbers you know (0, 1, 2, 3...) are called "digits."

## Fun Facts! 
- The number 0 was invented over 1,500 years ago!
- Ancient people used their fingers to count, which is why we have 10 digits (0-9)
- The biggest number has a name: it's called a "googolplex"!

## Let's Practice!
Try counting objects around you. How many books do you see? How many windows? Numbers make it easy to keep track!

Remember: Math is like a superpower that helps you solve problems every day! 💪
"""
        return f"[MOCK AI RESPONSE] You asked: {prompt}. Here is a fun fact about space!"

    async def generate_json(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        # Return a mock structure based on expected use cases
        if "chapters" in prompt.lower():
            return {
                "chapters": [
                    {"title": "The Magic of Numbers", "description": "Intro to numbers"},
                    {"title": "Adding Apples", "description": "Basic addition"},
                    {"title": "Taking Away Toys", "description": "Basic subtraction"}
                ]
            }
        elif "questions" in prompt.lower():
            return {
                "questions": [
                    {
                        "question": "What is 2 + 2?",
                        "options": {"A": "3", "B": "4", "C": "5", "D": "6"},
                        "correct_answer": "B",
                        "explanation": "When you add 2 and 2 together, you get 4!"
                    },
                    {
                        "question": "Which number comes after 5?",
                        "options": {"A": "4", "B": "5", "C": "6", "D": "7"},
                        "correct_answer": "C",
                        "explanation": "The number 6 comes right after 5 when counting!"
                    }
                ]
            }
        return {"data": "Mock JSON Data"}
