from typing import Dict, Any

class PromptManager:
    """Manages AI prompts for different content generation tasks."""
    
    @staticmethod
    def lesson_prompt(chapter_title: str, chapter_description: str, grade: int) -> str:
        return f"""
You are an expert educator creating engaging lesson content for a Grade {grade} student.

Chapter: {chapter_title}
Description: {chapter_description}

Create a fun, interactive lesson that:
1. Explains the concept in simple, kid-friendly language
2. Uses real-world examples and analogies
3. Includes 2-3 fun facts or interesting tidbits
4. Is approximately 300-500 words

Write the lesson in a conversational, encouraging tone. Use emojis sparingly to make it engaging.
"""

    @staticmethod
    def quiz_prompt(chapter_title: str, lesson_content: str, grade: int) -> str:
        return f"""
Based on this lesson about "{chapter_title}" for Grade {grade} students:

{lesson_content[:500]}...

Generate 5 multiple-choice questions to test understanding.
Each question should have:
- A clear question text
- 4 answer options (labeled A, B, C, D)
- The correct answer (letter)
- A brief explanation of why that answer is correct

Make questions fun and engaging, not too difficult.
Output as JSON with this structure:
{{
    "questions": [
        {{
            "question": "What is...",
            "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
            "correct_answer": "A",
            "explanation": "..."
        }}
    ]
}}
"""
