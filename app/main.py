from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from .engine import (
    build_persona_profile,
    build_session_summary,
    generate_persona_reply,
    run_scenario_reaction,
)
from .schemas import (
    ConversationTurnCreate,
    PersonaCreate,
    PersonaResponse,
    PersonaSummary,
    ScenarioCreate,
    ScenarioResultResponse,
    SessionResponse,
    SessionSummaryResponse,
)
from .storage import Storage

APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR.parent / "static"

app = FastAPI(
    title="Empathy Simulator MVP",
    description="A conversational rehearsal tool for brand teams.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

storage = Storage()

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def root() -> FileResponse:
    index = STATIC_DIR / "index.html"
    if not index.exists():
        raise HTTPException(status_code=404, detail="Frontend not found.")
    return FileResponse(index)


@app.post("/api/personas", response_model=PersonaResponse)
def create_persona(payload: PersonaCreate) -> PersonaResponse:
    profile = build_persona_profile(payload.brand_description, payload.audience_description)
    persona_id = storage.create_persona(
        name=payload.name.strip(),
        brand_description=payload.brand_description,
        audience_description=payload.audience_description,
        profile=profile.model_dump(),
    )
    return storage.get_persona(persona_id)


@app.get("/api/personas", response_model=list[PersonaSummary])
def list_personas() -> list[PersonaSummary]:
    return storage.list_personas()


@app.get("/api/personas/{persona_id}", response_model=PersonaResponse)
def get_persona(persona_id: int) -> PersonaResponse:
    persona = storage.get_persona(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found.")
    return persona


@app.put("/api/personas/{persona_id}", response_model=PersonaResponse)
def update_persona(persona_id: int, payload: PersonaCreate) -> PersonaResponse:
    existing = storage.get_persona(persona_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Persona not found.")

    profile = build_persona_profile(payload.brand_description, payload.audience_description)
    storage.update_persona(
        persona_id=persona_id,
        name=payload.name.strip(),
        brand_description=payload.brand_description,
        audience_description=payload.audience_description,
        profile=profile.model_dump(),
    )
    updated = storage.get_persona(persona_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Persona not found after update.")
    return updated


@app.post("/api/sessions/{persona_id}", response_model=SessionResponse)
def create_session(persona_id: int) -> SessionResponse:
    persona = storage.get_persona(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found.")
    session_id = storage.create_session(persona_id)
    session = storage.get_session(session_id)
    if not session:
        raise HTTPException(status_code=500, detail="Unable to create session.")
    return session


@app.get("/api/sessions/{session_id}", response_model=SessionResponse)
def get_session(session_id: int) -> SessionResponse:
    session = storage.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return session


@app.post("/api/sessions/{session_id}/turns", response_model=SessionResponse)
def add_turn(session_id: int, payload: ConversationTurnCreate) -> SessionResponse:
    session = storage.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    persona = storage.get_persona(session.persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found.")

    user_message = payload.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    storage.add_message(
        session_id=session_id,
        role="user",
        content=user_message,
    )
    updated_session = storage.get_session(session_id)
    if not updated_session:
        raise HTTPException(status_code=500, detail="Session not found after write.")

    user_turn_count = len([m for m in updated_session.messages if m.role == "user"])
    if user_turn_count >= 50:
        reply = "I'm at the edge of this conversation's memory. Let's start a fresh session and keep pressure-testing from a clean slate."
        tone = "cautious"
        provocation = None
    else:
        reply, tone, provocation = generate_persona_reply(persona.profile, updated_session.messages, user_message)

    storage.add_message(
        session_id=session_id,
        role="assistant",
        content=reply,
        tone=tone,
    )

    refreshed = storage.get_session(session_id)
    if not refreshed:
        raise HTTPException(status_code=500, detail="Session not found after reply.")

    if provocation:
        storage.add_message(
            session_id=session_id,
            role="provocation",
            content=provocation,
            tone="challenging",
        )

    final_session = storage.get_session(session_id)
    if not final_session:
        raise HTTPException(status_code=500, detail="Session not found after provocation.")
    return final_session


@app.get("/api/sessions/{session_id}/summary", response_model=SessionSummaryResponse)
def session_summary(session_id: int) -> SessionSummaryResponse:
    session = storage.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    persona = storage.get_persona(session.persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found.")
    summary = build_session_summary(persona.profile, session.messages)
    return SessionSummaryResponse(summary=summary)


@app.get("/api/sessions/{session_id}/export", response_class=PlainTextResponse)
def export_session_markdown(session_id: int) -> str:
    session = storage.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    persona = storage.get_persona(session.persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found.")
    return storage.export_session_markdown(session=session, persona=persona)


@app.post("/api/scenarios/{persona_id}", response_model=ScenarioResultResponse)
def run_scenario(persona_id: int, payload: ScenarioCreate) -> ScenarioResultResponse:
    persona = storage.get_persona(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found.")
    reaction = run_scenario_reaction(persona.profile, payload)
    scenario_id = storage.create_scenario(
        persona_id=persona_id,
        title=payload.title.strip() or "Untitled Scenario",
        context=payload.context,
        artifact_text=payload.artifact_text,
        reaction=reaction.model_dump(),
    )
    return storage.get_scenario(scenario_id)
