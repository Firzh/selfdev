# Siwa Miwa Failure-First Development Plan

**Project:** `self-development-agent` untuk `ai-rag-local`  
**Agent:** Siwa Miwa  
**Model lokal:** `qwen3:4b-instruct`  
**Peran:** local multi-agent orchestrator  
**Status dokumen:** development plan  
**Tanggal:** 2026-05-05 17:54:04

---

# Ringkasan Eksekutif

Dokumen ini merancang Siwa Miwa sebagai **orchestrator agent** yang mengatur kerja agent lain secara lokal, aman, dan dapat diaudit.

Siwa Miwa tidak boleh menjadi super-agent bebas. Siwa tidak boleh menulis patch, menjalankan shell, apply patch, commit, push, merge, release, atau membaca secret. Siwa hanya mengatur task, routing, Kanban, message bus, artifact collection, evaluator ringan, dan human escalation.

Asumsi utama dokumen ini:

```text
Kemungkinan failure awal dianggap 80%.
Maka desain harus failure-first.
```

Target desain:

```text
LLM boleh salah.
Agent boleh gagal.
Referensi GitHub boleh tidak cocok.
Script boleh lambat.
Workflow boleh berhenti.

Tetapi sistem tidak boleh:
- bypass safety;
- menyentuh secret;
- push otomatis;
- commit tanpa gate;
- hilang state;
- gagal tanpa report;
- loop tanpa batas;
- mengirim task ke agent yang salah tanpa koreksi.
```

---

# Bagian A
# Pondasi Anti-Gagal Siwa Miwa

Bagian ini berisi fondasi anti-gagal. Bagian ini sengaja dipisahkan dari bagian referensi. Tujuannya agar sistem tetap aman meskipun semua referensi eksternal tidak cocok.

---

## A1. Posisi Siwa Miwa

Siwa Miwa adalah **planner-router-dispatcher-evaluator**.

Siwa bertanggung jawab untuk:

1. Membaca task manifest.
2. Memvalidasi intent task.
3. Mengklasifikasi risiko.
4. Membagi task menjadi subtask.
5. Memilih agent yang sesuai.
6. Membuat dan memperbarui Kanban task.
7. Mengirim pesan ke agent lain.
8. Mengumpulkan artifact.
9. Memvalidasi kelengkapan artifact.
10. Mengirim hasil ke Senior Reviewer.
11. Membuat human escalation jika risiko tinggi.

Siwa tidak bertanggung jawab untuk:

1. Menulis patch source code.
2. Apply patch.
3. Menjalankan shell.
4. Commit.
5. Push.
6. Merge.
7. Release.
8. Membaca `.env`.
9. Membaca secret.
10. Mengubah permission agent tanpa human approval.
11. Mengubah tool registry tanpa human approval.
12. Override Safety Gate.
13. Override Senior Reviewer.

---

## A2. Failure Taxonomy

Sistem harus menganggap failure berikut sebagai hal normal.

| Failure | Contoh | Risiko | Respons |
|---|---|---|---|
| Reference mismatch | Referensi GitHub tidak cocok dengan repo lokal | Integrasi macet | Ambil pattern saja, jangan jadikan dependency inti |
| Script inefficient | Banyak I/O, call berulang, context terlalu besar | Runtime berat | Performance budget, cache, profiling |
| Routing salah | Task dependency dikirim ke Opung, bukan Doni | Patch buruk | Routing Gate dan evaluator |
| Context salah | Agent membaca file tidak relevan | Output tidak akurat | Explicit context dan allowed paths |
| Output invalid | JSON rusak, patch tidak valid | Workflow gagal | Schema validation dan retry terbatas |
| Agent loop | Revisi berulang tanpa selesai | Waktu habis | Max iterations dan stop condition |
| Tool misuse | Agent meminta shell, commit, atau push | Risiko tinggi | Deny-list dan Safety Gate |
| Parallel conflict | Dua agent menyentuh file terkait | Conflict artifact | Kanban lock dan file ownership |
| Verification false pass | Test minim, patch tetap rusak | Bug masuk commit | Required checks dan negative tests |
| Recovery gagal | Proses berhenti tanpa state | Tidak bisa lanjut | Checkpoint, resume, replay |
| Human gate bypass | High-risk task jalan otomatis | Bahaya | Hard stop policy |

---

## A3. Core Anti-Failure Gates

Siwa harus melewati tujuh gate.

```text
Manifest Gate
Schema Gate
Routing Gate
Context Gate
Iteration Gate
Artifact Gate
Human Gate
```

### A3.1 Manifest Gate

Siwa tidak boleh bekerja tanpa manifest valid.

Field wajib:

```yaml
task_id:
title:
risk_level:
mode:
task_type:
objective:
allowed_paths:
denied_paths:
required_outputs:
required_reviews:
stop_conditions:
```

Jika field wajib hilang, workflow berhenti.

Status:

```text
manifest_invalid
```

Artifact error:

```text
data/agent_workspace/errors/{task_id}.manifest_error.md
```

### A3.2 Schema Gate

Semua output Siwa harus memakai schema tetap.

Contoh routing decision:

```json
{
  "task_id": "task-043",
  "decision": "route",
  "target_agent": "opung",
  "reason": "implementation task with limited scope",
  "required_outputs": ["plan", "draft_patch", "notes"],
  "requires_review": ["asep", "senior_reviewer"]
}
```

Jika output invalid:

```text
retry once
if still invalid, stop and create human_review_required artifact
```

### A3.3 Routing Gate

Siwa tidak boleh memilih agent secara bebas. Siwa harus membaca `routing_rules.yaml`.

Contoh:

```yaml
routing_rules:
  implementation:
    primary: opung
    required_review:
      - senior_reviewer

  dependency_change:
    primary: doni
    required_review:
      - asep
      - senior_reviewer
    requires_human_review: true

  agent_permission_change:
    primary: asep
    required_review:
      - senior_reviewer
    requires_human_review: true
```

Jika tidak ada rule yang cocok:

```text
status = human_review_required
```

### A3.4 Context Gate

Siwa hanya boleh mengirim context eksplisit ke agent.

Format context:

```yaml
context:
  manifest: data/agent_workspace/manifests/task-043.yaml
  files_allowed:
    - app/channels/base.py
    - tests/channels/test_base.py
  files_denied:
    - .env
    - .git/
    - data/secrets/
  previous_artifacts:
    - data/agent_workspace/orchestration/task-043.siwa_plan.md
```

Dilarang:

```text
dump seluruh repository
dump semua history chat
dump data Chroma raw
dump secret
```

### A3.5 Iteration Gate

Siwa tidak boleh loop tanpa batas.

```yaml
loop_policy:
  max_dispatch_rounds: 3
  max_revision_rounds: 2
  max_agent_wait_seconds: 300
  stop_on_safety_block: true
  stop_on_manifest_conflict: true
  stop_on_schema_invalid_after_retry: true
```

### A3.6 Artifact Gate

Siwa tidak boleh menganggap task selesai jika artifact belum valid.

Minimum check:

```text
file exists
file not empty
required sections exist
decision field valid
artifact path registered in Kanban
changed paths within scope
```

### A3.7 Human Gate

Siwa wajib berhenti dan meminta human decision untuk:

```text
dependency change
agent permission change
tool registry change
security policy change
architecture change
commit policy change
production data access
secret access
remote operation
push or merge request
release request
```

---

## A4. State, Checkpoint, Resume, Replay, Fork

Siwa harus menulis state pada setiap stage.

Path:

```text
data/agent_workspace/state/{task_id}.state.json
```

Contoh:

```json
{
  "task_id": "task-043",
  "run_id": "run-20260506-001",
  "stage": "waiting_for_asep_review",
  "last_successful_checkpoint": "opung_artifact_collected",
  "current_agent": "asep",
  "status": "blocked",
  "reason": "asep output schema invalid",
  "retry_count": 1
}
```

Mode recovery:

| Mode | Fungsi |
|---|---|
| `resume` | Lanjut dari checkpoint terakhir |
| `replay` | Ulang dari checkpoint tertentu |
| `fork` | Buat jalur baru dari checkpoint tertentu |

---

## A5. Degrade Gracefully Policy

Jika sistem tidak bisa menjalankan mode penuh, sistem turun level.

| Level | Mode | Kondisi |
|---|---|---|
| Level 4 | Full multi-agent with Siwa planning | Semua komponen sehat |
| Level 3 | Deterministic routing plus specialist agents | Siwa LLM gagal format |
| Level 2 | Single worker plus Senior review | Specialist review timeout |
| Level 1 | Plan-only, no patch | Verification fail atau scope tidak jelas |
| Level 0 | Human-only with generated checklist | Critical safety block |

Contoh:

| Kondisi | Turun ke |
|---|---|
| Siwa output invalid | Level 3 |
| Opung gagal patch | Level 2 |
| Asep timeout | Level 2 dengan human security review |
| Verification fail | Level 1 |
| Safety critical | Level 0 |

---

## A6. Fallback Mode untuk Siwa

Jika `qwen3:4b-instruct` gagal memberi output valid, sistem memakai deterministic router.

```yaml
siwa_fallback:
  mode: deterministic_router
  behavior:
    - read manifest
    - match task_type to routing_rules.yaml
    - create Kanban task
    - send static message template
    - skip free planning
    - require Senior review
```

Routing statis:

```yaml
task_type_map:
  docs: adit
  implementation: opung
  dependency: doni
  security: asep
  runtime: supri
  final_review: senior_reviewer
```

---

## A7. Performance Budget

Efisiensi tidak diukur dari panjang script. Efisiensi diukur dari biaya runtime.

Metrik:

```text
jumlah file read
jumlah LLM call
durasi per stage
jumlah retry
jumlah token context
jumlah disk write
jumlah subprocess call
ukuran artifact
```

Batas awal:

```yaml
performance_budget:
  max_llm_calls_per_stage: 1
  max_files_read_per_agent: 8
  max_context_chars: 24000
  max_stage_duration_seconds: 60
  max_total_runtime_seconds: 900
```

Jika batas terlampaui, tulis:

```text
data/agent_workspace/performance/{task_id}.performance_warning.md
```

Contoh log:

```json
{
  "task_id": "task-043",
  "stage": "siwa_routing",
  "duration_ms": 812,
  "llm_calls": 1,
  "files_read": 3,
  "tokens_estimated": 2400,
  "artifacts_written": 2,
  "retry_count": 0
}
```

---

## A8. Failure Handling Matrix

| Failure | Deteksi | Tindakan otomatis | Tindakan akhir |
|---|---|---|---|
| Manifest invalid | Schema validation | Stop | Human fix manifest |
| Routing tidak cocok | No rule matched | Stop | Human classify task |
| Agent timeout | Timeout counter | Retry 1 kali | Mark blocked |
| Output JSON rusak | Schema fail | Retry 1 kali | Human review |
| Patch tidak valid | `git apply --check` fail | Request revision | Senior decides |
| Denied path tersentuh | Path scan | Block | Human review |
| Secret terdeteksi | Secret scan | Critical block | Human review |
| Loop revisi | Revision count exceeded | Stop | Human gate |
| Verification fail | Test fail | Mark needs_revision | Senior decides |
| Agent conflict | File ownership conflict | Block subtasks | Siwa reschedules |
| Model hallucination | Artifact evidence missing | Request revision | Senior decides |
| Script lambat | Duration threshold | Write performance report | Optimize tool |

---

## A9. Observability dari Hari Pertama

Setiap run harus mencatat:

```text
run_id
task_id
agent_id
stage
start_time
end_time
duration
decision
reason
artifact_path
error_type
retry_count
```

Folder observability:

```text
data/agent_workspace/logs/
data/agent_workspace/errors/
data/agent_workspace/performance/
data/agent_workspace/state/
data/agent_workspace/traces/
```

---

# Bagian B
# Development Plan Siwa Miwa

Bagian ini menjelaskan rancangan Siwa sebagai agent orchestration lokal.

---

## B1. Identity Configuration

File:

```text
config/agents.yaml
```

Konfigurasi:

```yaml
siwa:
  name: "Siwa Miwa"
  type: "llm_agent"
  role: "multi_agent_orchestrator"
  model: "siwa:latest"
  base_model: "qwen3:4b-instruct"
  temperature: 0.15
  max_context_tokens: 8192

  can_assign_tasks: true
  can_write_patch: false
  can_review_patch: false
  can_apply_patch: false
  can_commit: false
  can_push: false

  responsibilities:
    - read_task_manifest
    - validate_task_intent
    - split_task_into_subtasks
    - select_agent_by_capability
    - update_kanban
    - send_agent_message
    - collect_agent_artifacts
    - route_to_senior_reviewer
    - escalate_to_human_when_required

  denied_responsibilities:
    - write_source_code_patch
    - apply_patch
    - run_shell_command
    - git_commit
    - git_push
    - merge_branch
    - release
    - read_env
    - read_secret
    - override_safety_gate
    - override_senior_reviewer
```

---

## B2. Modelfile Siwa

File:

```text
modelfiles/Modelfile.siwa
```

Isi:

```dockerfile
FROM qwen3:4b-instruct

PARAMETER temperature 0.15
PARAMETER top_p 0.8
PARAMETER num_ctx 8192

SYSTEM """
You are Siwa Miwa, the local multi-agent orchestrator for ai-rag-local.

Your job:
- read and validate task manifests;
- split tasks into safe subtasks;
- select specialist agents by capability;
- update Kanban state;
- send structured messages;
- collect artifacts;
- validate artifact completeness;
- route final work to Senior Reviewer;
- escalate high-risk decisions to the Human Owner.

You must not:
- edit source code directly;
- write patches;
- apply patches;
- run shell commands;
- commit;
- push;
- merge;
- release;
- read secrets;
- modify .env;
- bypass Safety Gate;
- bypass Senior Reviewer.

You must output strict JSON or Markdown as requested.
You must follow the task manifest.
You must stop when scope, safety, schema, or permission is unclear.
"""
```

Command:

```bash
ollama create siwa -f modelfiles/Modelfile.siwa
```

---

## B3. Tools untuk Siwa

Siwa hanya memakai tools orchestration.

```yaml
siwa_tools:
  allow:
    - kanban_create_task
    - kanban_split_task
    - kanban_assign_task
    - kanban_update_status
    - kanban_attach_artifact
    - kanban_block_task
    - kanban_close_task
    - message_send
    - message_read_reply
    - agent_registry_lookup
    - tool_registry_lookup
    - workflow_state_read
    - workflow_state_write
    - artifact_index_read
    - artifact_summary_write
    - human_escalation_request
    - retrieve_orchestration_pattern

  deny:
    - read_env
    - read_secret
    - arbitrary_shell
    - apply_patch
    - write_patch
    - git_commit
    - git_push
    - git_merge
    - git_rebase
    - git_reset
    - delete_file
    - modify_source_file
    - modify_agent_permissions_without_human
```

---

## B4. Siwa Workflow Graph

Siwa harus berjalan sebagai graph sederhana.

```text
START
  ↓
Intake Node
  ↓
Manifest Check Node
  ↓
Risk Classification Node
  ↓
Task Split Node
  ↓
Agent Routing Node
  ↓
Dispatch Node
  ↓
Wait / Collect Artifact Node
  ↓
Evaluate Artifact Node
  ↓
Decision Node
  ├── needs_revision → Dispatch Node
  ├── needs_security_review → Asep
  ├── needs_devops_review → Doni
  ├── needs_docs → Adit
  ├── ready_for_senior → Senior Reviewer
  ├── human_required → Human Gate
  └── END
```

Loop policy:

```yaml
loop_policy:
  max_dispatch_rounds: 3
  max_revision_rounds: 2
  max_agent_wait_seconds: 300
  stop_on_safety_block: true
  stop_on_manifest_conflict: true
```

---

## B5. Node Contract

### B5.1 Intake Node

Input:

```text
user request
manifest path
optional context
```

Output:

```json
{
  "task_id": "task-043",
  "intake_status": "accepted",
  "manifest_path": "data/agent_workspace/manifests/task-043.yaml"
}
```

Stop if:

```text
manifest missing
task objective unclear
request asks prohibited action
```

### B5.2 Manifest Check Node

Checks:

```text
required fields exist
allowed paths exist
denied paths exist
risk level valid
mode valid
branch policy exists
```

Output:

```json
{
  "manifest_valid": true,
  "risk_level": "medium",
  "mode": "patch"
}
```

### B5.3 Risk Classification Node

Risk levels:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Auto-escalate if:

```text
dependency change
agent permission change
safety policy change
tool registry change
commit policy change
production data access
secret access
```

### B5.4 Task Split Node

Output:

```json
{
  "task_id": "task-043",
  "subtasks": [
    {
      "subtask_id": "task-043A",
      "type": "implementation",
      "target_agent": "opung",
      "required_outputs": ["plan", "draft_patch", "notes"]
    },
    {
      "subtask_id": "task-043B",
      "type": "security_review",
      "target_agent": "asep",
      "required_outputs": ["security_review"]
    }
  ]
}
```

### B5.5 Agent Routing Node

Routing must use `routing_rules.yaml`.

Output:

```json
{
  "routing_decision": "dispatch",
  "target_agent": "opung",
  "required_reviews": ["asep", "senior_reviewer"],
  "human_gate_required": false
}
```

### B5.6 Dispatch Node

Writes message:

```text
data/agent_workspace/agents/{agent_id}/inbox/{message_id}.json
```

### B5.7 Collect Artifact Node

Checks:

```text
artifact exists
artifact not empty
required fields present
artifact registered in Kanban
```

### B5.8 Evaluate Artifact Node

Siwa evaluates completeness only. Siwa does not do final code review.

Checks:

```text
required outputs complete
security review exists if required
devops review exists if required
docs update exists if required
Senior review ready
```

### B5.9 Decision Node

Valid decisions:

```text
dispatch_next
request_revision
request_security_review
request_devops_review
request_docs
route_to_senior
human_required
stop_blocked
done
```

---

## B6. Routing Rules

File:

```text
config/routing_rules.yaml
```

Isi:

```yaml
routing_rules:
  implementation:
    primary: opung
    required_review:
      - senior_reviewer

  implementation_with_security_risk:
    primary: opung
    required_review:
      - asep
      - senior_reviewer

  documentation:
    primary: adit
    required_review:
      - senior_reviewer

  dependency_change:
    primary: doni
    required_review:
      - asep
      - senior_reviewer
    requires_human_review: true

  ci_or_docker:
    primary: doni
    required_review:
      - senior_reviewer

  runtime_issue:
    primary: supri
    required_review:
      - doni

  agent_permission_change:
    primary: asep
    required_review:
      - senior_reviewer
    requires_human_review: true

  orchestration_policy_change:
    primary: siwa
    required_review:
      - asep
      - senior_reviewer
    requires_human_review: true

  tool_registry_change:
    primary: asep
    required_review:
      - doni
      - senior_reviewer
    requires_human_review: true

  high_risk:
    primary: siwa
    required_review:
      - asep
      - doni
      - senior_reviewer
    requires_human_review: true

  critical:
    primary: human_owner
    required_review: []
    requires_human_review: true
    automation_allowed: false
```

---

## B7. Kanban Integration

Kanban path:

```text
data/agent_workspace/kanban/board.json
```

Task structure:

```json
{
  "task_id": "task-043",
  "title": "Add BaseChannel allowlist API",
  "status": "in_progress",
  "priority": "high",
  "risk_level": "medium",
  "owner_agent": "siwa",
  "assigned_by": "human_owner",
  "task_type": "implementation_with_security_risk",
  "subtasks": [
    {
      "task_id": "task-043A",
      "title": "Implement allowlist check",
      "owner_agent": "opung",
      "status": "todo"
    },
    {
      "task_id": "task-043B",
      "title": "Review security risk",
      "owner_agent": "asep",
      "status": "todo"
    }
  ],
  "artifacts": {
    "siwa_plan": "data/agent_workspace/orchestration/task-043.siwa_plan.md",
    "opung_patch": null,
    "asep_review": null,
    "senior_review": null,
    "final_patch": null,
    "verification": null
  },
  "blocked_by": []
}
```

Status list:

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

---

## B8. Message Bus Integration

Inbox and outbox:

```text
data/agent_workspace/agents/siwa/inbox/
data/agent_workspace/agents/siwa/outbox/
data/agent_workspace/agents/{target_agent}/inbox/
data/agent_workspace/agents/{target_agent}/outbox/
```

Dispatch message template:

```json
{
  "message_id": "msg-0001",
  "from_agent": "siwa",
  "to_agent": "opung",
  "task_id": "task-043A",
  "message_type": "task_assignment",
  "priority": "medium",
  "objective": "Implement a small scoped patch.",
  "allowed_paths": [],
  "denied_paths": [],
  "required_outputs": [
    "plan",
    "draft_patch",
    "notes"
  ],
  "stop_conditions": [
    "scope_unclear",
    "denied_path_needed",
    "dependency_change_needed"
  ]
}
```

Reply template:

```json
{
  "message_id": "msg-0002",
  "from_agent": "opung",
  "to_agent": "siwa",
  "task_id": "task-043A",
  "message_type": "artifact_ready",
  "status": "completed",
  "artifacts": {
    "plan": "data/agent_workspace/plans/task-043A.opung_plan.md",
    "patch": "data/agent_workspace/patches/task-043A.opung_draft.patch",
    "notes": "data/agent_workspace/notes/task-043A.opung_notes.md"
  }
}
```

---

## B9. Output Contract Siwa

### B9.1 Orchestration Plan

Path:

```text
data/agent_workspace/orchestration/{task_id}.siwa_plan.md
```

Template:

```md
# Siwa Orchestration Plan

## Task ID

## User Objective

## Manifest Summary

## Risk Classification

## Subtasks

| Subtask | Assigned Agent | Reason | Required Output |
|---|---|---|---|

## Required Reviews

## Stop Conditions

## Human Gate Required
yes/no

## Next Action
```

### B9.2 Artifact Summary

Path:

```text
data/agent_workspace/orchestration/{task_id}.artifact_summary.md
```

Template:

```md
# Artifact Summary

## Task ID

## Agent Outputs

| Agent | Artifact | Decision | Notes |
|---|---|---|---|

## Missing Artifacts

## Conflicts

## Ready for Senior Review
yes/no
```

### B9.3 Human Review Request

Path:

```text
data/agent_workspace/requests/{task_id}.human_review_required.md
```

Template:

```md
# Human Review Required

## Task ID

## Reason

## Trigger

## Risk Level

## Affected Files

## Current Stage

## Options

1. Approve limited continuation.
2. Modify manifest.
3. Reject task.
4. Convert to manual work.

## Recommended Action
```

---

## B10. Guardrail Rules

File:

```text
config/siwa_guardrails.yaml
```

Isi:

```yaml
siwa_guardrails:
  block:
    - request_to_push
    - request_to_merge
    - request_to_delete_mass_files
    - request_to_modify_env
    - request_to_access_secret
    - request_to_bypass_safety_gate
    - request_to_skip_senior_review
    - request_to_auto_release
    - request_to_grant_arbitrary_shell_to_agent

  escalate_to_human:
    - dependency_change
    - agent_permission_change
    - security_policy_change
    - architecture_change
    - production_data_change
    - tool_registry_change
    - commit_policy_change
```

---

## B11. Knowledge Base untuk Siwa

Collection:

```text
siwa_orchestration_knowledge
```

Allowed use:

```text
design pattern only
workflow pattern only
routing pattern only
governance pattern only
```

Disallowed use:

```text
runtime dependency import without review
automatic framework migration
cloud service dependency
unreviewed external code copy
```

Metadata:

```json
{
  "agent": "siwa",
  "source_type": "orchestration_reference",
  "source_repo": "microsoft/conductor",
  "allowed_use": "design_pattern_only",
  "runtime_dependency": false,
  "risk": "low",
  "topic": "workflow_yaml_human_gate"
}
```

---

# Bagian C
# Implementation Roadmap

---

## C1. Phase 0: Contract Freeze

Tujuan:

```text
Bekukan schema sebelum LLM aktif.
```

Deliverables:

```text
config/agents.yaml
config/routing_rules.yaml
config/siwa_guardrails.yaml
schemas/manifest.schema.json
schemas/message.schema.json
schemas/kanban.schema.json
schemas/siwa_output.schema.json
```

Exit criteria:

```text
Semua schema bisa divalidasi.
Tidak ada agent yang bisa push.
Tidak ada agent yang bisa commit kecuali Commit Gate.
Siwa tidak punya write_patch.
```

---

## C2. Phase 1: Deterministic Siwa Skeleton

Tujuan:

```text
Siwa berjalan tanpa LLM.
```

Deliverables:

```text
selfdev/agents/siwa_orchestrator.py
selfdev/tools/kanban.py
selfdev/tools/message_bus.py
selfdev/agents/agent_registry.py
selfdev/runtime/workflow_state.py
```

Capabilities:

```text
load manifest
validate manifest
match routing rule
create Kanban task
send static message
write state
```

Exit criteria:

```text
Satu task docs bisa dibuat dan dikirim ke Adit tanpa LLM.
```

---

## C3. Phase 2: Qwen3 4B Instruct Planning

Tujuan:

```text
Aktifkan LLM hanya untuk planning text dan risk explanation.
```

Allowed LLM use:

```text
task summary
risk classification draft
subtask suggestion
assignment explanation
```

Not allowed:

```text
final routing without rule validation
write patch
execute tool outside allow-list
commit
```

Exit criteria:

```text
Siwa output valid JSON atau Markdown sesuai schema.
Jika invalid, fallback deterministic berjalan.
```

---

## C4. Phase 3: Artifact Evaluation

Tujuan:

```text
Siwa bisa mengecek kelengkapan artifact.
```

Checks:

```text
artifact exists
artifact not empty
required sections exist
decision valid
artifact registered in Kanban
```

Exit criteria:

```text
Siwa dapat memutuskan ready_for_senior atau needs_revision.
```

---

## C5. Phase 4: Human Gate Manager

Tujuan:

```text
Siwa membuat human_review_required artifact untuk high-risk task.
```

Triggers:

```text
dependency change
agent permission change
tool registry change
security policy change
architecture change
commit policy change
secret access
```

Exit criteria:

```text
High-risk task tidak lanjut otomatis.
```

---

## C6. Phase 5: Failure Test Suite

Minimum tests:

```text
test_manifest_missing_required_field
test_siwa_invalid_json_output
test_routing_unknown_task_type
test_agent_timeout
test_denied_path_detected
test_patch_outside_scope
test_dependency_change_requires_human
test_revision_loop_limit
test_checkpoint_resume
test_replay_from_checkpoint
test_artifact_missing
test_commit_gate_block_when_verification_failed
```

Exit criteria:

```text
Failure menghasilkan report.
Tidak ada silent failure.
Tidak ada gate yang bisa dilewati.
```

---

## C7. Phase 6: Limited Multi-Agent Run

Alur pertama yang disarankan:

```text
docs task
  ↓
Siwa
  ↓
Adit
  ↓
Senior Reviewer
  ↓
Verification Engine
```

Alur kedua:

```text
small code task
  ↓
Siwa
  ↓
Opung
  ↓
Asep if security relevant
  ↓
Senior Reviewer
  ↓
Runner
  ↓
Verification Engine
```

Exit criteria:

```text
Sistem stabil untuk task kecil.
Tidak ada automatic commit.
Tidak ada push.
```

---

# Bagian D
# Referensi Terpisah dari Pondasi Anti-Gagal

Bagian ini berisi referensi GitHub dan cara memakainya. Referensi tidak menjadi dependency inti. Referensi hanya menjadi pola desain sampai lolos compatibility score.

---

## D1. Compatibility Score

Setiap referensi harus dinilai sebelum diadopsi.

| Kriteria | Bobot |
|---|---:|
| Cocok dengan local-first | 20 |
| Bisa file-based | 15 |
| Bisa manifest-driven | 15 |
| Tidak memaksa cloud | 10 |
| Bisa human gate | 10 |
| Bisa checkpoint/resume | 10 |
| Tool permission jelas | 10 |
| Implementasi ringan | 10 |

Keputusan:

```text
>= 80  boleh jadi core pattern
60-79  boleh jadi optional pattern
40-59  hanya jadi ide
< 40   abaikan
```

---

## D2. Reference Mapping

| Referensi | Fungsi untuk Siwa | Status adopsi |
|---|---|---|
| `microsoft/conductor` | YAML workflow, conditional routing, human gate, safety limits | Core pattern |
| `foreveryh/mentis` | Planner, Supervisor, Handoff, Evaluator | Core pattern |
| `moiz-q/langgraph-agent` | Planner, evaluator, conditional edges, loop prevention | Core pattern |
| `gastownhall/gascity` | Work tracking, runtime provider, health patrol, supervisor loop | Optional pattern |
| `yx-fan/multi-agent-orchestration-framework` | YAML config, AgentRouter, StateManager | Optional pattern |
| `microsoft/agent-framework` | Checkpointing, HITL, observability, declarative agents | Long-term roadmap |
| `inkeep/agents` | Agent UI, subagents, credentials, traces | UI roadmap |
| `SocioProphet/agent-registry` | Agent identity, tool grants, revocation | Governance pattern |
| `offlabel-scaffolds/agent-tool-scaffold` | Tool registry, prompt manager, memory, tests | Scaffold pattern |
| `wundergraph/graphql-go-tools` | Router and gateway analogy | Concept only |
| AutoGen group chat examples | Persona and moderator idea | Not core engine |

---

## D3. References and Intended Use

### D3.1 Microsoft Conductor

URL:

```text
https://github.com/microsoft/conductor
```

Use for:

```text
workflow YAML
conditional routing
parallel execution with limits
human-in-the-loop gate
loop-back pattern
safety limits
validation before runtime
```

Local adaptation:

```text
Conductor workflow YAML → selfdev workflow YAML
Human gate → human_review_required.md
Safety limits → loop_policy and performance_budget
Parallel execution → optional after sequential runtime is stable
```

### D3.2 Foreveryh Mentis

URL:

```text
https://github.com/foreveryh/mentis
```

Use for:

```text
Planner
Supervisor
Handoff
Specialist Agent
Evaluator
Supervisor loop
A2A pattern
```

Local adaptation:

```text
Planner → Siwa Task Split Node
Supervisor → Siwa Routing Node
Handoff → Message Bus
Evaluator → Artifact Gate
Reporter → Artifact Summary
```

### D3.3 Moiz-Q LangGraph Agent

URL:

```text
https://github.com/moiz-q/langgraph-agent
```

Use for:

```text
simple state machine
conditional route
planner node
evaluator node
loop prevention
confidence based decision
```

Local adaptation:

```text
Planner → Siwa Plan
Retriever → Orchestration Knowledge Retrieval
Evaluator → Artifact completeness check
Answer → Routing decision
```

### D3.4 Gas City

URL:

```text
https://github.com/gastownhall/gascity
```

Use for:

```text
work tracking
runtime providers
orders
mail
health patrol
declarative configuration
supervisor reconciliation loop
```

Local adaptation:

```text
work tracking → Kanban board
mail → Message Bus
health patrol → local health report
runtime provider → selfdev Runner
```

### D3.5 YX Fan Multi-Agent Orchestration Framework

URL:

```text
https://github.com/yx-fan/multi-agent-orchestration-framework
```

Use for:

```text
YAML workflow config
AgentRouter
StateManager
provider abstraction
FastAPI interface idea
```

Local adaptation:

```text
workflow config → routing_rules.yaml
StateManager → workflow_state.py
AgentRouter → routing_gate.py
```

### D3.6 Microsoft Agent Framework

URL:

```text
https://github.com/microsoft/agent-framework
```

Use for:

```text
multi-agent workflow patterns
checkpointing
human-in-the-loop
observability
declarative agents
agent skills
```

Local adaptation:

```text
checkpointing → state file and replay
observability → logs, traces, performance
agent skills → skills in agents.yaml
```

### D3.7 Inkeep Agents

URL:

```text
https://github.com/inkeep/agents
```

Use for:

```text
agent management UI
subagent definition
MCP-style tool integration
credential boundary
traces
evaluation UI
```

Local adaptation:

```text
Agent UI → future dashboard
Subagent model → agent registry
Traces → local trace artifacts
```

### D3.8 SocioProphet Agent Registry

URL:

```text
https://github.com/SocioProphet/agent-registry
```

Use for:

```text
agent identity
sessions
memories
tool grants
revocation
runtime authority
```

Local adaptation:

```text
tool grants → tools.allow and tools.deny
revocation → disable agent or tool permission
runtime authority → gate before dispatch
```

### D3.9 Offlabel Agent Tool Scaffold

URL:

```text
https://github.com/offlabel-scaffolds/agent-tool-scaffold
```

Use for:

```text
tool registry
prompt manager
memory
unit tests
input validation
logging
metrics
error tracking
```

Local adaptation:

```text
Tool registry → config/tools.yaml
Prompt manager → modelfiles and prompt templates
Metrics → performance logs
```

### D3.10 WunderGraph GraphQL Go Tools

URL:

```text
https://github.com/wundergraph/graphql-go-tools
```

Use as concept only:

```text
router gateway
trusted operations
timeout
retry
middleware
schema validation
traffic shaping
```

Local adaptation:

```text
router gateway → Siwa Routing Gate
trusted operations → allowed tools
middleware → Safety Gate
schema validation → Schema Gate
```

### D3.11 AutoGen Group Chat Examples

URLs:

```text
https://github.com/chanirban/autogen-multiagent-conversation
https://github.com/SandeshGitHub2077/autogen_multiagent_groupChat
```

Use for:

```text
persona separation
moderator concept
planner engineer critic pattern
```

Do not use for:

```text
free-form group chat as execution engine
unbounded debate loop
automatic executor agent
```

---

# Bagian E
# Test and Acceptance Criteria

---

## E1. Minimum Acceptance Criteria

Siwa dianggap siap tahap awal jika:

```text
Can load valid manifest
Can reject invalid manifest
Can classify risk
Can match routing rule
Can create Kanban task
Can send message to target agent
Can write orchestration plan
Can collect artifact
Can detect missing artifact
Can escalate high-risk task
Can fallback to deterministic routing
Can stop safely on invalid output
```

---

## E2. Failure Acceptance Criteria

Sistem dianggap anti-gagal jika:

```text
No silent failure
No unlimited loop
No direct source modification by Siwa
No patch writing by Siwa
No shell access by Siwa
No commit by Siwa
No push by Siwa
No safety bypass
No Senior review bypass
No lost state after interruption
No high-risk action without human gate
```

---

## E3. First Dry-Run Scenario

Input:

```yaml
task_id: task-docs-001
task_type: documentation
risk_level: low
mode: plan
allowed_paths:
  - docs/
  - README.md
denied_paths:
  - .env
  - .git/
required_outputs:
  - docs_plan
required_reviews:
  - senior_reviewer
```

Expected:

```text
Siwa validates manifest.
Siwa routes to Adit.
Siwa writes Kanban task.
Siwa sends message to Adit.
Siwa does not write patch.
Siwa does not run shell.
Siwa writes state file.
```

---

## E4. First Failure Scenario

Input:

```yaml
task_id: task-risk-001
task_type: dependency_change
risk_level: medium
mode: patch
allowed_paths:
  - requirements.txt
denied_paths:
  - .env
required_outputs:
  - dependency_review
```

Expected:

```text
Siwa detects dependency_change.
Siwa routes to Doni.
Siwa requires Asep and Senior Reviewer.
Siwa creates human_review_required.
No automatic patch apply.
No automatic commit.
```

---

# Final Summary

Siwa Miwa harus dibangun sebagai orchestrator yang aman saat gagal. Referensi GitHub yang terkumpul berguna sebagai pola desain, tetapi tidak boleh langsung menjadi dependency inti.

Prinsip final:

```text
Build deterministic skeleton first.
Add Qwen3 4B instruct only after schema is stable.
Use LLM for planning and explanation.
Use rules for routing authority.
Use Kanban for shared state.
Use Message Bus for agent communication.
Use checkpoints for recovery.
Use human gate for high-risk actions.
Use Safety Gate and Senior Reviewer as hard boundaries.
```

Dengan desain ini, Siwa Miwa dapat berkembang menjadi orchestrator multi-agent yang kuat, tetapi tetap aman ketika failure terjadi.
