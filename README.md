# Learnivo - AI Powered Learning Platform

## Project Structure
- **backend/**: FastAPI application (Python 3.11).
- **frontend/**: Vue 3 + Vite application.
- **requirements/**: Detailed project documentation and specs.
- **docker-compose.yml**: Orchestration for Database (Postgres) and Cache (Redis).

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Node.js (v18+)
- Python 3.11+

### Running the Project

1.  **Start Infrastructure (DB + Redis)**
    ```bash
    docker-compose up -d db redis
    ```

2.  **Backend Setup**
    ```bash
    cd backend
    pip install -r requirements.txt
    uvicorn app.main:app --reload
    ```
    *API will be available at http://localhost:8000*

3.  **Frontend Setup**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```
    *UI will be available at http://localhost:5173*

## Documentation
See the `requirements/` folder for:
- `01_project_overview.md`: Vision & Tech Stack.
- `02_feature_spec.md`: Detailed feature breakdown.
- `03_technical_architecture.md`: System design & AI strategy.
- `04_ui_ux_guidelines.md`: Design system.