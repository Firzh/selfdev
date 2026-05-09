(() => {
  "use strict";

  const API_BASE = window.SELFDEV_API_BASE || "";

  const READ_ONLY_ENDPOINTS = [
    "/health",
    "/summary",
    "/kanban",
    "/actions/{task_id}",
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

  function renderHealth(payload) {
    const healthCard = byId("health-card");
    healthCard.className = `status-card ${payload.status === "ok" ? "success" : "warning"}`;
    healthCard.innerHTML = "";

    const title = document.createElement("strong");
    title.textContent = `${payload.service} · ${payload.status}`;

    const mode = document.createElement("span");
    mode.textContent = `mode: ${payload.mode}`;

    healthCard.append(title, mode);
  }

  function renderSummary(payload) {
    const summaryGrid = byId("summary-grid");
    const cards = [
      ["Health", payload.health_status],
      ["Tasks", payload.task_count],
      ["Artifacts", payload.artifact_count],
      ["Agents", payload.agent_count],
    ];

    summaryGrid.innerHTML = "";
    cards.forEach(([label, value]) => {
      const card = document.createElement("article");
      card.className = "metric-card";
      card.innerHTML = `<span>${label}</span><strong>${value}</strong>`;
      summaryGrid.appendChild(card);
    });
  }

  function renderKanban(payload) {
    const taskList = byId("task-list");
    const tasks = payload.tasks || {};
    const entries = Object.entries(tasks);

    taskList.innerHTML = "";
    if (entries.length === 0) {
      taskList.textContent = "No tasks found in the local workspace.";
      return;
    }

    entries.forEach(([taskId, task]) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "task-card";
      button.dataset.taskId = taskId;
      button.innerHTML = `
        <span class="task-id">${taskId}</span>
        <strong>${task.title || "Untitled task"}</strong>
        <span>${task.status || "unknown"}</span>
      `;
      button.addEventListener("click", () => inspectActions(taskId));
      taskList.appendChild(button);
    });
  }

  function renderActions(payload) {
    const actionCard = byId("action-card");
    const actions = payload.available_actions || {};
    const reasons = payload.reasons || {};

    actionCard.className = "action-card";
    actionCard.innerHTML = "";

    const heading = document.createElement("strong");
    heading.textContent = payload.exists
      ? `${payload.task_id} · ${payload.status}`
      : `${payload.task_id} · missing`;
    actionCard.appendChild(heading);

    const list = document.createElement("ul");
    Object.entries(actions).forEach(([action, allowed]) => {
      const item = document.createElement("li");
      item.className = allowed ? "allowed-action" : "blocked-action";
      item.textContent = `${allowed ? "available" : "blocked"}: ${action} — ${reasons[action] || "No reason provided."}`;
      list.appendChild(item);
    });
    actionCard.appendChild(list);
  }

  async function inspectActions(taskId) {
    const safeTaskId = String(taskId || "").trim();
    if (!safeTaskId || safeTaskId.includes("/") || safeTaskId.includes("\\")) {
      const actionCard = byId("action-card");
      actionCard.className = "action-card danger";
      actionCard.textContent = "Task ID must be a single path segment.";
      return;
    }

    byId("task-id-input").value = safeTaskId;
    const payload = await readJson(`/actions/${encodeURIComponent(safeTaskId)}`);
    renderActions(payload);
  }

  async function refreshDashboard() {
    const healthCard = byId("health-card");
    try {
      healthCard.className = "status-card muted";
      healthCard.textContent = "Loading read-only API data...";

      const [health, summary, kanban] = await Promise.all([
        readJson("/health"),
        readJson("/summary"),
        readJson("/kanban"),
      ]);

      renderHealth(health);
      renderSummary(summary);
      renderKanban(kanban);
    } catch (error) {
      renderError(healthCard, error);
    }
  }

  function boot() {
    renderList(byId("boundary-list"), FORBIDDEN_CAPABILITIES);
    renderList(byId("endpoint-list"), READ_ONLY_ENDPOINTS);

    byId("refresh-button").addEventListener("click", refreshDashboard);
    byId("task-id-input").addEventListener("change", (event) => {
      inspectActions(event.target.value).catch((error) => renderError(byId("action-card"), error));
    });

    refreshDashboard();
  }

  document.addEventListener("DOMContentLoaded", boot);
})();
