# Empathy Simulator MVP

An AI-powered conversational rehearsal tool that lets brand teams talk to their audience before they talk to their audience.

## Features in this MVP

- Persona generation from brand and audience descriptions
- Editable and saved personas (SQLite-backed)
- Conversation mode with:
  - tone tags per response
  - persistent persona context panel
  - provocation prompts every 5 user turns
- Scenario testing with structured reaction output
- Session summary generation
- Transcript export in Markdown format
- Visible simulation disclaimers in UI and exports

## Tech stack

- Backend: FastAPI + SQLite
- Frontend: Vanilla HTML/CSS/JavaScript served as static files

## Run locally

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the app:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. Open:

   ```text
   http://localhost:8000
   ```

## API overview

- `POST /api/personas` - create persona from brand + audience text
- `GET /api/personas` - list personas
- `GET /api/personas/{persona_id}` - fetch one persona
- `PUT /api/personas/{persona_id}` - regenerate persona from updated text
- `POST /api/sessions/{persona_id}` - create conversation session
- `GET /api/sessions/{session_id}` - fetch session + messages
- `POST /api/sessions/{session_id}/turns` - send one user turn and get persona reply
- `GET /api/sessions/{session_id}/summary` - generate session summary
- `GET /api/sessions/{session_id}/export` - export transcript markdown
- `POST /api/scenarios/{persona_id}` - run scenario reaction
