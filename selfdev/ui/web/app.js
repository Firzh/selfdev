(() => {
  "use strict";

  const API_BASE = window.SELFDEV_API_BASE || "";

  const READ_ONLY_ENDPOINTS = [
    "/health",
    "/summary",
    "/targets",
    "/kanban",
    "/actions/{task_id}",
    "/actions/",
    "/artifacts",
    "/artifact-previews/{artifact_id}",
    "/artifact-previews/",
  ];

  const FORBIDDEN_CAPABILITIES = [
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

  function byId(id) {
    const element = document.getElementById(id);
    if (!element) {
      throw new Error(`Missing UI element: ${id}`);
    }
    return element;
  }

  function renderList(target, values) {
    target.innerHTML = "";
    values.forEach((value) => {
      const item = document.createElement("li");
      item.textContent = value;
      target.appendChild(item);
    });
  }

  function renderError(target, error) {
    target.className = "status-card danger";
    target.textContent = `Read-only API unavailable: ${error.message}`;
  }

  async function readJson(endpoint) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: "GET",
      headers: { Accept: "application/json" },
      cache: "no-store",
    });

    if (!response.ok) {
      throw new Error(`${endpoint} returned HTTP ${response.status}`);
    }

    return response.json();
  }

  function safeSegment(value) {
    return String(value || "").trim();
  }

  function renderHealth(payload) {
    const healthCard = byId("health-card");
    healthCard.className = `status-card ${payload.status === "ok" ? "success" : "warning"}`;
    healthCard.innerHTML = "";

    const title = document.createElement("strong");
    title.textContent = `${payload.service || "selfdev"} · ${payload.status || "unknown"}`;

    const mode = document.createElement("span");
    mode.textContent = `mode: ${payload.mode || "read-only"}`;

    healthCard.append(title, mode);
  }

  function renderSummary(payload) {
    const summaryGrid = byId("summary-grid");
    const cards = [
      ["Health", payload.health_status || payload.status || "unknown"],
      ["Tasks", payload.task_count ?? payload.tasks ?? "—"],
      ["Artifacts", payload.artifact_count ?? payload.artifacts ?? "—"],
      ["Agents", payload.agent_count ?? payload.agents ?? "—"],
    ];

    summaryGrid.innerHTML = "";
    cards.forEach(([label, value]) => {
      const card = document.createElement("article");
      card.className = "metric-card";
      const cardLabel = document.createElement("span");
      cardLabel.textContent = label;
      const cardValue = document.createElement("strong");
      cardValue.textContent = String(value);
      card.append(cardLabel, cardValue);
      summaryGrid.appendChild(card);
    });
  }

  function taskEntries(payload) {
    if (Array.isArray(payload.tasks)) {
      return payload.tasks;
    }
    if (Array.isArray(payload.items)) {
      return payload.items;
    }
    if (payload.columns && typeof payload.columns === "object") {
      return Object.entries(payload.columns).flatMap(([status, tasks]) =>
        Array.isArray(tasks) ? tasks.map((task) => ({ ...task, status })) : []
      );
    }
    return [];
  }

  function renderKanban(payload) {
    const taskList = byId("task-list");
    const tasks = taskEntries(payload);
    taskList.innerHTML = "";

    if (!tasks.length) {
      taskList.className = "task-list muted";
      taskList.textContent = "No tasks reported by the read-only API.";
      return;
    }

    taskList.className = "task-list";
    tasks.forEach((task) => {
      const card = document.createElement("button");
      card.type = "button";
      card.className = "task-card";
      card.textContent = `${task.task_id || task.id || "unknown-task"} · ${task.status || "unknown"}`;
      card.addEventListener("click", () => {
        byId("task-id-input").value = task.task_id || task.id || "";
        loadActions();
      });
      taskList.appendChild(card);
    });
  }

  function targetEntries(payload) {
    if (Array.isArray(payload.targets)) {
      return payload.targets;
    }
    if (Array.isArray(payload.items)) {
      return payload.items;
    }
    return [];
  }

  function renderTargets(payload) {
    const targetList = byId("target-list");
    const targets = targetEntries(payload);
    targetList.innerHTML = "";

    if (!targets.length) {
      targetList.className = "target-list muted";
      targetList.textContent = "No targets reported by the read-only API.";
      return;
    }

    targetList.className = "target-list";
    targets.forEach((target) => {
      const card = document.createElement("article");
      card.className = "target-card";
      const name = document.createElement("strong");
      name.textContent = target.target_id || target.id || target.name || "unknown-target";
      const type = document.createElement("span");
      type.textContent = target.type || target.kind || "registered target";
      card.append(name, type);
      targetList.appendChild(card);
    });
  }

  function renderActions(payload) {
    const actionCard = byId("action-card");
    actionCard.className = "action-card";
    actionCard.innerHTML = "";

    const task = document.createElement("strong");
    task.textContent = payload.task_id || "unknown task";
    actionCard.appendChild(task);

    const values = Object.entries(payload.actions || payload.availability || {}).map(
      ([name, allowed]) => `${name}: ${allowed ? "available" : "blocked"}`
    );

    const list = document.createElement("ul");
    renderList(list, values.length ? values : ["No action model returned."]);
    actionCard.appendChild(list);
  }

  function renderArtifactPreview(payload) {
    const status = byId("artifact-preview-status");
    const content = byId("artifact-preview-content");
    const meta = byId("artifact-preview-meta");

    status.className = payload.exists ? "inline-status success" : "inline-status warning";
    status.textContent = `${payload.content_status || "unknown"}${payload.redacted ? " · redacted" : ""}`;
    content.textContent = payload.content || "No preview content available.";

    const rows = [
      ["artifact", payload.artifact_id || "unknown"],
      ["preview_length", payload.preview_length ?? "—"],
      ["truncated", payload.truncated ? "yes" : "no"],
      ["redacted", payload.redacted ? "yes" : "no"],
    ];

    meta.innerHTML = "";
    rows.forEach(([label, value]) => {
      const term = document.createElement("dt");
      term.textContent = label;
      const detail = document.createElement("dd");
      detail.textContent = String(value);
      meta.append(term, detail);
    });
  }

  async function loadActions() {
    const taskId = safeSegment(byId("task-id-input").value);
    const actionCard = byId("action-card");
    if (!taskId) {
      actionCard.className = "action-card muted";
      actionCard.textContent = "Select a task to inspect backend-approved action availability.";
      return;
    }

    try {
      const payload = await readJson(`/actions/${encodeURIComponent(taskId)}`);
      renderActions(payload);
    } catch (error) {
      actionCard.className = "action-card danger";
      actionCard.textContent = error.message;
    }
  }

  async function loadArtifactPreview() {
    const artifactId = safeSegment(byId("artifact-id-input").value);
    const status = byId("artifact-preview-status");
    const content = byId("artifact-preview-content");
    if (!artifactId) {
      status.className = "inline-status muted";
      status.textContent = "No artifact selected.";
      content.textContent = "Select an artifact to preview redacted text safely.";
      return;
    }

    try {
      status.className = "inline-status muted";
      status.textContent = "Loading read-only redacted preview...";
      const payload = await readJson(`/artifact-previews/${encodeURIComponent(artifactId)}`);
      renderArtifactPreview(payload);
    } catch (error) {
      status.className = "inline-status danger";
      status.textContent = error.message;
      content.textContent = "Preview could not be loaded.";
    }
  }

  async function refresh() {
    renderList(byId("boundary-list"), FORBIDDEN_CAPABILITIES);
    renderList(byId("endpoint-list"), READ_ONLY_ENDPOINTS);

    try {
      const [health, summary, targets, kanban] = await Promise.all([
        readJson("/health"),
        readJson("/summary"),
        readJson("/targets"),
        readJson("/kanban"),
      ]);

      renderHealth(health);
      renderSummary(summary);
      renderTargets(targets);
      renderKanban(kanban);
    } catch (error) {
      renderError(byId("health-card"), error);
    }
  }

  function bindEvents() {
    byId("refresh-button").addEventListener("click", refresh);
    byId("task-id-input").addEventListener("change", loadActions);
    byId("artifact-preview-button").addEventListener("click", loadArtifactPreview);
    byId("artifact-id-input").addEventListener("change", loadArtifactPreview);
  }

  document.addEventListener("DOMContentLoaded", () => {
    bindEvents();
    refresh();
  });
})();
