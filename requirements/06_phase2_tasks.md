# Phase 2: AI Content Engine & Student Experience

## Goal
Enable the platform to generate actual educational content using AI and allow students to consume it.

## Task List

### 1. AI Orchestrator Implementation
- [x] **Base Service**: Define abstract `LLMProvider` class.
- [x] **Providers**: Implement `OpenAIProvider` and `MockProvider`.
- [x] **Orchestrator**: Create `AIOrchestrator` to route requests.
- [x] **Prompts**: Create a `PromptManager` to store and version prompts.

### 2. Content Generation API ("The Factory")
- [x] **Curriculum Generation**: API to generate a list of chapters for a given Grade + Subject.
- [x] **Lesson Generation**: API to generate a full lesson (text + quiz) for a specific Chapter.
- [ ] **Streaming**: Implement streaming response for real-time content generation (optional but nice).

### 3. Student Learning Interface
- [x] **Subject View**: Page to see all subjects for the student's grade.
- [x] **Chapter Map**: A visual path of chapters (like a game map).
- [x] **Lesson View**: The actual learning interface (Read -> Quiz -> Result).

### 4. Gamification Logic
- [x] **XP System**: Backend logic to award XP upon lesson completion.
- [x] **Progress Tracking**: Store "Completed" status in DB.
