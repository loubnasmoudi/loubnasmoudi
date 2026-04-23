from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class PsychographicDimension(BaseModel):
    name: str
    position: int = Field(ge=0, le=100)
    label: str


class PersonaProfile(BaseModel):
    archetype_name: str
    core_truth: str
    identity_summary: str
    psychographic_dimensions: list[PsychographicDimension]
    cultural_tensions: list[str]
    hidden_motivations: list[str]
    daily_rituals: list[str]
    language_codes: dict[str, object]


class PersonaCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    brand_description: str = Field(min_length=10, max_length=4000)
    audience_description: str = Field(min_length=10, max_length=4000)


class ProfileGenerateRequest(BaseModel):
    brand_description: str = Field(min_length=10, max_length=4000)
    audience_description: str = Field(min_length=10, max_length=4000)


class ProfileGenerateResponse(BaseModel):
    profile: PersonaProfile
    generation_ms: int


class PersonaUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    brand_description: str | None = Field(default=None, min_length=10, max_length=4000)
    audience_description: str | None = Field(default=None, min_length=10, max_length=4000)
    profile: PersonaProfile | None = None


class PersonaSummary(BaseModel):
    id: int
    name: str
    archetype_name: str
    core_truth: str
    updated_at: str


class PersonaResponse(BaseModel):
    id: int
    name: str
    brand_description: str
    audience_description: str
    profile: PersonaProfile
    created_at: str
    updated_at: str


class ConversationTurnCreate(BaseModel):
    message: str = Field(min_length=1, max_length=10000)


class SessionMessage(BaseModel):
    role: str
    content: str
    tone: str | None = None
    created_at: str


class SessionResponse(BaseModel):
    id: int
    persona_id: int
    created_at: str
    updated_at: str
    messages: list[SessionMessage]


class SessionSummary(BaseModel):
    key_themes: list[str]
    surprises: list[str]
    followup_questions: list[str]
    disclaimer: str
    final_reflection: str


class SessionSummaryResponse(BaseModel):
    summary: SessionSummary


class ScenarioCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    context: str = Field(min_length=5, max_length=4000)
    artifact_text: str = Field(default="", max_length=10000)


class ScenarioReaction(BaseModel):
    initial_gut_feeling: str
    specific_objections: list[str]
    what_needs_to_change: list[str]
    likelihood_to_act: int = Field(ge=1, le=10)
    reasoning: str


class ScenarioResultResponse(BaseModel):
    id: int
    persona_id: int
    title: str
    context: str
    artifact_text: str
    reaction: ScenarioReaction
    created_at: str
