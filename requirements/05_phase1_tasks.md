# Phase 1: Foundation & Core Content Engine

## Goal
Establish the technical foundation, user management system, and the core "Content Factory" capability. By the end of Phase 1, an admin should be able to generate a lesson using AI, and a student should be able to view it.

## Task List

### 1. Backend Infrastructure & Database
- [x] **Config & DB Setup**: Configure environment variables, SQLAlchemy `session`, and AsyncPG connection.
- [x] **Core Models**: Implement `User`, `Profile` (Parent/Student), `Curriculum` (Grade/Subject/Chapter), and `ContentBlock` models.
- [x] **Migrations**: Initialize Alembic and run the first migration to create tables in Postgres.

### 2. Authentication & User Management
- [x] **Auth API**: Implement Login/Register endpoints (JWT).
- [x] **Profile Management**: APIs for Parents to create/edit Child profiles.
- [x] **Frontend Auth**: Login page and "Select Profile" screen.

### 3. AI Orchestrator (The Engine)
- [ ] **Service Layer**: Create a base `AIService` class.
- [ ] **Integration**: Implement a basic provider (e.g., OpenAI or Mock) to test text generation.
- [ ] **Prompt Templates**: Create the first set of prompts for "Explain Concept" and "Generate Quiz".

### 4. Content Management (The Factory)
- [ ] **Curriculum API**: CRUD endpoints for Grades, Subjects, and Chapters.
- [ ] **Generation Endpoint**: API to trigger AI content generation for a specific Chapter.
- [ ] **Content Storage**: Save generated JSON to the `ContentBlock` table.

### 5. Frontend Core UI
- [ ] **Layouts**: Create `AuthLayout` and `DashboardLayout`.
- [ ] **Parent Dashboard**: View child progress (mock data initially).
- [ ] **Student Dashboard**: View available subjects and chapters.
