from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from .schemas import (
    PersonaProfile,
    PersonaResponse,
    PersonaSummary,
    ScenarioResultResponse,
    SessionMessage,
    SessionResponse,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Storage:
    def __init__(self, db_path: Path | None = None) -> None:
        self.db_path = db_path or Path(__file__).resolve().parent.parent / "data" / "empathy_simulator.db"
        self._ensure_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_db(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS personas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    brand_description TEXT NOT NULL,
                    audience_description TEXT NOT NULL,
                    profile_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    persona_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    messages_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (persona_id) REFERENCES personas(id)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS scenarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    persona_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    context TEXT NOT NULL,
                    artifact_text TEXT NOT NULL DEFAULT '',
                    reaction_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (persona_id) REFERENCES personas(id)
                )
                """
            )
            conn.commit()

    @staticmethod
    def _row_to_persona(row: sqlite3.Row) -> PersonaResponse:
        return PersonaResponse(
            id=row["id"],
            name=row["name"],
            brand_description=row["brand_description"],
            audience_description=row["audience_description"],
            profile=PersonaProfile(**json.loads(row["profile_json"])),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    @staticmethod
    def _row_to_session(row: sqlite3.Row) -> SessionResponse:
        payload = json.loads(row["messages_json"])
        messages = [SessionMessage(**msg) for msg in payload]
        return SessionResponse(
            id=row["id"],
            persona_id=row["persona_id"],
            title=row["title"],
            messages=messages,
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    @staticmethod
    def _row_to_scenario(row: sqlite3.Row) -> ScenarioResultResponse:
        reaction = json.loads(row["reaction_json"])
        return ScenarioResultResponse(
            id=row["id"],
            persona_id=row["persona_id"],
            title=row["title"],
            context=row["context"],
            artifact_text=row["artifact_text"],
            reaction=reaction,
            created_at=row["created_at"],
        )

    def create_persona(
        self,
        *,
        name: str,
        brand_description: str,
        audience_description: str,
        profile: dict,
    ) -> int:
        now = utc_now()
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO personas (name, brand_description, audience_description, profile_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (name, brand_description, audience_description, json.dumps(profile), now, now),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def update_persona(
        self,
        *,
        persona_id: int,
        name: str,
        brand_description: str,
        audience_description: str,
        profile: dict,
    ) -> None:
        now = utc_now()
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE personas
                SET name = ?, brand_description = ?, audience_description = ?, profile_json = ?, updated_at = ?
                WHERE id = ?
                """,
                (name, brand_description, audience_description, json.dumps(profile), now, persona_id),
            )
            conn.commit()

    def get_persona(self, persona_id: int) -> PersonaResponse | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM personas WHERE id = ?", (persona_id,)).fetchone()
            if not row:
                return None
            return self._row_to_persona(row)

    def list_personas(self) -> list[PersonaSummary]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM personas ORDER BY updated_at DESC").fetchall()
            return [
                PersonaSummary(
                    id=row["id"],
                    name=row["name"],
                    archetype_name=json.loads(row["profile_json"]).get("archetype_name", "Unknown"),
                    core_truth=json.loads(row["profile_json"]).get("core_truth", ""),
                    updated_at=row["updated_at"],
                )
                for row in rows
            ]

    def create_session(self, persona_id: int) -> int:
        now = utc_now()
        title = f"Session {now[:19]}"
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO sessions (persona_id, title, messages_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (persona_id, title, json.dumps([]), now, now),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def get_session(self, session_id: int) -> SessionResponse | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
            if not row:
                return None
            return self._row_to_session(row)

    def add_message(self, *, session_id: int, role: str, content: str, tone: str | None = None) -> None:
        session = self.get_session(session_id)
        if not session:
            raise ValueError("Session not found.")
        messages = [m.model_dump() for m in session.messages]
        messages.append({"role": role, "content": content, "tone": tone, "created_at": utc_now()})
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE sessions
                SET messages_json = ?, updated_at = ?
                WHERE id = ?
                """,
                (json.dumps(messages), utc_now(), session_id),
            )
            conn.commit()

    def create_scenario(self, *, persona_id: int, title: str, context: str, artifact_text: str, reaction: dict) -> int:
        now = utc_now()
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO scenarios (persona_id, title, context, artifact_text, reaction_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (persona_id, title, context, artifact_text, json.dumps(reaction), now),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def get_scenario(self, scenario_id: int) -> ScenarioResultResponse:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM scenarios WHERE id = ?", (scenario_id,)).fetchone()
            if not row:
                raise ValueError("Scenario not found.")
            return self._row_to_scenario(row)

    def export_session_markdown(self, *, session: SessionResponse, persona: PersonaResponse) -> str:
        lines = [
            "# Empathy Simulator Transcript",
            "",
            "> Disclaimer: This is a simulated perspective, not validated research.",
            "",
            f"**Persona:** {persona.name}",
            f"**Archetype:** {persona.profile.archetype_name}",
            "",
            "## Conversation",
            "",
        ]
        for message in session.messages:
            tone_part = f" _(tone: {message.tone})_" if message.tone else ""
            lines.append(f"- **{message.role}**{tone_part}: {message.content}")
        return "\n".join(lines) + "\n"
