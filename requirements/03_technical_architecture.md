# Technical Architecture & Data Strategy

## System Architecture Diagram (Conceptual)

```mermaid
graph TD
    Client[Vue.js Frontend] --> API[FastAPI Gateway]
    API --> Auth[Auth Service (JWT)]
    API --> Content[Content Engine]
    API --> Analytics[Analytics Service]
    
    Content --> Orchestrator[AI Orchestrator]
    Orchestrator --> GPT[OpenAI API]
    Orchestrator --> Gem[Gemini API]
    Orchestrator --> Local[Local LLM / Ollama]
    
    Content --> DB[(PostgreSQL)]
    Analytics --> Parquet[(Parquet Files / S3)]
    
    DB --> Redis[(Redis Cache)]
```

## Database Schema Strategy (PostgreSQL)

### Core Tables
- `users` (id, email, role, password_hash)
- `profiles` (id, parent_id, display_name, avatar_config, current_grade)
- `curriculum` (id, grade, subject, chapter_name, order_index)
- `content_blocks` (id, chapter_id, type, content_json, ai_model_used)
- `questions` (id, content_block_id, question_text, options, correct_answer, difficulty)
- `student_progress` (profile_id, content_id, status, score, completed_at)

## High-Volume Data Strategy (Parquet)

We will use Parquet for immutable, high-volume data that doesn't require frequent row-level updates but requires fast analytical querying.

**Use Case 1: Interaction Logs**
Instead of cluttering Postgres with every single click:
- Buffer events in Redis.
- Periodically flush to Parquet files partitioned by `date` and `student_id`.
- *Schema*: `timestamp`, `profile_id`, `event_type` (click, answer, view), `metadata` (json).

**Use Case 2: AI Generation History**
Keep a record of every prompt sent to AI and the raw response for auditing and fine-tuning.
- *Schema*: `request_id`, `prompt`, `model_name`, `raw_response`, `cost`, `timestamp`.

## AI Orchestration Logic
The backend will implement a Strategy Pattern for AI generation:

1.  **Prompt Template**: "Explain {topic} to a {grade} grader using {analogy}."
2.  **Model Selection**:
    - Configurable via Admin Panel.
    - Example: Use Local LLM for generating multiple choice distractors (cheap). Use GPT-4 for explaining complex physics concepts (high quality).
3.  **Fallback**: If Gemini API fails, auto-retry with OpenAI.

## Grading Engine
- **Objective**: MCQs graded instantly.
- **Subjective**: Short answer questions sent to LLM for grading.
    - Prompt: "Grade this answer: '{student_answer}' for question '{question}'. Give score 0-10 and constructive feedback."
