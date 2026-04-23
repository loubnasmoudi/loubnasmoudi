# Product Requirements Document: Empathy Simulator

An AI-powered conversational tool that lets brand teams talk to their audience before they talk to their audience.

## Document Metadata

| Field | Value |
| --- | --- |
| Status | Draft |
| Version | 1.0 |
| Date | April 2026 |
| Author | Lulu - Product Design Engineering |
| Stakeholders | Brand Strategy, UX Research, Engineering, Client Services |

## 1. Overview

The Empathy Simulator is a conversational AI tool that lets brand teams interact with a synthetic audience persona grounded in deep psychographic profiling. Instead of guessing how their audience might react to messaging, campaigns, or product decisions, teams can ask questions and receive responses that reflect real human tensions, motivations, and cultural context.

This is not a chatbot. It is a rehearsal space - a way to pressure-test assumptions before investing in expensive qualitative research, and a way to build empathy muscles across teams who rarely talk to end users directly.

## 2. Problem Statement

### 2.1 The Gap

Most brand teams operate on a thin understanding of their audience. They have demographic data, maybe a survey, maybe a set of personas created two years ago. When it comes time to make a decision - what to say, how to position, where to show up - they rely on instinct filtered through internal consensus.

The result: messaging that sounds like the brand talking to itself. Campaigns that optimize for what leadership likes, not what the audience feels. Product decisions made in a vacuum of real human context.

### 2.2 Why This Matters Now

- The cost of getting messaging wrong is rising as channels fragment and attention shrinks.
- Qualitative research is slow (4-8 weeks) and expensive ($15-50K per round).
- AI has reached the point where psychographic simulation is credible enough to be useful as a starting input - not a replacement for research, but a complement that sits upstream of it.
- Teams need empathy tools that are fast enough to use in the flow of work, not just in quarterly planning cycles.

## 3. Product Vision

Give every brand team the ability to sit across from their audience and ask the hard questions - anytime, without scheduling a focus group.

Core principles:

- **Grounded, not generic.** Every response is anchored to a specific psychographic profile - cultural tensions, hidden motivations, language codes, and behavioral patterns. No generic "millennial consumer" responses.
- **Rehearsal, not replacement.** This tool is explicitly positioned as practice for real conversations. It sharpens the questions teams ask before they go talk to actual humans.
- **Provocative, not validating.** The simulator should challenge assumptions, not confirm them. If the team walks away comfortable, the tool has failed.
- **Fast enough for Tuesday.** Usable in a working session, not just a strategy offsite. Generate a persona and start talking in under 60 seconds.

## 4. Target Users

### 4.1 Primary: Brand Strategists and Planners

People who write briefs, develop positioning, and craft messaging frameworks. They need to internalize the audience perspective before they can articulate it.

Current workflow: read research decks, make assumptions, get feedback too late.

### 4.2 Secondary: Creative Teams

Copywriters, art directors, content strategists. They need a gut-check on tone, language, and framing before they present work.

Current workflow: write, present to internal stakeholders, get subjective feedback that reflects the room - not the audience.

### 4.3 Tertiary: Client-Facing Consultants

People who need to demonstrate audience understanding in pitches, workshops, and strategy sessions. They need a tool that makes the audience feel real and present in the room.

## 5. User Stories and Functional Requirements

### 5.1 Persona Generation

As a strategist, I want to describe my audience in plain language and have the system generate a rich psychographic profile, so that I have a grounded foundation for conversation.

| ID | Requirement | Priority | Status |
| --- | --- | --- | --- |
| FR-01 | User can input brand/product description and audience description in free-text fields | P0 | Planned |
| FR-02 | System generates a psychographic profile including: audience archetype name, core truth, identity summary, 5 psychographic dimensions with spectrum positions, 3 cultural tensions, 4 hidden motivations, 4 daily rituals, and language codes | P0 | Planned |
| FR-03 | Profile generation completes in under 15 seconds | P0 | Planned |
| FR-04 | User can save, name, and recall generated profiles | P1 | Planned |
| FR-05 | User can manually edit or refine any dimension of the generated profile before entering conversation mode | P1 | Planned |

### 5.2 Conversation Mode

As a brand team member, I want to ask the simulated persona questions and receive responses that reflect their psychographic profile, so that I can pressure-test messaging and build intuition.

| ID | Requirement | Priority | Status |
| --- | --- | --- | --- |
| FR-06 | User can enter a conversational interface where the AI responds as the generated persona | P0 | Planned |
| FR-07 | Responses reflect the persona's language codes (vocabulary, tone), cultural tensions, and motivations - not generic consumer language | P0 | Planned |
| FR-08 | User can paste ad copy, landing page text, or email drafts and ask "What do you think of this?" - persona responds with specific emotional and linguistic feedback | P0 | Planned |
| FR-09 | Conversation maintains context across turns (up to 50 messages per session) | P0 | Planned |
| FR-10 | User can ask meta-questions: "What would make you trust this brand?" "What would make you unsubscribe?" "Why did you choose the competitor?" | P0 | Planned |
| FR-11 | System surfaces a "provocation" after every 5 messages - an unsolicited challenge to an assumption the user seems to be making | P1 | Planned |
| FR-12 | Conversation can be exported as a transcript (PDF or Markdown) | P1 | Planned |

### 5.3 Scenario Testing

As a strategist, I want to run structured scenarios (for example, "Show this persona our new pricing page") and see how the persona reacts across multiple dimensions.

| ID | Requirement | Priority | Status |
| --- | --- | --- | --- |
| FR-13 | User can create a "Scenario": a structured prompt with context (for example, "You just saw this Instagram ad for the first time") | P1 | Planned |
| FR-14 | System responds with a structured reaction: initial gut feeling, specific objections, what would need to change, likelihood to act (1-10 with reasoning) | P1 | Planned |
| FR-15 | User can run the same scenario across multiple saved personas to compare reactions side-by-side | P2 | Planned |

## 6. Information Architecture and Key Screens

### 6.1 Screen Map

- Home / Dashboard - saved personas, recent sessions, quick-start
- Persona Builder - brand and audience input, profile generation, editable profile view
- Conversation Mode - chat interface with persona context panel visible alongside
- Scenario Runner - structured input, multi-dimensional reaction output
- Comparison View (P2) - same scenario, multiple personas, side-by-side
- Session Library - searchable archive of past conversations and scenarios

### 6.2 Conversation Mode - UX Detail

The conversation interface is the core of the product. It is not a standard chatbot. Key design requirements:

- **Persistent context panel:** The persona's profile (archetype name, core truth, key tensions, language codes) remains visible in a sidebar throughout the conversation. This prevents the "who am I talking to?" problem.
- **Tone indicators:** Each response includes a subtle emotional tone tag (for example, skeptical, intrigued, defensive, warm) so the user can read the room.
- **Provocation moments:** Every 5 messages, the system interjects with a challenge card - visually distinct from the conversation flow - that pushes back on an assumption.
- **Copy-paste zone:** A dedicated area where users can paste creative work (ad copy, subject lines, product descriptions) for the persona to react to, separate from the conversational flow.
- **Session summary:** At the end of a session (or on demand), the system generates a summary of key themes, surprises, and recommended follow-up questions for real research.

## 7. Non-Functional Requirements

| Category | Requirement |
| --- | --- |
| Performance | Persona generation < 15s. Conversation responses < 5s. Scenario reactions < 10s. |
| Scalability | Support 50 concurrent users at launch, scaling to 500 within 6 months. |
| Data privacy | No user-inputted brand strategy data is used for model training. All sessions encrypted at rest and in transit. SOC 2 Type II compliance required for enterprise clients. |
| Accuracy | Responses must be psychographically consistent within a session. Contradiction rate < 5% across a 50-message conversation. |
| Accessibility | WCAG 2.1 AA. Full keyboard navigation. Screen reader support for conversation mode. |

## 8. Technical Architecture

### 8.1 AI Layer

The system uses a two-stage AI pipeline:

- **Stage 1 - Profile Generation:** A structured prompt generates the full psychographic profile as JSON. Model: Claude Sonnet (optimized for speed and structure). Output is validated against a schema before display.
- **Stage 2 - Conversation Engine:** The generated profile is injected as a system prompt for the conversation. The persona's language codes, tensions, and motivations are encoded as behavioral constraints. Model: Claude Sonnet with temperature 0.7 for natural variation.

Key technical decisions:

- Conversation context is maintained via full message history (not summarization) to preserve psychographic consistency.
- Provocation generation runs as a parallel process every 5 turns, analyzing the conversation for unstated assumptions.
- Scenario reactions use structured output (JSON) to ensure consistent multi-dimensional scoring.

### 8.2 Data Model

Core entities: Workspace, Persona (profile JSON + metadata), Session (conversation history + metadata), Scenario (structured input + reactions), User (auth + preferences).

### 8.3 Integration Points

- Authentication: SSO via enterprise identity providers (Okta, Azure AD)
- Export: PDF/Markdown transcript generation, Slack integration for sharing insights
- Future: Integration with the Audience Insight Engine for profile import, Google Drive for document ingestion in copy-paste zone

## 9. Guardrails and Ethical Considerations

This tool simulates audience perspective. It does not replace real human research. The following guardrails are non-negotiable:

- **Visible disclaimers:** Every session begins and ends with a reminder that this is a simulated perspective, not validated research. The summary export includes this disclaimer prominently.
- **No demographic stereotyping:** The system must never reduce people to demographic cliches. Responses are grounded in psychographic dimensions, not assumptions about race, gender, age, or income.
- **Contradiction surfacing:** If the user's questions push the persona into territory not covered by the profile, the system should say "I'm not sure - this is where you'd want to ask a real person" rather than hallucinate.
- **No false confidence:** Responses should use hedging language ("I'd probably...", "My gut says...") rather than authoritative declarations. The persona is a hypothesis, not a source of truth.
- **Bias audit:** Quarterly review of generated personas and responses for systemic bias patterns, conducted by an external ethics reviewer.

## 10. Success Metrics

| Metric | Target (3 months) | Target (12 months) |
| --- | --- | --- |
| Sessions per user per week | 2+ | 4+ |
| Avg. conversation length | 12+ messages | 20+ messages |
| Transcript export rate | 30% of sessions | 50% of sessions |
| User-reported insight quality (1-5) | 3.5+ | 4.0+ |
| "Changed my approach" rate | 25% of sessions | 40% of sessions |
| Real research initiated post-session | 15% of sessions | 30% of sessions |

The north star metric is **"Changed my approach"** - the percentage of sessions after which a user reports they changed something about their strategy, messaging, or assumptions. If this number is low, the tool is confirming biases instead of challenging them.

## 11. Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Teams treat simulation as validated research | High - false confidence in untested assumptions | Persistent disclaimers, session summaries that explicitly recommend follow-up research questions, "confidence ceiling" language |
| Psychographic profiles reinforce stereotypes | High - reputational and ethical harm | Bias audit pipeline, prompt engineering to avoid demographic shortcuts, human review of flagged sessions |
| Persona contradicts itself across long sessions | Medium - erodes trust in the tool | Full message history (no summarization), periodic profile re-injection, contradiction detection layer |
| Client data leakage via LLM | High - enterprise deal-breaker | No training on user data, data isolation per workspace, SOC 2 compliance, enterprise deployment option |

## 12. Phased Roadmap

### Phase 1: Foundation (Weeks 1-6)

Ship the core loop: describe an audience, generate a profile, have a conversation.

- Free-text brand and audience input
- Psychographic profile generation (JSON schema-validated)
- Conversation mode with persistent context panel
- Tone indicators on every response
- Session transcript export (Markdown)
- Visible guardrails and disclaimers

### Phase 2: Depth (Weeks 7-12)

Add the features that make the tool indispensable for strategy work.

- Provocation engine (every 5 messages)
- Copy-paste zone for creative review
- Scenario runner with structured reactions
- Saved persona library
- Editable profile dimensions
- Session summary generation
- PDF export with branding

### Phase 3: Scale (Weeks 13-20)

Multi-persona capabilities and team workflows.

- Multi-persona comparison (same scenario, different audiences)
- Team workspaces with shared persona libraries
- SSO / enterprise authentication
- Slack integration for sharing insights
- Import personas from Audience Insight Engine
- Bias audit dashboard

## 13. Open Questions

- Should the persona ever break character to offer strategic meta-commentary? (for example, "As this persona I wouldn't say this, but as a strategist, you should know...")
- How do we measure psychographic consistency? What's the acceptable contradiction threshold?
- Should we support voice input for the conversation mode? Some strategists think better out loud.
- What's the right pricing model? Per-seat, per-session, per-workspace?
- Should scenario reactions include a confidence score per dimension, or does that imply false precision?
- How do we handle audience segments that intersect with protected characteristics without reducing people to demographics?

---

This document is a living artifact. It will evolve as we validate assumptions through prototyping and user testing.
