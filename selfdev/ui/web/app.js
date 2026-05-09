"use strict";

const endpoints = {
  health: "/health",
  summary: "/summary",
  targets: "/targets",
  kanban: "/kanban",
  artifacts: "/artifacts",
  actionTemplate: "/actions/{task_id}",
  actionPrefix: "/actions/",
  artifactPreviewTemplate: "/artifact-previews/{artifact_id}",
  artifactPreviewPrefix: "/artifact-previews/",
};

const safetyBoundaries = [
  "No mutation",
  "No shell execution",
  "No patch apply",
  "No commit",
  "No push",
  "No merge",
  "No deploy",
  "No release",
  "No .env modification",
  "No secret read",
];

const $ = (id) => document.getElementById(id);

function asPrettyJson(value) {
  return JSON.stringify(value, null, 2);
}

function singleSegment(value) {
  return String(value || "").trim().replace(/^\/+|\/+$/g, "");
}

async function getJson(path) {
  const response = await fetch(path, {
    method: "GET",
    headers: { Accept: "application/json" },
  });
  const payload = await response.json().catch(() => ({ error: "invalid_json" }));
  if (!response.ok) {
    return { ok: false, status: response.status, payload };
  }
  return { ok: true, status: response.status, payload };
}

function renderBoundary() {
  const target = $("safetyBoundary");
  if (!target) return;
  target.innerHTML = safetyBoundaries
    .map((item) => `<span class="boundary-chip">${item}</span>`)
    .join("");
}

function setHealthState(ok, label) {
  const badge = $("healthBadge");
  if (!badge) return;
  badge.textContent = label;
  badge.className = ok ? "state-pill good" : "state-pill warn";
}

function renderSummary(payload) {
  const output = $("summaryOutput");
  if (!output) return;
  output.textContent = asPrettyJson(payload);
}

function renderTargets(payload) {
  const list = $("targetList");
  if (!list) return;
  const targets = payload.targets || payload.items || [];
  if (!Array.isArray(targets) || targets.length === 0) {
    list.innerHTML = `<div class="muted-card">No targets reported by the API.</div>`;
    return;
  }
  list.innerHTML = targets
    .map((target) => {
      const id = target.target_id || target.id || "unknown-target";
      const kind = target.kind || target.type || "target";
      const status = target.status || "registered";
      return `<article class="mini-card"><strong>${id}</strong><span>${kind}</span><small>${status}</small></article>`;
    })
    .join("");
}

function renderKanban(payload) {
  const list = $("kanbanList");
  if (!list) return;
  const tasks = payload.tasks || payload.items || [];
  if (!Array.isArray(tasks) || tasks.length === 0) {
    list.innerHTML = `<div class="muted-card">No kanban tasks found.</div>`;
    return;
  }
  list.innerHTML = tasks
    .map((task) => {
      const taskId = task.task_id || task.id || "unknown-task";
      const status = task.status || task.column || "unknown";
      const title = task.title || task.summary || taskId;
      return `<article class="task-card" data-task-id="${taskId}"><strong>${title}</strong><span>${taskId}</span><small>${status}</small></article>`;
    })
    .join("");
  list.querySelectorAll("[data-task-id]").forEach((item) => {
    item.addEventListener("click", () => {
      const input = $("taskIdInput");
      if (input) input.value = item.getAttribute("data-task-id") || "";
      loadActions();
    });
  });
}

function renderArtifacts(payload) {
  const list = $("artifactList");
  if (!list) return;
  const artifacts = payload.artifacts || payload.items || [];
  if (!Array.isArray(artifacts) || artifacts.length === 0) {
    list.innerHTML = `<div class="muted-card">No artifacts reported by the API.</div>`;
    return;
  }
  list.innerHTML = artifacts
    .map((artifact) => {
      const artifactId = artifact.artifact_id || artifact.id || "unknown-artifact";
      const artifactType = artifact.artifact_type || artifact.type || "artifact";
      const status = artifact.status || "registered";
      return `<article class="mini-card artifact-card" data-artifact-id="${artifactId}"><strong>${artifactId}</strong><span>${artifactType}</span><small>${status}</small></article>`;
    })
    .join("");
  list.querySelectorAll("[data-artifact-id]").forEach((item) => {
    item.addEventListener("click", () => {
      const input = $("artifactIdInput");
      if (input) input.value = item.getAttribute("data-artifact-id") || "";
    });
  });
}

function renderArtifactPreview(payload, artifactId, ok) {
  const meta = $("previewMeta");
  const content = $("previewContent");
  if (!meta || !content) return;
  const preview = payload || {};
  meta.className = ok
    ? "preview-meta muted-card artifact-preview-meta"
    : "preview-meta warn-card artifact-preview-meta";
  meta.textContent = `artifact_id=${preview.artifact_id || artifactId} | preview_length=${preview.preview_length ?? 0} | truncated=${Boolean(preview.truncated)} | redacted=${Boolean(preview.redacted)}`;
  content.textContent = preview.content || asPrettyJson(preview);
}

async function loadActions() {
  const taskId = singleSegment($("taskIdInput")?.value);
  const output = $("actionOutput");
  if (!output) return;
  if (!taskId) {
    output.textContent = "Enter a single-segment task ID.";
    return;
  }
  output.textContent = "Loading read-only action availability...";
  const result = await getJson(`${endpoints.actionPrefix}${encodeURIComponent(taskId)}`);
  output.className = result.ok ? "action-card" : "action-card warn-card";
  output.textContent = asPrettyJson(result.payload);
}

async function loadArtifactPreview() {
  const artifactId = singleSegment($("artifactIdInput")?.value);
  const meta = $("previewMeta");
  const content = $("previewContent");
  if (!meta || !content) return;
  if (!artifactId) {
    meta.className = "preview-meta warn-card artifact-preview-meta";
    meta.textContent = "Enter a single-segment artifact ID.";
    content.textContent = "";
    return;
  }
  meta.className = "preview-meta muted-card artifact-preview-meta";
  meta.textContent = "Loading redacted preview...";
  content.textContent = "";
  const result = await getJson(`${endpoints.artifactPreviewPrefix}${encodeURIComponent(artifactId)}`);
  renderArtifactPreview(result.payload || {}, artifactId, result.ok);
}

async function refreshAll() {
  setHealthState(false, "Loading");
  const [health, summary, targets, kanban, artifacts] = await Promise.all([
    getJson(endpoints.health),
    getJson(endpoints.summary),
    getJson(endpoints.targets),
    getJson(endpoints.kanban),
    getJson(endpoints.artifacts),
  ]);

  const healthOutput = $("healthOutput");
  if (healthOutput) healthOutput.textContent = asPrettyJson(health.payload);
  setHealthState(health.ok, health.ok ? "Healthy" : "Unavailable");
  renderSummary(summary.payload);
  renderTargets(targets.payload);
  renderKanban(kanban.payload);
  renderArtifacts(artifacts.payload);
}

document.addEventListener("DOMContentLoaded", () => {
  renderBoundary();
  $("refreshButton")?.addEventListener("click", refreshAll);
  $("loadActionsButton")?.addEventListener("click", loadActions);
  $("loadPreviewButton")?.addEventListener("click", loadArtifactPreview);
  refreshAll();
});
