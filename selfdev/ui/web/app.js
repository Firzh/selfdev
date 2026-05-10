(() => {
  "use strict";

  const ARTIFACT_CARD_ID_ATTRIBUTE = "data-artifact-id";

  const API_BASE = window.SELFDEV_API_BASE || "";

  const READ_ONLY_ENDPOINTS = [
    "/health",
    "/summary",
    "/targets",
    "/targets/{target_id}",
    "/targets/",
    "/kanban",
    "/actions/{task_id}",
    "/actions/",
    "/artifacts",
    "/artifact-previews/{artifact_id}",
    "/artifact-previews/",
  ];

  const READ_ONLY_BOUNDARY_MARKERS = Object.freeze([
    "No mutation",
    "No command execution",
    "No patch apply",
    "No VCS write",
    "No push",
    "No merge",
    "No deploy",
    "No release",
    "No .env modification",
    "No secret read",
  ]);

  function $(id) {
    return document.getElementById(id);
  }

  function endpoint(path) {
    return `${API_BASE}${path}`;
  }

  function asText(value) {
    if (value === null || value === undefined || value === "") {
      return "—";
    }
    return String(value);
  }

  function asPrettyJson(value) {
    return JSON.stringify(value, null, 2);
  }

  async function readJson(path) {
    try {
      const response = await fetch(endpoint(path), {
        method: "GET",
        headers: { Accept: "application/json" },
      });
      const contentType = response.headers.get("content-type") || "";
      const payload = contentType.includes("application/json")
        ? await response.json()
        : { raw: await response.text() };
      return { ok: response.ok, status: response.status, payload };
    } catch (error) {
      return { ok: false, status: 0, payload: { error: String(error) } };
    }
  }

  function setText(id, value) {
    const element = $(id);
    if (element) {
      element.textContent = value;
    }
  }

  function setStatus(id, ok, label) {
    const element = $(id);
    if (!element) {
      return;
    }
    element.textContent = label || (ok ? "ready" : "error");
    element.classList.toggle("danger", !ok);
  }

  function renderSafetyBoundary() {
    const boundary = $("safetyBoundary");
    if (!boundary) {
      return;
    }
    boundary.replaceChildren(
      ...READ_ONLY_BOUNDARY_MARKERS.map((label) => {
        const item = document.createElement("span");
        item.className = "mode-badge";
        item.textContent = label;
        return item;
      }),
    );
  }

  function targetEntries(payload) {
    if (Array.isArray(payload)) {
      return payload;
    }
    if (Array.isArray(payload?.targets)) {
      return payload.targets;
    }
    if (Array.isArray(payload?.items)) {
      return payload.items;
    }
    if (Array.isArray(payload?.data?.targets)) {
      return payload.data.targets;
    }
    return [];
  }

  function artifactEntries(payload) {
    if (Array.isArray(payload)) {
      return payload;
    }
    if (Array.isArray(payload?.artifacts)) {
      return payload.artifacts;
    }
    if (Array.isArray(payload?.items)) {
      return payload.items;
    }
    if (Array.isArray(payload?.data?.artifacts)) {
      return payload.data.artifacts;
    }
    return [];
  }

  function taskEntries(payload) {
    if (Array.isArray(payload)) {
      return payload;
    }
    if (Array.isArray(payload?.tasks)) {
      return payload.tasks;
    }
    if (Array.isArray(payload?.items)) {
      return payload.items;
    }
    if (Array.isArray(payload?.columns)) {
      return payload.columns.flatMap((column) => column.tasks || []);
    }
    return [];
  }

  function actionEntries(payload) {
    if (Array.isArray(payload)) {
      return payload;
    }
    if (Array.isArray(payload?.actions)) {
      return payload.actions;
    }
    if (Array.isArray(payload?.items)) {
      return payload.items;
    }
    return [];
  }

  function stableTargetId(target) {
    return asText(target?.target_id || target?.id || target?.name || target?.slug);
  }

  function stableArtifactId(artifact) {
    return asText(artifact?.artifact_id || artifact?.id || artifact?.name || artifact?.path);
  }

  function renderTargets(payload) {
    const container = $("targetList");
    if (!container) {
      return;
    }
    const entries = targetEntries(payload);
    if (!entries.length) {
      container.innerHTML = '<p class="muted">No targets found.</p>';
      return;
    }
    container.replaceChildren(
      ...entries.map((target) => {
        const targetId = stableTargetId(target);
        const button = document.createElement("button");
        button.type = "button";
        button.className = "task-card target-card";
        button.dataset.targetId = targetId;
        button.innerHTML = `
          <strong>${targetId}</strong>
          <span>${asText(target.kind || target.type || target.root || target.path)}</span>
        `;
        button.addEventListener("click", () => {
          const input = $("target-id-input");
          if (input) {
            input.value = targetId;
          }
          loadTargetDetail();
        });
        return button;
      }),
    );
  }

  function renderArtifacts(payload) {
    const container = $("artifactList");
    if (!container) {
      return;
    }
    const entries = artifactEntries(payload);
    if (!entries.length) {
      container.innerHTML = '<p class="muted">No artifacts found.</p>';
      return;
    }
    container.replaceChildren(
      ...entries.map((artifact) => {
        const artifactId = stableArtifactId(artifact);
        const button = document.createElement("button");
        button.type = "button";
        button.className = "task-card artifact-card";
        button.dataset.artifactId = artifactId;
        button.innerHTML = `
          <strong>${artifactId}</strong>
          <span>${asText(artifact.artifact_type || artifact.type || artifact.status || artifact.path)}</span>
        `;
        button.addEventListener("click", () => {
          const input = $("artifact-id-input");
          if (input) {
            input.value = artifactId;
          }
          loadArtifactPreview();
        });
        return button;
      }),
    );
  }

  function renderKanban(payload) {
    const container = $("kanbanList");
    if (!container) {
      return;
    }
    const entries = taskEntries(payload);
    if (!entries.length) {
      container.innerHTML = '<p class="muted">No task cards found.</p>';
      return;
    }
    container.replaceChildren(
      ...entries.slice(0, 12).map((task) => {
        const card = document.createElement("article");
        card.className = "task-card";
        card.innerHTML = `
          <strong>${asText(task.task_id || task.id || task.title)}</strong>
          <span>${asText(task.status || task.column || task.agent_id)}</span>
        `;
        return card;
      }),
    );
  }

  function renderActions(payload) {
    const container = $("actionList");
    if (!container) {
      return;
    }
    const entries = actionEntries(payload);
    if (!entries.length) {
      container.innerHTML = '<p class="muted">No actions found.</p>';
      return;
    }
    container.replaceChildren(
      ...entries.map((action) => {
        const card = document.createElement("article");
        card.className = "action-card";
        card.innerHTML = `
          <strong>${asText(action.action_id || action.id || action.kind || action.type)}</strong>
          <span>${asText(action.status || action.agent_id || action.created_at)}</span>
        `;
        return card;
      }),
    );
  }

  function renderTargetDetail(payload, targetId, ok) {
    setStatus("targetDetailStatus", ok, ok ? "loaded" : "error");
    setText("target-detail-meta", `target_id=${targetId} · ok=${ok}`);
    setText("target-detail-content", asPrettyJson(payload));
  }

  async function loadTargetDetail() {
    const input = $("target-id-input");
    const targetId = (input?.value || "").trim();
    if (!targetId) {
      setStatus("targetDetailStatus", false, "missing target id");
      return;
    }
    setStatus("targetDetailStatus", true, "loading");
    const result = await readJson(`/targets/${encodeURIComponent(targetId)}`);
    renderTargetDetail(result.payload || {}, targetId, result.ok);
  }

  function renderArtifactPreview(payload, artifactId, ok) {
    setStatus("previewStatus", ok, ok ? "loaded" : "error");
    const meta = [
      `artifact_id=${artifactId}`,
      `ok=${ok}`,
      `redacted=${Boolean(payload.redacted)}`,
      `truncated=${Boolean(payload.truncated)}`,
      `preview_length=${asText(payload.preview_length)}`,
    ].join(" · ");
    setText("artifact-preview-meta", meta);
    const preview = payload.content ?? asPrettyJson(payload);
    setText("artifact-preview-content", String(preview));
    setText("previewContent", String(preview));
  }

  function renderArtifactPreviewResult(result, artifactId) {
    renderArtifactPreview(result.payload || {}, artifactId, result.ok);
  }

  async function loadArtifactPreview() {
    const input = $("artifact-id-input");
    const artifactId = (input?.value || "").trim();
    if (!artifactId) {
      setStatus("previewStatus", false, "missing artifact id");
      return;
    }
    setStatus("previewStatus", true, "loading");
    const result = await readJson(`/artifact-previews/${encodeURIComponent(artifactId)}`);
    renderArtifactPreview(result.payload || {}, artifactId, result.ok);
  }

  async function loadActions() {
    const input = $("task-id-input");
    const taskId = (input?.value || "").trim();
    if (!taskId) {
      setStatus("actionsStatus", false, "missing task id");
      return;
    }
    setStatus("actionsStatus", true, "loading");
    const result = await readJson(`/actions/${encodeURIComponent(taskId)}`);
    setStatus("actionsStatus", result.ok, result.ok ? "loaded" : "error");
    renderActions(result.payload || {});
  }

  async function refresh() {
    renderSafetyBoundary();
    const [health, summary, targets, kanban, artifacts] = await Promise.all([
      readJson("/health"),
      readJson("/summary"),
      readJson("/targets"),
      readJson("/kanban"),
      readJson("/artifacts"),
    ]);
    setText("healthStatus", health.ok ? "ok" : "error");
    setStatus("healthBadge", health.ok, health.ok ? "healthy" : "error");
    setText("summaryStatus", summary.ok ? "loaded" : "error");
    setText("summaryContent", asPrettyJson(summary.payload || {}));
    setStatus("targetStatus", targets.ok, targets.ok ? "loaded" : "error");
    setStatus("kanbanStatus", kanban.ok, kanban.ok ? "loaded" : "error");
    setStatus("artifactStatus", artifacts.ok, artifacts.ok ? "loaded" : "error");
    renderTargets(targets.payload || {});
    renderKanban(kanban.payload || {});
    renderArtifacts(artifacts.payload || {});
  }

  function bindEvents() {
    $("refreshButton")?.addEventListener("click", refresh);
    $("loadActionsButton")?.addEventListener("click", loadActions);
    $("artifact-preview-button")?.addEventListener("click", loadArtifactPreview);
    $("target-detail-button")?.addEventListener("click", loadTargetDetail);
  }

  document.addEventListener("DOMContentLoaded", () => {
    bindEvents();
    refresh();
  });
  function rememberArtifactForPreview(artifactId) {
    byId("artifact-id-input").value = artifactId;
    return artifactId;
  }

})();
