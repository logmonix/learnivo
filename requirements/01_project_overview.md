# Project Overview: AI-Powered Learning Platform

## Vision
To create an engaging, AI-driven learning platform that bridges the gap between daily casual learning (vocabulary, brain teasers) and structured academic curriculum (grades, subjects, chapters). The platform will serve students, parents, and administrators with a focus on personalization and gamification.

## Core Philosophy
- **Fun First**: Learning should feel like a game, not a chore.
- **AI-Native**: AI is not an add-on; it is the engine generating content, grading assessments, and guiding the student.
- **Data-Driven**: Heavy usage of analytics to track progress and adapt to the student's pace.

## Technology Stack Selection

### Backend: Python (FastAPI)
- **Why FastAPI?**: You requested Python. FastAPI is superior to Django/Flask for this use case because of its native asynchronous support. When querying multiple AIs (Gemini, OpenAI, Local LLM) simultaneously, async allows the server to handle thousands of requests without blocking.
- **AI Integration**: LangChain or a custom orchestration layer to manage prompts and fallback logic between models.

### Frontend: Vue.js 3 + Vite
- **Why Vue?**: Excellent reactivity system, easy to learn, and highly performant.
- **State Management**: Pinia.
- **Styling**: TailwindCSS (highly recommended for rapid, custom designs) or custom CSS for unique "kid-friendly" themes.

### Database & Storage
- **Primary DB**: PostgreSQL. Handles user data, relationships, curriculum structure, and transactional records.
- **Big Data**: Parquet. Used for storing:
    - Detailed interaction logs (every click, every answer).
    - Generated content archives (to avoid regenerating same content).
    - Analytics data for ML training.
- **Caching**: Redis. Essential for caching AI responses and managing user sessions.

### AI Infrastructure
- **Orchestrator**: A service that decides which model to call based on cost/complexity.
    - *Simple Query*: Local LLM (Llama 3 / Mistral via Ollama).
    - *Complex Reasoning/Math*: GPT-4o or Gemini Pro.
    - *Creative Writing*: Claude or GPT.

## User Roles
1.  **Super Admin**: System configuration, AI model management.
2.  **Content Admin**: Generates and curates curriculum content.
3.  **Parent**: Manages subscription, views reports, creates child profiles.
4.  **Student**: The learner (Gamified interface).
