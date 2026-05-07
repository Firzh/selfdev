# SelfDev UI Tooling and Web Wrapper Decision

**Project:** SelfDev standalone multi-agent system  
**Module:** UI, API surface, desktop wrapper, and operator tooling  
**Status:** revised tooling plan  
**Version:** v0.1  
**Date:** 2026-05-07  

---

## 1. Purpose

This document defines UI-related tooling for SelfDev.

It covers:

```text
frontend tooling
backend API tooling
schema tooling
artifact viewer tooling
diff viewer tooling
workflow graph tooling
redaction tooling
desktop wrapper tooling
PWA tooling
test tooling
security controls
```

SelfDev UI is not a core agent. It is an operator console.

---

## 2. Recommended Technical Stack

### 2.1 Default stack

```yaml
ui_stack:
  frontend:
    framework: React
    language: TypeScript
    build_tool: Vite
    styling: Tailwind CSS
    component_policy: small local components first

  backend_api:
    framework: FastAPI
    language: Python
    data_source: file_based_workspace
    binding: 127.0.0.1

  desktop_wrapper:
    default: Tauri
    fallback: PWA
    alternative: Electron
    windows_specific: WebView2

  state:
    source_of_truth:
      - data/agent_workspace/state
      - data/agent_workspace/kanban
      - data/agent_workspace/artifacts
      - data/agent_workspace/reviews
      - data/agent_workspace/verification
      - data/agent_workspace/safety

  realtime:
    phase_1: polling
    phase_2: server_sent_events
    phase_3: websocket_if_needed
```

---

## 3. Why Web First

Web first is recommended because:

```text
fast iteration
debuggable in browser
reuses same UI in Tauri, Electron, or PWA
does not lock SelfDev to a desktop runtime
can work in WSL or local machine
fits file-based workspace
```

Desktop wrapper should be packaging, not architecture.

---

## 4. Wrapper Decision Matrix

| Option | Strength | Weakness | Best Use |
|---|---|---|---|
| Local Web App | fastest development, easy debug, no wrapper lock-in | needs browser | phase 1 default |
| PWA | installable, light, same web app | limited native capabilities | simple app shortcut |
| Tauri | small, local-first, web stack reuse, native shell via Rust boundary | Rust toolchain adds complexity | recommended desktop wrapper |
| Electron | mature, Node and Chromium ecosystem | heavier package and larger attack surface | JS-only desktop app |
| WebView2 | good Windows integration | Windows-centric and runtime dependency | Windows-only deployment |

Recommendation:

```text
Use local web app first.
Add PWA installability if useful.
Adopt Tauri after API and workflow stabilize.
Keep Electron only as fallback.
Use WebView2 only for Windows-first packaging.
```

---

## 5. UI Tool Categories

```yaml
ui_tool_categories:
  read_tools:
    - read_workspace_state
    - read_kanban
    - read_agent_registry
    - read_tool_registry
    - read_artifact_index
    - read_review_report
    - read_safety_report
    - read_verification_report
    - read_runner_report
    - read_audit_log

  write_request_tools:
    - create_manifest_draft
    - validate_manifest_request
    - submit_task_request
    - request_revision
    - request_specialist_review
    - request_runner_action
    - request_commit_gate
    - approve_human_gate
    - reject_human_gate

  render_tools:
    - render_markdown
    - render_diff
    - render_workflow_graph
    - render_json
    - render_yaml
    - render_log_excerpt

  safety_tools:
    - redact_sensitive_content
    - check_artifact_path
    - check_action_availability
    - check_artifact_hash
    - write_audit_event
```

---

## 6. UI Must Not Have These Tools

```yaml
ui_denied_tools:
  - run_shell
  - apply_patch
  - run_tests_directly
  - run_scanner_directly
  - git_commit_directly
  - git_push
  - git_merge
  - git_rebase
  - git_reset_hard
  - deploy
  - restart_service
  - modify_env
  - read_secret
  - delete_file
  - modify_agent_permission_directly
  - modify_tool_permission_directly
```

UI can request actions. Backend and core tools decide.

---

## 7. Backend API Tooling

### 7.1 FastAPI routes

```text
selfdev/api/routes/
├── health.py
├── targets.py
├── manifests.py
├── kanban.py
├── agents.py
├── tools.py
├── artifacts.py
├── reviews.py
├── safety.py
├── runner.py
├── verification.py
├── approvals.py
└── audit.py
```

### 7.2 Backend services

```text
selfdev/api/services/
├── workspace_reader.py
├── target_registry_service.py
├── manifest_service.py
├── kanban_service.py
├── agent_registry_service.py
├── tool_registry_service.py
├── artifact_service.py
├── review_service.py
├── redaction_service.py
├── approval_service.py
├── audit_service.py
└── event_stream.py
```

### 7.3 Backend policies

```text
selfdev/api/policies/
├── api_action_policy.py
├── artifact_path_policy.py
├── approval_policy.py
├── redaction_policy.py
├── ui_role_policy.py
└── desktop_permission_policy.py
```

---

## 8. Frontend Tooling

### 8.1 Suggested folder

```text
selfdev/ui/web/
├── src/
│   ├── app/
│   ├── components/
│   ├── pages/
│   ├── features/
│   │   ├── dashboard/
│   │   ├── targets/
│   │   ├── manifests/
│   │   ├── kanban/
│   │   ├── workflow/
│   │   ├── agents/
│   │   ├── tools/
│   │   ├── artifacts/
│   │   ├── reviews/
│   │   ├── safety/
│   │   ├── verification/
│   │   ├── approvals/
│   │   └── settings/
│   ├── lib/
│   │   ├── api.ts
│   │   ├── schemas.ts
│   │   ├── redaction.ts
│   │   └── status.ts
│   └── styles/
│
├── public/
├── package.json
├── tsconfig.json
└── vite.config.ts
```

### 8.2 Frontend libraries

Recommended minimal choices:

```yaml
frontend_libraries:
  required:
    - react
    - typescript
    - vite

  optional:
    - zod
    - react-router
    - tanstack-query
    - tailwindcss
    - lucide-react

  defer_until_needed:
    - complex graph library
    - Monaco editor
    - heavy markdown editor
    - websocket state library
```

Reason:

```text
Start small.
Avoid UI dependency creep.
Render artifacts, do not edit everything.
```

---

## 9. Markdown and Artifact Viewer Tooling

### 9.1 Artifact viewer

Capabilities:

```text
Markdown preview
raw text view
JSON view
YAML view
diff view
log view
download artifact
copy artifact path
```

Required safety:

```text
redaction before preview
path allow-list
artifact hash display
large file warning
no inline execution
```

### 9.2 Markdown rendering rule

Markdown must be rendered as content, not executed.

Block:

```text
HTML script execution
remote image loading by default
unsafe link auto-open
embedded iframes
```

---

## 10. Diff Viewer Tooling

Minimum features:

```text
file list
added and removed lines
path status
scope status
secret pattern warning
dependency file warning
DevOps file warning
security-sensitive file warning
test file warning
```

Risk badges:

```text
docs_only
code_change
test_change
security_sensitive
devops_sensitive
dependency_change
denied_path
secret_like
large_patch
```

---

## 11. Workflow Graph Tooling

Phase 1:

```text
simple vertical timeline
```

Phase 2:

```text
node graph with statuses
```

Graph nodes:

```text
Manifest
Siwa
Opung
Adit
Asep
Doni
Supri
Senior Reviewer
Safety Gate
Runner
Verification Engine
Commit Gate
Human Owner
```

Avoid complex graph engine in phase 1.

---

## 12. Redaction Tooling

### 12.1 Redaction service

Backend service:

```text
selfdev/api/services/redaction_service.py
```

Patterns:

```text
API keys
tokens
password assignments
authorization headers
cookies
private key blocks
database URLs
session IDs
personal data if not needed
```

Output labels:

```text
[REDACTED_TOKEN]
[REDACTED_SECRET]
[REDACTED_PRIVATE_KEY]
[REDACTED_AUTH_HEADER]
[REDACTED_COOKIE]
[REDACTED_DATABASE_URL]
[REDACTED_PERSONAL_DATA]
```

### 12.2 UI display rule

UI must show:

```text
redaction applied
number of redacted items
artifact path
hash of original artifact if available
```

Never show original secret in UI.

---

## 13. Approval Tooling

### 13.1 Human approval object

```yaml
approval_request:
  approval_id:
  task_id:
  target_id:
  requested_by:
  action_type:
  risk_level:
  reason:
  affected_files:
  evidence_artifacts:
  required_reviews:
  artifact_hashes:
  status:
  created_at:
```

### 13.2 Approval actions

```text
approve
reject
request_more_evidence
request_specialist_review
convert_to_manual_work
```

### 13.3 Approval guard

Approval allowed only if:

```text
manifest valid
artifact hash available
required evidence displayed
risk shown
audit event ready
```

---

## 14. Desktop Wrapper Tooling

### 14.1 Tauri wrapper folder

```text
selfdev/ui/desktop/tauri/
├── src-tauri/
├── package.json
├── tauri.conf.json
└── README.md
```

### 14.2 Tauri allowed capabilities

```yaml
tauri_capabilities:
  allowed:
    - open_main_window
    - check_local_api_health
    - open_file_dialog_for_target_registration
    - open_artifact_folder_if_policy_allows

  denied:
    - run_arbitrary_shell
    - modify_file_directly
    - read_env
    - read_secret
    - apply_patch
    - git_commit
    - git_push
    - restart_service
```

### 14.3 Electron wrapper folder

```text
selfdev/ui/desktop/electron/
├── main/
├── preload/
├── renderer/
└── README.md
```

Electron security defaults:

```yaml
electron_security:
  nodeIntegration: false
  contextIsolation: true
  sandbox: true
  enableRemoteModule: false
  shell_openExternal_policy: allowlist_only
  preload_api: minimal
```

### 14.4 WebView2 wrapper folder

```text
selfdev/ui/desktop/webview2/
├── src/
├── README.md
└── webview2_policy.md
```

WebView2 use case:

```text
Windows-focused packaged app only.
```

---

## 15. PWA Tooling

PWA is optional.

Files:

```text
selfdev/ui/web/public/manifest.webmanifest
selfdev/ui/web/public/icons/
selfdev/ui/web/src/service-worker.ts
```

Use only for:

```text
installable shortcut
offline static shell
quick access
```

Avoid caching:

```text
sensitive artifacts
logs
reviews
secrets
runner output
verification output
```

PWA cache policy:

```text
cache UI shell only
never cache artifact content by default
```

---

## 16. API Action Availability Model

Backend should return allowed actions per task.

Example:

```json
{
  "task_id": "task-001",
  "available_actions": {
    "submit": false,
    "request_revision": true,
    "approve_for_runner": false,
    "request_commit": false,
    "reject": true
  },
  "reasons": {
    "approve_for_runner": "Senior Reviewer approval missing",
    "request_commit": "Verification Engine has not passed"
  }
}
```

UI must not compute authority alone.

---

## 17. Audit Tooling

Audit event:

```yaml
audit_event:
  event_id:
  task_id:
  target_id:
  actor:
  action:
  risk_level:
  before_state:
  after_state:
  artifact_hashes:
  timestamp:
  result:
  reason:
```

Audit log path:

```text
data/agent_workspace/audit/{task_id}.audit.jsonl
```

Required audited actions:

```text
manifest submit
task dispatch
revision request
specialist review request
human approval
human rejection
runner request
commit request
settings change
target registration
```

---

## 18. UI Testing Tooling

### 18.1 Backend tests

```text
test_health_api
test_targets_api
test_manifest_validation_api
test_artifact_path_policy
test_redaction_service
test_approval_policy
test_action_availability
test_audit_event_written
```

### 18.2 Frontend tests

```text
test_dashboard_renders
test_manifest_builder_blocks_invalid
test_kanban_shows_status
test_artifact_viewer_redacts
test_diff_viewer_shows_risk_badges
test_approval_modal_requires_confirmation
test_commit_button_disabled_until_pass
```

### 18.3 Desktop wrapper tests

```text
test_wrapper_opens_ui
test_wrapper_checks_local_api
test_wrapper_cannot_run_shell
test_wrapper_cannot_read_env
test_wrapper_cannot_apply_patch
```

---

## 19. Development Phases

```text
Phase 0: Data contract and route list
Phase 1: Read-only backend API
Phase 2: Read-only dashboard
Phase 3: Artifact and review viewer
Phase 4: Manifest builder
Phase 5: Approval center
Phase 6: Runner and verification request UI
Phase 7: Commit readiness UI
Phase 8: PWA packaging
Phase 9: Tauri wrapper prototype
Phase 10: Desktop wrapper security review
```

---

## 20. Final Tooling Recommendation

Recommended path:

```text
FastAPI backend
React + TypeScript + Vite frontend
Tailwind CSS
file-based workspace adapter
backend redaction service
simple polling first
Tauri wrapper later
PWA optional
Electron fallback
WebView2 Windows-only
```

Most important rule:

```text
UI must not become the executor.
UI is the control panel.
Core tools remain the only execution layer.
```
