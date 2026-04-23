from __future__ import annotations

import json
import textwrap
from datetime import datetime, timezone

from .schemas import PersonaProfile, ScenarioCreate, ScenarioReaction, SessionMessage, SessionSummary


def _now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def _fit(values: list[str], total: int, fallback: str) -> list[str]:
    safe = [v.strip() for v in values if v and v.strip()]
    while len(safe) < total:
        safe.append(fallback)
    return safe[:total]


def _infer_tone(text: str) -> str:
    lowered = text.lower()
    if any(word in lowered for word in ["trust", "proof", "evidence", "data"]):
        return "skeptical"
    if any(word in lowered for word in ["love", "great", "excited", "amazing"]):
        return "warm"
    if any(word in lowered for word in ["price", "cost", "expensive", "cheap"]):
        return "defensive"
    if "?" in lowered or any(word in lowered for word in ["why", "how", "what if"]):
        return "intrigued"
    return "measured"


def build_persona_profile(brand_description: str, audience_description: str) -> PersonaProfile:
    brand = (brand_description or "a brand").strip()
    audience = (audience_description or "an audience").strip()
    audience_key = audience.split()[0].capitalize() if audience.split() else "Audience"

    return PersonaProfile(
        archetype_name=f"The {audience_key} Realist",
        core_truth=f"I reward brands that reduce emotional overhead. If {brand[:80].lower()} feels performative, I tune out.",
        identity_summary=f"This persona represents {audience[:140].lower()}. They prefer practical outcomes over polished promises.",
        psychographic_dimensions=[
            {"name": "Risk tolerance", "position": 40, "label": "Cautiously experimental"},
            {"name": "Identity expression", "position": 72, "label": "Signals values through choices"},
            {"name": "Trust posture", "position": 30, "label": "Skeptical until proven"},
            {"name": "Decision speed", "position": 57, "label": "Fast once confidence exists"},
            {"name": "Community orientation", "position": 68, "label": "Checks social proof"},
        ],
        cultural_tensions=_fit(
            [
                "Wants convenience but worries about losing control.",
                "Values ethics but defaults to easiest option under stress.",
                "Claims independence while still checking peer consensus.",
            ],
            3,
            "Balances aspiration with practical constraints.",
        ),
        hidden_motivations=_fit(
            [
                "Protect personal time and attention.",
                "Feel competent and in control.",
                "Avoid regret from poor choices.",
                "Belong to trusted communities.",
            ],
            4,
            "Reduce unnecessary risk.",
        ),
        daily_rituals=_fit(
            [
                "Scans reviews before trying something new.",
                "Compares alternatives in short mobile sessions.",
                "Saves options and revisits later.",
                "Checks one trusted source before committing.",
            ],
            4,
            "Pressure-tests choices with quick checks.",
        ),
        language_codes={
            "vocabulary": ["worth it", "show me", "feels off", "don't overhype it"],
            "tone": ["direct", "reflective", "slightly skeptical"],
            "phrases": ["My gut says...", "If you can prove it...", "I might be in if..."],
            "avoid": ["world-class", "revolutionary", "best-in-class"],
        },
    )


def generate_persona_reply(
    profile: PersonaProfile,
    messages: list[SessionMessage],
    user_message: str,
) -> tuple[str, str, str | None]:
    tone = _infer_tone(user_message)
    vocab = profile.language_codes.get("vocabulary", ["show me"])
    phrase = profile.language_codes.get("phrases", ["My gut says..."])[0]
    tension = profile.cultural_tensions[len(messages) % len(profile.cultural_tensions)]
    motivation = profile.hidden_motivations[len(messages) % len(profile.hidden_motivations)]
    response = textwrap.dedent(
        f"""\
        {phrase} {vocab[0]}.
        On "{user_message[:180]}", I'd probably ask for clearer proof and fewer polished claims.
        I care about this tension: {tension.lower()}
        If your direction helps me {motivation.lower()}, I lean in. If not, I keep scrolling.
        """
    ).strip()
    user_turn_count = len([m for m in messages if m.role == "user"])
    provocation = generate_provocation(profile, messages) if user_turn_count > 0 and user_turn_count % 5 == 0 else None
    return response, tone, provocation


def generate_provocation(profile: PersonaProfile, messages: list[SessionMessage]) -> str:
    idx = len(messages) % len(profile.cultural_tensions)
    tension = profile.cultural_tensions[idx]
    return (
        "Provocation: You're optimizing for internal clarity, not audience risk. "
        f"How does your message address this tension: {tension.lower()}?"
    )


def build_session_summary(profile: PersonaProfile, messages: list[SessionMessage]) -> SessionSummary:
    user_messages = [m.content for m in messages if m.role == "user"]
    assistant_count = len([m for m in messages if m.role == "assistant"])
    latest_user = user_messages[-1] if user_messages else "No user prompt captured."
    return SessionSummary(
        key_themes=[
            "Trust is conditional on concrete proof and reduced effort.",
            "Over-polished language increases skepticism.",
            "Clear tradeoffs perform better than broad claims.",
        ],
        surprises=[
            "Positive tone appeared only when evidence was explicit.",
            "Friction signals triggered quick disengagement.",
        ],
        followup_questions=[
            "Which exact claims need validation in live interviews?",
            "What language currently sounds performative to this audience?",
            "Where does our message increase emotional overhead?",
        ],
        disclaimer=(
            "This is a simulated perspective grounded in psychographic hypotheses and does not replace real human research."
        ),
        final_reflection=f'Latest prompt: "{latest_user[:180]}" | Assistant turns: {assistant_count} | Archetype: {profile.archetype_name}',
    )


def run_scenario_reaction(profile: PersonaProfile, scenario: ScenarioCreate) -> ScenarioReaction:
    combined = f"{scenario.title} {scenario.context} {scenario.artifact_text}".lower()
    score = 6
    if any(token in combined for token in ["free trial", "transparent pricing", "guarantee", "social proof"]):
        score = 8
    elif any(token in combined for token in ["exclusive", "luxury", "premium", "limited edition"]):
        score = 4

    return ScenarioReaction(
        initial_gut_feeling="Cautiously interested, but still scanning for proof.",
        specific_objections=[
            "I cannot yet tell why this is better than my current option.",
            "The language sounds polished, but I need practical upside now.",
        ],
        what_needs_to_change=[
            "Add concrete outcomes or evidence with specifics.",
            "Reduce cognitive load and make the next step obvious.",
        ],
        likelihood_to_act=score,
        reasoning=(
            "Likelihood is driven by trust posture and convenience needs. "
            "When confidence rises and effort falls, action intent increases."
        ),
    )


def export_transcript_markdown(
    persona_name: str,
    profile: PersonaProfile,
    messages: list[SessionMessage],
    summary: SessionSummary,
) -> str:
    lines = [
        "# Empathy Simulator Transcript",
        "",
        f"**Persona:** {persona_name}",
        f"**Generated:** {_now_iso()}",
        "",
        "> Disclaimer: This is a simulated perspective, not validated research.",
        "",
        "## Persona Snapshot",
        f"- **Archetype:** {profile.archetype_name}",
        f"- **Core truth:** {profile.core_truth}",
        f"- **Identity summary:** {profile.identity_summary}",
        "",
        "## Conversation",
    ]
    for m in messages:
        tone = f" _(tone: {m.tone})_" if m.tone else ""
        lines.append(f"- **{m.role}**{tone}: {m.content}")
    lines.extend(
        [
            "",
            "## Session Summary",
            "",
            "### Key themes",
            *[f"- {x}" for x in summary.key_themes],
            "",
            "### Surprises",
            *[f"- {x}" for x in summary.surprises],
            "",
            "### Recommended follow-up questions",
            *[f"- {x}" for x in summary.followup_questions],
            "",
            f"> {summary.disclaimer}",
            "",
            f"_Reflection: {summary.final_reflection}_",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def profile_to_json(profile: PersonaProfile) -> str:
    return json.dumps(profile.model_dump(), indent=2, ensure_ascii=True)
