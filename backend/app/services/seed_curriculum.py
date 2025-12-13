# Seed script for Standard 4 curriculum (Maths, English, Science)
# Generates subjects, chapters, lessons and quizzes using static content.

import uuid
import os
import sys
# Ensure the project root is on PYTHONPATH so absolute imports work when running this script directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..", "backend")))

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.curriculum import Subject, Chapter, ContentBlock

# Helper to create a lesson content block
async def _create_lesson(db: AsyncSession, chapter: Chapter, title: str, markdown: str):
    lesson = ContentBlock(
        chapter_id=chapter.id,
        block_type="lesson",
        content_data={"markdown": markdown},
        ai_model_used="seed_script",
    )
    db.add(lesson)
    await db.flush()
    return lesson

# Helper to create a quiz content block
async def _create_quiz(db: AsyncSession, chapter: Chapter, title: str, questions: list):
    quiz = ContentBlock(
        chapter_id=chapter.id,
        block_type="quiz",
        content_data={"questions": questions},
        ai_model_used="seed_script",
    )
    db.add(quiz)
    await db.flush()
    return quiz

# Sample data for Standard 4 (CBSE) – limited to a few chapters per subject for brevity.
MATHS_CHAPTERS = [
    {
        "title": "Numbers up to 1000",
        "lesson_md": "# Numbers up to 1000\n\n## Learning Objectives\n- Read, write and compare numbers up to 1000.\n- Understand place value (hundreds, tens, units).\n\n## Explanation\nA three‑digit number is made of **hundreds**, **tens**, and **units**. For example, **742** = 7 hundreds + 4 tens + 2 units.\n\n### Place‑Value Chart\n| Hundreds | Tens | Units |\n|----------|------|-------|\n| 0‑9      | 0‑9  | 0‑9   |\n\n## Worked Example\n**Problem:** 483 + 259 = ?\n1. Add units: 3 + 9 = 12 → write 2, carry 1.\n2. Add tens: 8 + 5 + 1 = 14 → write 4, carry 1.\n3. Add hundreds: 4 + 2 + 1 = 7.\n**Answer:** 742\n\n## Practice Questions\n1. 527 + 186 = ?\n2. 904 – 375 = ?\n3. Write 658 in words.\n\n## Mini‑Game Idea\n**Number Tower** – Drag and drop digit blocks to build the correct three‑digit number shown on the screen. Earn 5 XP per correct tower.",
        "quiz_questions": [
            {"question": "527 + 186 = ?", "options": ["713", "713?", "713"], "answer": "713"},
            {"question": "904 – 375 = ?", "options": ["529", "529", "529"], "answer": "529"},
            {"question": "Write 658 in words.", "options": ["Six hundred fifty‑eight", "Six hundred and fifty‑eight", "Six hundred fifty eight"], "answer": "Six hundred fifty‑eight"}
        ]
    },
    {
        "title": "Fractions",
        "lesson_md": "# Fractions\n\n## Learning Objectives\n- Understand numerator and denominator.\n- Represent fractions on a number line.\n- Add and subtract simple fractions with like denominators.\n\n## Explanation\nA fraction \u00A0`a/b` represents **a** parts out of **b** equal parts. The **denominator** (bottom) tells how many equal parts the whole is divided into, while the **numerator** (top) tells how many of those parts we have.\n\n### Visual Example\nImagine a pizza cut into 8 equal slices. One slice is `1/8`. Three slices are `3/8`.\n\n## Adding Fractions with Same Denominator\n`a/b + c/b = (a + c)/b`\n\n**Example:** `3/8 + 2/8 = (3+2)/8 = 5/8`\n\n## Practice Questions\n1. What is `4/10 + 3/10`?\n2. If you have `2/5` of a chocolate bar and eat `1/5`, how much is left?\n\n## Mini‑Game Idea\n**Fraction Pizza** – Drag pizza slices to match the given fraction. Earn stars for speed.",
        "quiz_questions": [
            {"question": "3/8 + 2/8 = ?", "options": ["5/8", "5/8", "5/8"], "answer": "5/8"},
            {"question": "4/10 + 3/10 = ?", "options": ["7/10", "7/10", "7/10"], "answer": "7/10"},
            {"question": "2/5 – 1/5 = ?", "options": ["1/5", "1/5", "1/5"], "answer": "1/5"}
        ]
    },
    {
        "title": "Geometry – Shapes and Perimeter",
        "lesson_md": "# Geometry – Shapes and Perimeter\n\n## Objectives\n- Identify basic 2D shapes (square, rectangle, triangle, circle).\n- Calculate perimeter of squares and rectangles.\n\n## Explanation\nPerimeter is the total distance around a shape. For a rectangle: `Perimeter = 2 × (length + width)`.\n\n## Examples\n- Square with side 5 cm → Perimeter = 4 × 5 = 20 cm.\n- Rectangle 3 cm × 7 cm → Perimeter = 2 × (3+7) = 20 cm.\n\n## Practice Questions\n1. Find the perimeter of a square with side 9 cm.\n2. Find the perimeter of a rectangle 4 cm × 6 cm.\n\n## Mini‑Game Idea\n**Shape Builder** – Drag sides to form a shape that matches a given perimeter.",
        "quiz_questions": [
            {"question": "Perimeter of square side 9 cm?", "options": ["36 cm", "36 cm", "36"], "answer": "36 cm"},
            {"question": "Perimeter of rectangle 4 cm × 6 cm?", "options": ["20 cm", "20 cm", "20"], "answer": "20 cm"}
        ]
    },
    {
        "title": "Data Handling – Tables and Graphs",
        "lesson_md": "# Data Handling – Tables and Graphs\n\n## Objectives\n- Read and interpret simple tables.\n- Plot basic bar graphs from given data.\n\n## Explanation\nA table organizes data in rows and columns. A bar graph visualizes the same data with bars whose lengths represent values.\n\n## Example Table\n| Fruit | Quantity |\n|-------|----------|\n| Apple | 5 |\n| Banana | 3 |\n\n## Example Bar Graph\n(Imagine a bar graph with two bars: Apple = 5, Banana = 3)\n\n## Practice Questions\n1. If the table shows 8 oranges, how tall should the orange bar be compared to a bar of 4 apples?\n2. Fill the missing value: Apples = 6, Bananas = ?, Total = 10.\n\n## Mini‑Game Idea\n**Data Detective** – Match bars to correct table entries under a time limit.",
        "quiz_questions": [
            {"question": "If oranges = 8 and apples = 4, orange bar is how many times taller?", "options": ["2×", "2 times", "2"], "answer": "2×"},
            {"question": "Apples = 6, total = 10, bananas = ?", "options": ["4", "4", "4"], "answer": "4"}
        ]
    },
    {
        "title": "Measurement – Length and Mass",
        "lesson_md": "# Measurement – Length and Mass\n\n## Objectives\n- Convert between centimeters and meters.\n- Understand basic units of mass (grams, kilograms).\n\n## Explanation\n1 meter = 100 centimeters. 1 kilogram = 1000 grams.\n\n## Examples\n- 250 cm = 2.5 m.\n- 1500 g = 1.5 kg.\n\n## Practice Questions\n1. Convert 3.2 m to centimeters.\n2. Convert 750 g to kilograms.\n\n## Mini‑Game Idea\n**Conversion Race** – Quickly convert given measurements to earn points.",
        "quiz_questions": [
            {"question": "3.2 m = ? cm", "options": ["320 cm", "320 cm", "320"], "answer": "320 cm"},
            {"question": "750 g = ? kg", "options": ["0.75 kg", "0.75 kg", "0.75"], "answer": "0.75 kg"}
        ]
    }
]


ENGLISH_CHAPTERS = [
    {
        "title": "Reading Comprehension – Short Stories",
        "lesson_md": "# Reading Comprehension – Short Stories\n\n## Objectives\n- Improve reading fluency.\n- Develop ability to answer questions based on a passage.\n\n## Story: *The Clever Monkey*\n*Once upon a time, a clever monkey lived in a forest. He loved solving puzzles...* (full story omitted for brevity).\n\n## Questions (after reading)\n1. What was the monkey’s favorite activity?\n2. How did the monkey solve the puzzle?\n\n## Mini‑Game Idea\n**Story Puzzle** – As the story unfolds, children choose the correct next line from options. Correct choices reveal hidden treasures.",
        "quiz_questions": [
            {"question": "What was the monkey’s favorite activity?", "options": ["Solving puzzles", "Sleeping", "Eating bananas"], "answer": "Solving puzzles"},
            {"question": "How did the monkey solve the puzzle?", "options": ["By thinking", "By asking friends", "By using a tool"], "answer": "By thinking"}
        ]
    },
    {
        "title": "Grammar – Simple Present Tense",
        "lesson_md": "# Grammar – Simple Present Tense\n\n## Learning Objectives\n- Form simple present sentences.\n- Use correct verb forms for singular and plural subjects.\n\n## Rules\n1. For **he/she/it**, add **‑s** or **‑es** to the base verb.\n2. For **I/you/we/they**, use the base verb unchanged.\n\n## Examples\n- *She **runs** fast.*\n- *They **run** fast.*\n\n## Practice Sentences (fill in the blank)\n1. He ___ (play) cricket.\n2. We ___ (go) to school.\n\n## Mini‑Game Idea\n**Verb Builder** – Drag the correct suffix onto the verb to complete the sentence. Earn points for speed.",
        "quiz_questions": [
            {"question": "She ___ (watch) TV.", "options": ["watches", "watch", "watched"], "answer": "watches"},
            {"question": "They ___ (play) football.", "options": ["plays", "play", "played"], "answer": "play"}
        ]
    }
]

SCIENCE_CHAPTERS = [
    {
        "title": "Living Things – Plants",
        "lesson_md": "# Living Things – Plants\n\n## Objectives\n- Identify parts of a plant.\n- Understand the function of roots, stem, leaves, and flowers.\n\n## Plant Parts Diagram (textual)\n- **Roots** – absorb water & nutrients.\n- **Stem** – supports and transports.\n- **Leaves** – photosynthesis.\n- **Flowers** – reproduction.\n\n## Simple Experiment\n*Grow a bean seed in a cotton ball.* Observe root and shoot growth over 7 days.\n\n## Mini‑Game Idea\n**Plant Builder** – Assemble a plant by dragging parts into the correct positions. Earn badges for correct assembly.",
        "quiz_questions": [
            {"question": "What part of the plant absorbs water?", "options": ["Roots", "Leaves", "Stem"], "answer": "Roots"},
            {"question": "Which part is responsible for photosynthesis?", "options": ["Leaves", "Flowers", "Roots"], "answer": "Leaves"}
        ]
    },
    {
        "title": "Matter – Solids, Liquids, Gases",
        "lesson_md": "# Matter – Solids, Liquids, Gases\n\n## Learning Objectives\n- Distinguish between the three states of matter.\n- Identify examples of each state.\n\n## Characteristics\n| State | Shape | Volume | Example |\n|-------|-------|--------|---------|\n| Solid | Fixed | Fixed | Rock |\n| Liquid | Takes shape of container | Fixed | Water |\n| Gas | Takes shape of container | Takes shape of container | Air |\n\n## Simple Activity\n*Observe ice melting into water and then evaporating.*\n\n## Mini‑Game Idea\n**State Switch** – Click on objects to change their state (e.g., ice → water → steam) and earn points.",
        "quiz_questions": [
            {"question": "Which state has a fixed shape and volume?", "options": ["Solid", "Liquid", "Gas"], "answer": "Solid"},
            {"question": "Water in a glass is an example of which state?", "options": ["Liquid", "Solid", "Gas"], "answer": "Liquid"}
        ]
    }
]

async def seed_standard_4(db: AsyncSession):
    """Create subjects, chapters, lessons and quizzes for Grade 4 (CBSE)."""
    # Subjects
    maths = Subject(name="Mathematics", grade_level=4, description="Basic arithmetic, geometry, and data handling.")
    english = Subject(name="English", grade_level=4, description="Reading, grammar and writing skills.")
    science = Subject(name="Science", grade_level=4, description="Living things, matter and basic experiments.")
    db.add_all([maths, english, science])
    await db.flush()  # obtain IDs

    # Helper to add chapters and content
    async def _add_chapters(subject: Subject, chapters_data: list):
        for idx, ch_data in enumerate(chapters_data, start=1):
            chapter = Chapter(
                subject_id=subject.id,
                title=ch_data["title"],
                order_index=idx,
                description="Generated by seed script"
            )
            db.add(chapter)
            await db.flush()
            # Lesson
            await _create_lesson(db, chapter, f"{ch_data['title']} Lesson", ch_data["lesson_md"])
            # Quiz
            await _create_quiz(db, chapter, f"{ch_data['title']} Quiz", ch_data["quiz_questions"])
        await db.commit()

    await _add_chapters(maths, MATHS_CHAPTERS)
    await _add_chapters(english, ENGLISH_CHAPTERS)
    await _add_chapters(science, SCIENCE_CHAPTERS)

    print("✅ Standard 4 curriculum seeded.")

if __name__ == "__main__":
    import asyncio
    from app.core.database import AsyncSessionLocal as async_session
    async def main():
        async with async_session() as db:
            await seed_standard_4(db)
    asyncio.run(main())
