const state = {
  personas: [],
  selectedPersonaId: null,
  sessionId: null,
};

const el = {
  status: document.getElementById("status"),
  personaName: document.getElementById("personaName"),
  brandDescription: document.getElementById("brandDescription"),
  audienceDescription: document.getElementById("audienceDescription"),
  personaSelect: document.getElementById("personaSelect"),
  profileJson: document.getElementById("profileJson"),
  profileSummary: document.getElementById("profileSummary"),
  chatWindow: document.getElementById("chatWindow"),
  chatInput: document.getElementById("chatInput"),
  copyZone: document.getElementById("copyZone"),
  summaryOutput: document.getElementById("summaryOutput"),
  scenarioTitle: document.getElementById("scenarioTitle"),
  scenarioContext: document.getElementById("scenarioContext"),
  scenarioArtifact: document.getElementById("scenarioArtifact"),
  scenarioOutput: document.getElementById("scenarioOutput"),
};

function setStatus(message, isError = false) {
  el.status.textContent = message;
  el.status.style.color = isError ? "#b42318" : "#344054";
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed (${response.status})`);
  }
  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return response.json();
  }
  return response.text();
}

function renderPersonaSelect() {
  el.personaSelect.innerHTML =
    '<option value="">Select a saved persona</option>' +
    state.personas
      .map(
        (p) =>
          `<option value="${p.id}" ${
            Number(p.id) === Number(state.selectedPersonaId) ? "selected" : ""
          }>${escapeHtml(p.name)}</option>`,
      )
      .join("");
}

function renderProfileSummary(profile, personaName = "Persona") {
  const dimensions = profile.psychographic_dimensions
    .map((d) => `<li><strong>${escapeHtml(d.name)}</strong>: ${escapeHtml(d.label)} (${d.position}/100)</li>`)
    .join("");
  const tensions = profile.cultural_tensions.map((t) => `<li>${escapeHtml(t)}</li>`).join("");
  const motivations = profile.hidden_motivations.map((m) => `<li>${escapeHtml(m)}</li>`).join("");
  const codes = (profile.language_codes.vocabulary || []).map((v) => `<li>${escapeHtml(v)}</li>`).join("");

  el.profileSummary.innerHTML = `
    <h3>${escapeHtml(personaName)}</h3>
    <p><strong>${escapeHtml(profile.archetype_name)}</strong></p>
    <p>${escapeHtml(profile.core_truth)}</p>
    <p>${escapeHtml(profile.identity_summary)}</p>
    <h4>Psychographic dimensions</h4>
    <ul>${dimensions}</ul>
    <h4>Cultural tensions</h4>
    <ul>${tensions}</ul>
    <h4>Hidden motivations</h4>
    <ul>${motivations}</ul>
    <h4>Language codes</h4>
    <ul>${codes}</ul>
  `;
}

function renderChat(session) {
  if (!session.messages.length) {
    el.chatWindow.innerHTML = '<div class="muted small">No messages yet. Ask the persona a question.</div>';
    return;
  }
  el.chatWindow.innerHTML = session.messages
    .map((message) => {
      if (message.role === "provocation") {
        return `<div class="provocation"><strong>Provocation:</strong> ${escapeHtml(message.content)}</div>`;
      }
      const role = message.role === "user" ? "You" : "Persona";
      const tone = message.tone ? `<div class="tone">Tone: ${escapeHtml(message.tone)}</div>` : "";
      return `<div class="msg ${message.role}">${tone}<div><strong>${role}:</strong> ${escapeHtml(
        message.content,
      )}</div></div>`;
    })
    .join("");
  el.chatWindow.scrollTop = el.chatWindow.scrollHeight;
}

async function refreshPersonas() {
  state.personas = await api("/api/personas");
  renderPersonaSelect();
}

async function generateProfile() {
  const brand = el.brandDescription.value.trim();
  const audience = el.audienceDescription.value.trim();
  if (!brand || !audience) {
    setStatus("Add both brand and audience descriptions first.", true);
    return;
  }
  const profilePreview = await api("/api/personas", {
    method: "POST",
    body: JSON.stringify({
      name: el.personaName.value.trim() || "Draft Persona",
      brand_description: brand,
      audience_description: audience,
    }),
  });
  state.selectedPersonaId = profilePreview.id;
  el.personaName.value = profilePreview.name;
  el.profileJson.textContent = JSON.stringify(profilePreview.profile, null, 2);
  renderProfileSummary(profilePreview.profile, profilePreview.name);
  await refreshPersonas();
  setStatus("Profile generated and saved.");
}

async function loadPersona() {
  const personaId = Number(el.personaSelect.value);
  if (!personaId) {
    return;
  }
  const persona = await api(`/api/personas/${personaId}`);
  state.selectedPersonaId = persona.id;
  el.personaName.value = persona.name;
  el.brandDescription.value = persona.brand_description;
  el.audienceDescription.value = persona.audience_description;
  el.profileJson.textContent = JSON.stringify(persona.profile, null, 2);
  renderProfileSummary(persona.profile, persona.name);
  setStatus(`Loaded "${persona.name}".`);
}

async function startSession() {
  if (!state.selectedPersonaId) {
    setStatus("Generate or load a persona first.", true);
    return;
  }
  const session = await api(`/api/sessions/${state.selectedPersonaId}`, { method: "POST" });
  state.sessionId = session.id;
  el.summaryOutput.innerHTML = "";
  renderChat(session);
  setStatus("Session started.");
}

async function sendTurn(message) {
  if (!state.sessionId) {
    setStatus("Start a session first.", true);
    return;
  }
  const text = message.trim();
  if (!text) {
    return;
  }
  const session = await api(`/api/sessions/${state.sessionId}/turns`, {
    method: "POST",
    body: JSON.stringify({ message: text }),
  });
  renderChat(session);
}

async function generateSummary() {
  if (!state.sessionId) {
    setStatus("Start a session first.", true);
    return;
  }
  const data = await api(`/api/sessions/${state.sessionId}/summary`);
  const summary = data.summary;
  el.summaryOutput.innerHTML = `
    <h4>Key themes</h4>
    <ul>${summary.key_themes.map((v) => `<li>${escapeHtml(v)}</li>`).join("")}</ul>
    <h4>Surprises</h4>
    <ul>${summary.surprises.map((v) => `<li>${escapeHtml(v)}</li>`).join("")}</ul>
    <h4>Recommended follow-up questions</h4>
    <ul>${summary.followup_questions.map((v) => `<li>${escapeHtml(v)}</li>`).join("")}</ul>
    <p class="small"><strong>Disclaimer:</strong> ${escapeHtml(summary.disclaimer)}</p>
    <p class="small muted">${escapeHtml(summary.final_reflection || "")}</p>
  `;
}

async function exportTranscript() {
  if (!state.sessionId) {
    setStatus("Start a session first.", true);
    return;
  }
  const markdown = await api(`/api/sessions/${state.sessionId}/export`);
  const blob = new Blob([markdown], { type: "text/markdown" });
  const href = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = href;
  anchor.download = `session-${state.sessionId}.md`;
  anchor.click();
  URL.revokeObjectURL(href);
  setStatus("Transcript exported.");
}

async function runScenario() {
  if (!state.selectedPersonaId) {
    setStatus("Generate or load a persona first.", true);
    return;
  }
  const context = el.scenarioContext.value.trim();
  if (!context) {
    setStatus("Scenario context is required.", true);
    return;
  }
  const result = await api(`/api/scenarios/${state.selectedPersonaId}`, {
    method: "POST",
    body: JSON.stringify({
      title: el.scenarioTitle.value.trim() || "Scenario Test",
      context,
      artifact_text: el.scenarioArtifact.value.trim(),
    }),
  });
  el.scenarioOutput.innerHTML = `<pre class="profile-pre">${escapeHtml(
    JSON.stringify(result.reaction, null, 2),
  )}</pre>`;
}

async function init() {
  try {
    await refreshPersonas();
    setStatus("Ready.");
  } catch (error) {
    setStatus(`Startup error: ${error.message}`, true);
  }

  document.getElementById("generateProfileBtn").addEventListener("click", async () => {
    try {
      await generateProfile();
    } catch (error) {
      setStatus(`Generate failed: ${error.message}`, true);
    }
  });

  document.getElementById("savePersonaBtn").addEventListener("click", async () => {
    try {
      await generateProfile();
    } catch (error) {
      setStatus(`Save failed: ${error.message}`, true);
    }
  });

  document.getElementById("loadPersonaBtn").addEventListener("click", async () => {
    try {
      await loadPersona();
    } catch (error) {
      setStatus(`Load failed: ${error.message}`, true);
    }
  });

  document.getElementById("startSessionBtn").addEventListener("click", async () => {
    try {
      await startSession();
    } catch (error) {
      setStatus(`Session start failed: ${error.message}`, true);
    }
  });

  document.getElementById("chatSendBtn").addEventListener("click", async () => {
    try {
      const text = el.chatInput.value;
      el.chatInput.value = "";
      await sendTurn(text);
    } catch (error) {
      setStatus(`Message failed: ${error.message}`, true);
    }
  });

  document.getElementById("copySendBtn").addEventListener("click", async () => {
    try {
      const text = `Please react to this draft copy:\n${el.copyZone.value}`;
      el.copyZone.value = "";
      await sendTurn(text);
    } catch (error) {
      setStatus(`Copy review failed: ${error.message}`, true);
    }
  });

  document.getElementById("generateSummaryBtn").addEventListener("click", async () => {
    try {
      await generateSummary();
    } catch (error) {
      setStatus(`Summary failed: ${error.message}`, true);
    }
  });

  document.getElementById("exportTranscriptBtn").addEventListener("click", async () => {
    try {
      await exportTranscript();
    } catch (error) {
      setStatus(`Export failed: ${error.message}`, true);
    }
  });

  document.getElementById("scenarioRunBtn").addEventListener("click", async () => {
    try {
      await runScenario();
    } catch (error) {
      setStatus(`Scenario failed: ${error.message}`, true);
    }
  });

  el.chatInput.addEventListener("keydown", async (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      try {
        const text = el.chatInput.value;
        el.chatInput.value = "";
        await sendTurn(text);
      } catch (error) {
        setStatus(`Message failed: ${error.message}`, true);
      }
    }
  });
}

init();
