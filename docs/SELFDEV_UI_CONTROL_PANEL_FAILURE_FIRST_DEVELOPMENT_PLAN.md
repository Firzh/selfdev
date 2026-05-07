# SelfDev UI Control Panel Failure-First Development Plan

**Project:** `selfdev` standalone local multi-agent self-development system  
**Module:** UI Control Panel / Operator Console  
**Status:** development plan  
**Version:** v0.1  
**Date:** 2026-05-07  
**Scope:** desain tampilan, workflow dashboard, operator console, web local app, dan opsi desktop wrapper  
**Position:** bukan agent utama, tetapi human-facing control surface untuk SelfDev  

---

## 0. Executive Summary

UI Control Panel adalah antarmuka manusia untuk mengendalikan, memantau, dan mengaudit sistem SelfDev.

UI ini tidak boleh menjadi executor bebas.

UI harus menjadi lapisan aman untuk:

```text
melihat status sistem
membuat task manifest
memvalidasi manifest
mengirim task ke Siwa
melihat Kanban
melihat inbox dan outbox agent
melihat artifact
melihat review
melihat Safety Gate
melihat Runner report
melihat Verification Engine report
memberi human approval
menolak high-risk action
membuat commit request melalui Commit Gate
```

UI tidak boleh:

```text
menjalankan shell langsung
apply patch langsung
commit langsung
push
merge
release
deploy
modify .env
read secret
mengubah tool permission tanpa human approval
menghapus artifact tanpa audit
bypass Safety Gate
bypass Senior Reviewer
bypass Verification Engine
```

Rekomendasi teknis utama:

```text
Phase awal: local web app
Packaging lanjut: Tauri desktop wrapper
Fallback ringan: PWA
Alternatif berat: Electron
Windows-only option: WebView2 wrapper
```

Alasan:

```text
SelfDev adalah sistem lokal yang butuh audit, state, artifact, dan approval.
UI harus mudah dibuka di browser selama development.
Desktop wrapper baru dipakai setelah workflow stabil.
```

---

## 1. Position in SelfDev Architecture

SelfDev sekarang berdiri sebagai sistem mandiri.

AI RAG Local bukan fondasi utama SelfDev. AI RAG Local menjadi target awal yang dikembangkan dan dimaintain oleh SelfDev.

Hubungan:

```text
SelfDev
  ├── manages ai-rag-local
  ├── can manage other local projects
  ├── can manage documentation systems
  ├── can manage DevOps configs
  ├── can manage runtime procedures
  └── can manage future agent systems
```

UI Control Panel berada di sisi operator.

```text
Human Owner
  ↓
UI Control Panel
  ↓
SelfDev API Layer
  ↓
Siwa Miwa
  ↓
Specialist Agents
  ├── Opung
  ├── Adit
  ├── Asep
  ├── Doni
  └── Supri
  ↓
Senior Reviewer
  ↓
Safety Gate
  ↓
Runner
  ↓
Verification Engine
  ↓
Commit Gate
```

UI tidak mengganti Siwa, Senior Reviewer, Safety Gate, Runner, Verification Engine, atau Commit Gate.

UI hanya menyediakan interaction surface.

---

## 2. Design Principle

UI harus mengikuti prinsip failure-first.

Asumsi:

```text
User bisa salah klik.
Agent bisa salah output.
Artifact bisa hilang.
Patch bisa menyentuh denied path.
Approval bisa terlalu cepat.
Log bisa mengandung secret.
Runner bisa gagal.
Verification bisa gagal.
```

Maka UI harus:

```text
menampilkan risiko sebelum aksi
memisahkan read-only dan action mode
membutuhkan konfirmasi untuk high-risk action
menampilkan evidence
menampilkan status gate
menampilkan missing artifact
menampilkan failed verification
mencegah aksi tanpa manifest valid
mencegah approval tanpa review lengkap
mencegah commit request tanpa Verification PASS
menyensor secret dalam log
menyimpan audit trail
```

---

## 3. UI Role Boundary

### 3.1 UI boleh

```text
create task manifest draft
edit task manifest draft
validate task manifest
submit task to Siwa
show agent registry
show tool grants
show Kanban
show workflow graph
show artifacts
show diff preview
show review reports
show safety report
show verification report
show runner report
show commit readiness
approve human-gated action
reject human-gated action
request revision
request specialist review
download artifact bundle
export run summary
```

### 3.2 UI tidak boleh

```text
execute shell command directly
apply patch directly
run test directly
run scanner directly
deploy directly
restart service directly
commit directly
push directly
merge directly
release directly
modify .env
read secrets
edit denied paths
change agent permission without policy
override Safety Gate
override Senior Reviewer
override Verification Engine
```

### 3.3 UI action rule

All actions must go through backend API.

```text
UI button
  ↓
API request
  ↓
policy check
  ↓
Safety Gate
  ↓
allowed runtime component
  ↓
audit log
```

No frontend-only decision is trusted.

---

## 4. Recommended UI Strategy

### 4.1 Phase 1: Local Web App First

Use a local web app served by SelfDev.

Suggested stack:

```text
Frontend:
- React or simple HTML/HTMX
- TypeScript if complexity grows
- Tailwind CSS or simple CSS variables
- shadcn/ui optional only if React is selected

Backend:
- FastAPI
- file-based SelfDev workspace adapter
- read-only endpoints first
- action endpoints later with gate checks

Runtime:
- localhost only
- no public binding by default
- no auth in early local-only phase, but API token can be added later
```

Why web first:

```text
faster iteration
easy debugging
same UI can later be wrapped
can run in browser
does not lock SelfDev to desktop framework
```

---

### 4.2 Phase 2: PWA Installable App

PWA can be added if the local web app is stable.

Use when:

```text
operator wants app-like shortcut
offline shell is useful
desktop install is enough
native system access is not needed
```

Avoid when:

```text
native file system control is needed
process control is needed
deep OS integration is needed
packaged distribution is required
```

PWA still talks to local SelfDev API.

---

### 4.3 Phase 3: Desktop Wrapper

Use desktop wrapper only after:

```text
manifest flow is stable
Kanban flow is stable
artifact viewer is stable
Safety Gate is stable
approval flow is stable
Runner API is stable
Verification Engine report format is stable
```

Recommended default:

```text
Tauri wrapper
```

Reason:

```text
small footprint
web UI reuse
local-first fit
Rust backend boundary
good for local desktop tooling
```

Alternative:

```text
Electron
```

Use Electron if:

```text
Node.js ecosystem is required
Chromium consistency is more important than binary size
frontend team prefers JS-only desktop stack
```

Windows-specific option:

```text
WebView2
```

Use WebView2 if:

```text
target is Windows only
integration with Windows desktop is required
the team accepts Microsoft Edge WebView2 runtime dependency
```

---

## 5. UI Architecture

```text
selfdev/
├── ui/
│   ├── web/
│   │   ├── src/
│   │   ├── public/
│   │   ├── package.json
│   │   └── vite.config.ts
│   │
│   ├── desktop/
│   │   ├── tauri/
│   │   ├── electron/
│   │   └── webview2/
│   │
│   └── shared/
│       ├── schemas/
│       ├── api-client/
│       ├── types/
│       └── design-system/
│
├── api/
│   ├── main.py
│   ├── routes/
│   │   ├── health.py
│   │   ├── targets.py
│   │   ├── manifests.py
│   │   ├── kanban.py
│   │   ├── agents.py
│   │   ├── tools.py
│   │   ├── artifacts.py
│   │   ├── reviews.py
│   │   ├── safety.py
│   │   ├── runner.py
│   │   ├── verification.py
│   │   ├── approvals.py
│   │   └── audit.py
│   │
│   ├── services/
│   │   ├── workspace_reader.py
│   │   ├── manifest_service.py
│   │   ├── artifact_service.py
│   │   ├── redaction_service.py
│   │   ├── approval_service.py
│   │   └── event_stream.py
│   │
│   └── schemas/
│       ├── manifest_api.py
│       ├── kanban_api.py
│       ├── artifact_api.py
│       └── approval_api.py
```

Recommended repository placement:

```text
selfdev/ui/
selfdev/api/
```

Reason:

```text
UI belongs to SelfDev, not ai-rag-local.
AI RAG Local can be shown as a target system inside the UI.
```

---

## 6. Target System Concept in UI

Since SelfDev is not only for AI RAG Local, UI must have target system selection.

### 6.1 Target Registry Page

The UI should show managed systems:

```text
ai-rag-local
selfdev-core
anki-japanese-learning
future-project-x
```

Each target has:

```yaml
target_id:
name:
root_path:
type:
status:
allowed_paths:
denied_paths:
branch_policy:
test_profiles:
docs_profiles:
devops_profiles:
runtime_profiles:
```

### 6.2 Target Detail Page

Fields:

```text
Target overview
Repository path
Current branch
Last task
Open tasks
Recent failures
Agent coverage
Allowed paths
Denied paths
Configured checks
Known risks
```

### 6.3 Cross-target rule

UI must never let an agent read or modify another target unless the task manifest explicitly allows it.

---

## 7. Core UI Pages

### 7.1 Dashboard

Purpose:

```text
show system health and current work state
```

Widgets:

```text
SelfDev status
Active target system
Open tasks
Blocked tasks
Human approval needed
Verification failures
Safety blocks
Runner failures
Recent commits ready
Agent health
Core tools health
```

Status cards:

```text
green: healthy
yellow: needs attention
red: blocked
gray: unavailable
```

No decorative complexity in early phase.

---

### 7.2 Task Manifest Builder

Purpose:

```text
make valid task manifest without hand-writing YAML every time
```

Form sections:

```text
Basic info
Target system
Task type
Objective
Risk level
Mode
Allowed paths
Denied paths
Required outputs
Required reviewers
Validation required
Stop conditions
Human gate required
```

Actions:

```text
Save draft
Validate manifest
Submit to Siwa
Export YAML
Import YAML
```

Failure-first behavior:

```text
cannot submit invalid manifest
warn if allowed_paths too broad
warn if denied_paths missing
warn if risk level conflicts with task type
warn if dependency change lacks Doni review
warn if security task lacks Asep review
warn if implementation lacks Senior Reviewer
```

---

### 7.3 Kanban Board

Purpose:

```text
visualize task state
```

Columns:

```text
todo
picked
in_progress
blocked
needs_review
needs_revision
ready_for_senior
ready_for_verification
verification_failed
verified
commit_ready
done
rejected
human_required
```

Card fields:

```text
task_id
title
target system
owner agent
risk level
status
blocked by
missing artifacts
last update
```

Actions:

```text
open task detail
view artifacts
view messages
view blockers
request revision
```

UI must not drag task into unsafe state without backend validation.

---

### 7.4 Workflow Graph

Purpose:

```text
show execution path and current stage
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

Node status:

```text
not_started
in_progress
completed
failed
blocked
skipped
human_required
```

Graph must show:

```text
current node
failed node
missing artifact
next required action
human gate
```

---

### 7.5 Agent Registry Page

Purpose:

```text
show agent roles, models, permission, and status
```

Agent cards:

```text
Siwa Miwa
Opung
Adit
Asep
Doni
Supri
Senior Reviewer
```

Each card shows:

```text
role
model
temperature
allowed tools
denied tools
current task
last output
last error
performance warning
```

No edit permission in early phase.

Editing agent config should require:

```text
human owner confirmation
Asep review for permission change
Senior Reviewer review
Safety Gate pass
```

---

### 7.6 Tool Registry Page

Purpose:

```text
show tools and risk levels
```

Tool groups:

```text
read tools
write artifact tools
orchestration tools
request tools
execution tools
core tools
```

Core tools:

```text
Runner
Verification Engine
Safety Gate
Commit Gate
```

For each tool:

```text
tool_id
category
risk level
allowed callers
requires gate
requires human approval
denied actions
recent failures
```

UI must clearly mark execution tools as high risk.

---

### 7.7 Message Bus Viewer

Purpose:

```text
debug agent handoff without opening raw files
```

Views:

```text
agent inbox
agent outbox
message timeline
task assignment
artifact ready
revision request
review request
human escalation
```

Message fields:

```text
message_id
run_id
task_id
from_agent
to_agent
message_type
created_at
status
required_outputs
stop_conditions
artifact paths
```

Sensitive content must be redacted.

---

### 7.8 Artifact Browser

Purpose:

```text
view generated outputs safely
```

Artifact types:

```text
orchestration plan
implementation plan
draft patch
docs plan
docs patch
security review
DevOps review
runtime summary
senior review
safety report
runner report
verification report
commit request
error report
performance warning
```

Features:

```text
Markdown preview
raw view
download artifact
copy path
artifact completeness indicator
linked task
linked agent
linked gate result
```

Blocked:

```text
direct edit artifact in early phase
delete artifact without audit
view secret file
view denied path file
```

---

### 7.9 Diff and Patch Viewer

Purpose:

```text
review patches before Runner apply
```

Features:

```text
changed file list
line-level diff
allowed path indicator
denied path warning
patch size indicator
secret pattern warning
dependency change indicator
test change indicator
config change indicator
```

Actions:

```text
approve for Senior review
request revision
request Asep review
request Doni review
request Adit review
request Supri review
```

UI must not allow direct apply patch.

---

### 7.10 Review Center

Purpose:

```text
centralize review and approval
```

Sections:

```text
Opung implementation notes
Adit documentation review
Asep security review
Doni DevOps review
Supri runtime summary
Senior Reviewer decision
Safety Gate report
Verification Engine report
Runner report
```

Decision buttons:

```text
Request Revision
Request Specialist Review
Approve for Runner
Reject
Escalate to Human Owner
Request Commit
```

Buttons must be hidden or disabled if prerequisites fail.

---

### 7.11 Human Approval Center

Purpose:

```text
handle high-risk actions intentionally
```

Approval types:

```text
dependency change
tool permission change
agent permission change
architecture change
commit policy change
security policy change
Runner high-risk validation
terraform plan
active scanner request
desktop wrapper native capability
deployment
push
merge
release
```

Approval screen must show:

```text
request reason
trigger
risk level
affected files
required reviewers
available evidence
recommended action
rollback notes
audit log impact
```

No one-click high-risk approval.

Use two-step confirmation:

```text
1. Review evidence
2. Confirm exact action
```

---

### 7.12 Verification Center

Purpose:

```text
show deterministic validation status
```

Checks:

```text
manifest schema
message schema
artifact schema
denied path
secret pattern
patch scope
dependency change
unit tests
compile check
docs check
OpenAPI validation
AsyncAPI validation
YAML validation
Docker Compose config
Terraform validate
Kubernetes dry-run client
security validation results
```

Result types:

```text
PASS
FAIL
BLOCKED
SKIPPED
PENDING
```

Commit Gate requires blocking checks to pass.

---

### 7.13 Safety Center

Purpose:

```text
show policy blocks and risk decisions
```

Sections:

```text
denied path blocks
secret detection
unsafe command detection
tool misuse
agent permission escalation
dependency risk
network scan risk
deployment risk
Commit Gate bypass attempt
Senior Reviewer bypass attempt
```

Safety Center should be read-only.

Only Human Owner can resolve safety escalations.

---

### 7.14 Commit Readiness Page

Purpose:

```text
show whether a local commit is allowed
```

Checklist:

```text
manifest valid
all required artifacts present
Senior Reviewer approved
Safety Gate PASS
Runner report PASS
Verification Engine PASS
Asep not blocking
Doni not blocking
allowed paths only
commit message valid
push disabled
```

Allowed action:

```text
request Commit Gate local commit
```

Not allowed:

```text
push
merge
release
tag
```

---

### 7.15 Settings Page

Purpose:

```text
manage safe UI preferences and local config visibility
```

Allowed settings:

```text
theme
default target
dashboard refresh interval
artifact preview mode
redaction display mode
local API endpoint
```

Restricted settings:

```text
agent tool grants
Safety Gate policy
Commit Gate policy
Runner allowed actions
target root paths
```

Restricted settings require manifest-driven change.

---

## 8. UI Security Model

### 8.1 Local-only default

Default API binding:

```text
127.0.0.1
```

Avoid:

```text
0.0.0.0 by default
public tunnel by default
cloud sync by default
```

### 8.2 Authentication

Phase 1:

```text
local-only and localhost binding
```

Phase 2:

```text
local API token
```

Phase 3:

```text
user session
role-based UI
audit trail
```

### 8.3 Redaction

UI must redact:

```text
tokens
passwords
private keys
session IDs
authorization headers
cookies
API keys
database URLs
personal data if not needed
```

Redaction format:

```text
[REDACTED_TOKEN]
[REDACTED_SECRET]
[REDACTED_PERSONAL_DATA]
```

### 8.4 Dangerous content display

UI must warn before showing:

```text
full log
diff with secret-like pattern
security report with exploit context
runner stderr
unredacted artifact
```

### 8.5 Desktop wrapper native permissions

Desktop wrapper must not automatically gain high-risk OS permissions.

Native capabilities must be explicit:

```yaml
desktop_native_permissions:
  file_dialog:
    allowed: true
    risk: low

  open_folder:
    allowed: true
    risk: medium

  run_command:
    allowed: false
    risk: critical

  modify_file:
    allowed: false
    risk: high

  read_secret:
    allowed: false
    risk: critical
```

---

## 9. API Surface

### 9.1 Read-only APIs first

Initial endpoints:

```text
GET /health
GET /targets
GET /targets/{target_id}
GET /kanban
GET /tasks/{task_id}
GET /tasks/{task_id}/timeline
GET /agents
GET /agents/{agent_id}
GET /tools
GET /artifacts
GET /artifacts/{artifact_id}
GET /reviews/{task_id}
GET /safety/{task_id}
GET /verification/{task_id}
GET /runner/{task_id}
GET /audit
```

### 9.2 Controlled action APIs

Add only after read-only UI is stable:

```text
POST /manifests/draft
POST /manifests/validate
POST /tasks/submit
POST /tasks/{task_id}/request-revision
POST /tasks/{task_id}/request-specialist-review
POST /approvals/{task_id}/approve
POST /approvals/{task_id}/reject
POST /runner/request
POST /commit/request
```

### 9.3 Forbidden frontend operations

```text
direct file write from browser
direct shell execution
direct patch apply
direct commit
direct push
direct secret read
```

---

## 10. Event and Refresh Model

Phase 1:

```text
polling every 2 to 5 seconds
```

Phase 2:

```text
Server-Sent Events for task updates
```

Phase 3:

```text
WebSocket only if real-time interaction becomes necessary
```

Preferred initial event model:

```text
simple polling
stable file-based state
low complexity
```

---

## 11. Data Contracts

### 11.1 Task summary for UI

```json
{
  "task_id": "task-001",
  "title": "Update docs",
  "target_id": "ai-rag-local",
  "task_type": "documentation",
  "risk_level": "low",
  "status": "needs_review",
  "owner_agent": "adit",
  "required_reviewers": ["senior_reviewer"],
  "missing_artifacts": [],
  "blocked_by": [],
  "last_updated": "2026-05-07T10:00:00Z"
}
```

### 11.2 Gate summary

```json
{
  "task_id": "task-001",
  "safety": "PASS",
  "runner": "PENDING",
  "verification": "PENDING",
  "senior_review": "PENDING",
  "commit_gate": "BLOCKED"
}
```

### 11.3 Artifact summary

```json
{
  "artifact_id": "artifact-001",
  "task_id": "task-001",
  "agent_id": "adit",
  "type": "docs_plan",
  "path": "data/agent_workspace/docs/task-001.adit_docs_plan.md",
  "exists": true,
  "size_bytes": 12040,
  "redaction_status": "clean",
  "created_at": "2026-05-07T10:00:00Z"
}
```

### 11.4 Approval request

```json
{
  "approval_id": "approval-001",
  "task_id": "task-001",
  "action": "dependency_change",
  "risk_level": "high",
  "requested_by": "siwa",
  "required_reviewers": ["asep", "doni", "senior_reviewer"],
  "evidence_artifacts": [],
  "status": "pending_human"
}
```

---

## 12. UI State Machine

### 12.1 Task UI State

```text
draft
validated
submitted
routed
in_progress
waiting_for_artifact
waiting_for_review
waiting_for_human
waiting_for_runner
waiting_for_verification
verified
commit_ready
done
blocked
rejected
```

### 12.2 Button state rule

Buttons must follow state.

Example:

```text
Submit Task:
enabled only if manifest_valid = true

Approve for Runner:
enabled only if Senior Reviewer decision allows it

Request Commit:
enabled only if Safety PASS, Runner PASS, Verification PASS

Push:
never available
```

---

## 13. UI Failure Taxonomy

| Failure | Example | Impact | Response |
|---|---|---|---|
| False green status | UI shows PASS while report failed | Unsafe approval | Backend status is source of truth |
| Stale state | UI shows old task status | Wrong decision | show last_updated and refresh state |
| Click misfire | User approves wrong task | High-risk action | two-step confirmation |
| Artifact confusion | User reads wrong patch | Bad review | show task_id and hash |
| Secret leak | UI renders secret from logs | Security incident | redaction service |
| Path traversal | artifact path requests escape workspace | data exposure | backend path allow-list |
| Desktop native misuse | wrapper can run command directly | critical | native command disabled |
| Broken graph | workflow graph misses block | wrong expectation | graph generated from state file |
| Overloaded dashboard | too many cards | poor triage | show only actionable items |
| Unauthorized API | remote process calls local API | risk | localhost binding and token |
| Race condition | approval while artifact changes | bad approval | artifact hash lock |
| Missing audit | no record of approval | accountability loss | audit log mandatory |

---

## 14. UI Anti-Failure Gates

UI must implement:

```text
Manifest UI Gate
Action Gate
Role Gate
Artifact Hash Gate
Redaction Gate
Approval Gate
State Freshness Gate
Path Access Gate
Desktop Permission Gate
Audit Gate
```

### 14.1 Manifest UI Gate

UI cannot submit invalid manifest.

### 14.2 Action Gate

UI cannot call action endpoint unless backend says action is available.

### 14.3 Role Gate

Only Human Owner can approve high-risk action.

### 14.4 Artifact Hash Gate

Approval must bind to artifact hash.

If artifact changes after review:

```text
approval invalidated
review required again
```

### 14.5 Redaction Gate

Artifact/log preview goes through redaction service.

### 14.6 Approval Gate

High-risk action requires evidence screen and explicit confirmation.

### 14.7 State Freshness Gate

UI must show stale status warning if state is older than threshold.

### 14.8 Path Access Gate

Artifact paths must be resolved by backend and checked against workspace allow-list.

### 14.9 Desktop Permission Gate

Native wrapper cannot bypass API policy.

### 14.10 Audit Gate

Every action writes audit record.

---

## 15. Recommended Visual Design

### 15.1 Style

Use a utilitarian operator-console style.

```text
clean
dense but readable
not flashy
high contrast
clear state colors
monospace for IDs and paths
strong separation between safe and risky actions
```

### 15.2 Layout

Recommended layout:

```text
Left sidebar:
- Dashboard
- Targets
- Tasks
- Kanban
- Workflow
- Agents
- Tools
- Artifacts
- Reviews
- Safety
- Verification
- Approvals
- Settings

Top bar:
- active target
- active branch
- SelfDev status
- approval needed count

Main content:
- contextual page
```

### 15.3 Color semantics

```text
Green = pass / done
Yellow = warning / needs review
Red = block / fail / critical
Blue = information / in progress
Gray = inactive / skipped
Purple = human approval
```

Colors must not be the only indicator. Add labels.

### 15.4 Typography

```text
Use clear sans-serif for UI.
Use monospace for:
- paths
- task IDs
- logs
- diffs
- commands
- schema
```

---

## 16. Desktop Wrapper Decision

### 16.1 Recommended path

```text
Build web app first.
Stabilize API and state.
Add Tauri wrapper later.
Keep Electron as fallback.
Use WebView2 only for Windows-focused packaging.
```

### 16.2 Tauri plan

Tauri wrapper should:

```text
load local web UI
start or detect SelfDev local API
show local API status
open artifact folder via safe file dialog
not run arbitrary shell
not bypass backend policy
```

Tauri native permissions:

```text
file dialog: allowed
open external link: allowed
start selfdev API: conditional
run arbitrary command: denied
write artifact: denied
read secret: denied
```

### 16.3 Electron plan

Electron wrapper should be considered if:

```text
team wants JS-only stack
Node integration is needed
Chromium consistency is mandatory
bundle size is acceptable
```

Electron risk controls:

```text
disable nodeIntegration in renderer
enable contextIsolation
use preload bridge with minimal API
block arbitrary shell
block filesystem access from renderer
```

### 16.4 WebView2 plan

Use only if:

```text
target deployment is Windows-first
native Windows shell is preferred
Edge WebView2 runtime dependency is acceptable
```

### 16.5 PWA plan

Use if:

```text
operator only needs installable shortcut
local web server is already running
native features are not required
```

---

## 17. Development Roadmap

### Phase 0: UI Contract Freeze

Deliverables:

```text
schemas/ui/task_summary.schema.json
schemas/ui/artifact_summary.schema.json
schemas/ui/gate_summary.schema.json
schemas/ui/approval_request.schema.json
schemas/ui/audit_event.schema.json
```

Exit criteria:

```text
UI data contracts frozen
backend routes listed
no action endpoint without policy
```

---

### Phase 1: Read-Only Dashboard

Deliverables:

```text
GET /health
GET /targets
GET /kanban
GET /agents
GET /tools
Dashboard page
Kanban page
Agent Registry page
Tool Registry page
```

Exit criteria:

```text
UI can inspect state
UI cannot mutate state
no shell
no patch apply
no commit
```

---

### Phase 2: Artifact and Review Viewer

Deliverables:

```text
Artifact Browser
Markdown Preview
Diff Viewer
Review Center
Safety Center
Verification Center
redaction service
```

Exit criteria:

```text
UI can show artifact safely
secret-like content is redacted
patch can be reviewed but not applied
```

---

### Phase 3: Manifest Builder

Deliverables:

```text
Manifest Builder
manifest validation endpoint
manifest export YAML
manifest draft save
submit to Siwa endpoint
```

Exit criteria:

```text
invalid manifest cannot be submitted
allowed_paths and denied_paths are visible
task can enter Kanban
```

---

### Phase 4: Human Approval Center

Deliverables:

```text
Approval list
Approval detail
approve/reject action
audit log
artifact hash lock
two-step confirmation
```

Exit criteria:

```text
high-risk approval requires evidence
approval binds to artifact hash
audit event created
```

---

### Phase 5: Runner and Verification Request UI

Deliverables:

```text
Runner request viewer
Verification request viewer
Runner report page
Verification report page
blocking check indicator
```

Exit criteria:

```text
UI can request only allowed actions
backend rejects unsafe requests
Verification FAIL blocks Commit Readiness
```

---

### Phase 6: Commit Readiness UI

Deliverables:

```text
Commit readiness page
commit request form
commit message preview
Commit Gate report viewer
```

Exit criteria:

```text
Commit request allowed only after all gates pass
push is not available
merge is not available
release is not available
```

---

### Phase 7: Desktop Wrapper Prototype

Deliverables:

```text
Tauri wrapper prototype
local API detection
open UI window
safe file dialog
no command execution
wrapper permission policy
```

Exit criteria:

```text
desktop app opens SelfDev UI
no native bypass exists
desktop wrapper cannot run shell
desktop wrapper cannot modify files directly
```

---

## 18. Acceptance Criteria

UI is acceptable when:

```text
can show active target systems
can show task status
can build valid manifest
can submit task to Siwa
can show Kanban
can show artifact safely
can show review reports
can show Safety Gate result
can show Runner result
can show Verification Engine result
can handle human approval
can request revision
can request commit only after all gates pass
cannot run shell
cannot apply patch directly
cannot commit directly
cannot push
cannot merge
cannot show secrets unredacted
```

---

## 19. Failure Acceptance Criteria

UI is failure-first when:

```text
invalid manifest is blocked
missing artifact is visible
failed verification is visible
Safety block is visible
high-risk action needs confirmation
approval is invalidated when artifact changes
stale state is visible
secret-like content is redacted
denied path access is blocked
desktop wrapper cannot bypass backend
all actions create audit log
```

---

## 20. Minimum Test List

```text
test_ui_health_endpoint
test_dashboard_reads_state
test_manifest_builder_blocks_invalid_manifest
test_manifest_builder_warns_broad_allowed_path
test_kanban_shows_blocked_task
test_artifact_viewer_blocks_path_traversal
test_artifact_viewer_redacts_secret
test_diff_viewer_marks_denied_path
test_review_center_blocks_missing_senior_review
test_approval_requires_two_step_confirmation
test_approval_binds_artifact_hash
test_approval_invalidated_when_artifact_changes
test_runner_request_rejects_denied_action
test_verification_fail_blocks_commit_button
test_commit_request_requires_all_gates_pass
test_push_button_never_exists
test_desktop_wrapper_cannot_run_shell
test_desktop_wrapper_cannot_modify_env
test_audit_log_created_for_action
```

---

## 21. Open Questions

```text
Should UI be React, HTMX, or plain server-rendered templates?
Should desktop wrapper start backend automatically or require backend already running?
Should SelfDev use API token from first version or localhost-only first?
Should UI support multiple users later?
Should web wrapper have file picker for target system registration?
Should artifact viewer support large files via streaming?
Should graph view be custom SVG or library-based?
```

Recommended default answers:

```text
React if long-term UI is expected.
HTMX if simpler local console is enough.
Backend should start manually in phase 1.
Desktop wrapper can auto-detect backend later.
Use localhost-only first, token later.
Single operator first.
Add file picker only after target registry is stable.
Stream large artifacts later.
Use simple graph first.
```

---

## 22. Final Recommendation

Build UI in this order:

```text
1. local web read-only dashboard
2. artifact and review viewer
3. manifest builder
4. approval center
5. runner and verification request UI
6. commit readiness UI
7. Tauri desktop wrapper
```

Do not start with Electron or full desktop app first.

The safest path is:

```text
SelfDev API + local web UI
  ↓
PWA optional
  ↓
Tauri wrapper after workflow stable
```

This keeps SelfDev flexible, auditable, and independent from AI RAG Local.
