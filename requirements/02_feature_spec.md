# Feature Specifications

## 1. Student Experience (The "Game")

### Daily Learning (Micro-learning)
- **Daily Mix**: A generated set of 5-10 minute tasks covering Vocabulary, Grammar, Mental Math, and General Knowledge.
- **Streak System**: Rewards for logging in and learning consecutive days.
- **Gamification**:
    - **XP & Levels**: Earn XP for every correct answer.
    - **Currency (Star Coins)**: Earn coins to buy virtual items (hats, outfits) for their Avatar.
    - **Badges**: Achievements for milestones (e.g., "Math Whiz", "Early Bird").

### Classroom Learning (Structured)
- **Curriculum Map**: Visual journey map (like Candy Crush levels) for chapters.
- **AI Tutor**: A chat interface where students can ask "Why is this answer wrong?" and get a kid-friendly explanation.
- **Modes**:
    - *Learn*: Read/Watch generated content.
    - *Practice*: AI-generated quizzes.
    - *Exam*: Timed assessments.

## 2. Parent Portal
- **Multi-Profile Management**: Single login for parent, switch between kid profiles.
- **Dashboard**:
    - "Weakness vs Strength" radar charts.
    - Time spent breakdown.
    - Curriculum progress.
- **Controls**: Set daily goals or time limits.

## 3. Admin & Content Generation (The "Factory")
- **Content Wizard**:
    - Input: Grade (e.g., 5th), Subject (Math), Chapter (Fractions).
    - Action: "Generate Explainer", "Generate 20 MCQs", "Generate Word Problems".
    - AI Selector: Choose which AI model generates this batch.
- **Review System**: Human-in-the-loop interface to approve/edit AI content before publishing.
- **Syllabus Manager**: Define the tree structure of Standard -> Subject -> Unit -> Chapter.

## 4. Advanced Features (Robustness Extensions)
- **Adaptive Difficulty**: If a student fails a quiz, the system automatically generates a remedial lesson and simpler questions.
- **Voice Interaction**:
    - Text-to-Speech (TTS) for reading questions to younger kids.
    - Speech-to-Text (STT) for practicing pronunciation or answering orally.
- **Offline Support (PWA)**: Allow downloading a chapter for offline learning (syncs when back online).
- **Peer Battle (Optional)**: Real-time math duel against a friend (or bot).
