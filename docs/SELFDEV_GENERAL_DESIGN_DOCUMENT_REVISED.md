# SelfDev General Design Document

**Document status:** Revised general design document  
**Document type:** System architecture and governance design  
**Version:** v0.2  
**Date:** 2026-05-07  
**Primary system name:** SelfDev  
**Former project anchor:** `ai-rag-local`  
**New position:** Standalone local multi-agent self-development and maintenance system  

---

## 1. Executive Summary

SelfDev is a standalone local multi-agent system for controlled software development, review, maintenance, documentation, runtime analysis, and local commit preparation.

At the beginning, SelfDev was planned as a development layer for `ai-rag-local`. That position is now revised. `ai-rag-local` is no longer the foundation of SelfDev. It is the first managed system and one important product that SelfDev can help develop and maintain.

The revised model is:

```text
SelfDev = standalone self-development and maintenance system
ai-rag-local = first managed system and assistant product
Other systems = future managed systems
```

SelfDev must be able to work on:

```text
AI RAG Local
RAG pipelines
knowledge base systems
agent systems
documentation systems
backend services
local automation tools
DevOps and CI configuration
runtime and sysadmin workflows
security review workflows
future internal systems
```

SelfDev is not an autonomous production engineer. It is a controlled, failure-first, local multi-agent workflow with explicit gates, audit trail, artifact contracts, and human control for high-risk actions.

---

## 2. Revised Positioning

### 2.1 Old Position

The old assumption was:

```text
SelfDev exists to develop ai-rag-local.
```

This is too narrow.

### 2.2 New Position

The new assumption is:

```text
SelfDev exists as its own system.
ai-rag-local is only one managed target.
```

SelfDev has broader responsibility than maintaining a RAG project. It can support any repository or system that can be represented through:

```text
target system registry
manifest
allowed paths
denied paths
task type
risk classification
agent routing
artifact contract
review gates
verification gates
human gates
```

### 2.3 Relationship Between SelfDev and AI RAG Local

AI RAG Local is expected to become an assistant that is close to general-purpose in local usage. It may support RAG, knowledge retrieval, reasoning assistance, workspace search, and other assistant functions.

SelfDev is different.

SelfDev is the system that can develop, maintain, review, document, and audit AI RAG Local and other systems.

Clear separation:

| System | Function | Position |
|---|---|---|
| SelfDev | Multi-agent development and maintenance system | Parent development system |
| AI RAG Local | Local assistant and RAG system | Managed target system |
| Other systems | Future repositories, tools, agents, services, docs, runtime systems | Managed target systems |

---

## 3. Core Design Principle

SelfDev uses a failure-first architecture.

The starting assumption is:

```text
LLM output can be wrong.
Agent routing can be wrong.
Patch can be wrong.
Review can be incomplete.
Scanner can be noisy.
Tests can miss bugs.
Docs can hallucinate behavior.
Runtime diagnosis can overclaim root cause.
DevOps validation can be unsafe if executed directly.
```

Therefore, SelfDev must never depend on trust alone.

SelfDev must enforce:

```text
manifest first
schema first
least privilege tools
explicit allowed paths
explicit denied paths
small context
small patch
artifact-based workflow
specialist review
senior review
safety gate
runner-controlled execution
verification before commit
local commit only
human owner for push, merge, release, and high-risk actions
```

---

## 4. Non-Negotiable Safety Rules

SelfDev must never allow an agent to:

```text
read .env
read secrets
modify .env
modify secrets
run arbitrary shell
apply patch directly
run tests directly
install dependency directly
commit directly
push directly
merge directly
release directly
deploy directly
restart service directly
run destructive command directly
bypass Safety Gate
bypass Senior Reviewer
bypass Verification Engine
bypass Human Owner
```

Only deterministic runtime tools may execute approved actions.

Execution belongs to Runner.  
Validation belongs to Verification Engine.  
Policy enforcement belongs to Safety Gate.  
Local commit belongs to Commit Gate.  
Push, merge, release, production deployment, and high-risk runtime action belong to Human Owner.

---

## 5. System Goals

SelfDev should support these goals:

```text
1. Convert human requests into valid task manifests.
2. Route tasks to the correct specialist agent.
3. Keep every agent inside role, scope, and tool boundaries.
4. Produce small, reviewable artifacts.
5. Create documentation, patch, review, runtime, DevOps, and security artifacts.
6. Validate artifacts through deterministic gates.
7. Prepare local commits only after all required checks pass.
8. Maintain auditability through state, logs, traces, and reports.
9. Support multiple managed systems beyond ai-rag-local.
10. Degrade safely when LLM output or tooling fails.
```

---

## 6. System Non-Goals

SelfDev should not:

```text
act as a free autonomous coding agent
edit production systems directly
own secrets
own cloud credentials
perform live pentest without approved scope
run active external scans by default
deploy infrastructure directly
push or merge code automatically
replace human ownership for high-risk decisions
turn knowledge base references into automatic dependencies
copy external code into target repositories without review
```

---

## 7. Managed System Model

SelfDev should manage multiple target systems through a registry.

### 7.1 Target System Registry

Recommended file:

```text
config/selfdev/target_systems.yaml
```

Example:

```yaml
target_systems:
  ai_rag_local:
    name: AI RAG Local
    type: rag_assistant
    repo_path: ../ai-rag-local
    default_branch: main
    selfdev_branch_prefix: selfdev/
    risk_profile: medium
    allowed_default_paths:
      - app/
      - tests/
      - docs/
      - scripts/
      - config/
    denied_default_paths:
      - .env
      - .env.*
      - .git/
      - data/secrets/
      - credentials/
      - private_keys/
    required_gates:
      - safety_gate
      - senior_reviewer
      - verification_engine

  future_backend_service:
    name: Future Backend Service
    type: backend_service
    repo_path: ../future-backend-service
    risk_profile: high
    required_gates:
      - safety_gate
      - senior_reviewer
      - verification_engine
      - human_gate_for_deploy
```

### 7.2 Target System Adapter

Each target system may need an adapter.

Recommended folder:

```text
selfdev/targets/
├── base_target.py
├── ai_rag_local.py
├── python_project.py
├── docs_project.py
├── service_project.py
└── generic_repo.py
```

Adapter responsibilities:

```text
resolve repo path
load target policy
map task type to file types
map verification checks
map docs structure
map runtime profile
map risk profile
```

Adapter restrictions:

```text
must not override Safety Gate
must not override denied paths
must not inject secrets
must not run commands directly
```

---

## 8. High-Level Architecture

```text
Human Owner
  ↓
Task Intake
  ↓
Task Manifest
  ↓
Target System Registry
  ↓
Siwa Miwa Orchestrator
  ↓
Routing Rules
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
Senior Reviewer Commit Request
  ↓
Commit Gate
  ↓
Local Commit Record
  ↓
Human Owner decides push, merge, release, or deployment
```

---

## 9. Component Classes

SelfDev has four component classes.

| Class | Components | Function |
|---|---|---|
| Agents | Siwa, Opung, Adit, Asep, Doni, Supri, Senior Reviewer | Reasoning, review, planning, artifact writing |
| Runtime tools | Runner, Verification Engine, Safety Gate, Commit Gate | Execute, validate, block, local commit |
| State tools | Kanban, Message Bus, State Manager, Artifact Registry, Trace Writer | Workflow memory and audit |
| Governance tools | Agent Registry, Tool Registry, Policy Engine, Human Gate, Target System Registry | Authority and boundary control |

---

## 10. Repository Structure

SelfDev should not live as an internal subfolder of AI RAG Local in the long term. It should be structured as its own system.

Recommended standalone structure:

```text
selfdev/
├── README.md
├── CHANGELOG.md
├── pyproject.toml
├── .env.sample
│
├── docs/
│   ├── GENERAL_DESIGN_DOCUMENT.md
│   ├── CORE_TOOLS_AND_AGENT_TOOLING.md
│   ├── architecture/
│   ├── agents/
│   │   ├── SIWA_MIWA_FAILURE_FIRST_DEVELOPMENT_PLAN.md
│   │   ├── OPUNG_FAILURE_FIRST_DEVELOPMENT_PLAN.md
│   │   ├── ADIT_FAILURE_FIRST_DEVELOPMENT_PLAN.md
│   │   ├── ASEP_FAILURE_FIRST_DEVELOPMENT_PLAN.md
│   │   ├── DONI_FAILURE_FIRST_DEVELOPMENT_PLAN.md
│   │   ├── SUPRI_FAILURE_FIRST_DEVELOPMENT_PLAN.md
│   │   └── SENIOR_REVIEWER_FAILURE_FIRST_DEVELOPMENT_PLAN.md
│   └── knowledge_base/
│       ├── SIWA_MIWA_KNOWLEDGE_BASE_LINKS.md
│       ├── OPUNG_KNOWLEDGE_BASE_LINKS.md
│       ├── ADIT_KNOWLEDGE_BASE_LINKS.md
│       ├── ASEP_KNOWLEDGE_BASE_LINKS.md
│       ├── DONI_KNOWLEDGE_BASE_LINKS.md
│       ├── SUPRI_KNOWLEDGE_BASE_LINKS.md
│       └── SENIOR_REVIEWER_KNOWLEDGE_BASE_LINKS.md
│
├── config/
│   └── selfdev/
│       ├── target_systems.yaml
│       ├── agents.yaml
│       ├── models.yaml
│       ├── tools.yaml
│       ├── agent_tool_grants.yaml
│       ├── routing_rules.yaml
│       ├── workflow.yaml
│       ├── safety_policy.yaml
│       ├── branch_policy.yaml
│       ├── artifact_policy.yaml
│       ├── risk_policy.yaml
│       ├── docs_policy.yaml
│       ├── security_knowledge_routing.yaml
│       ├── devops_knowledge_routing.yaml
│       ├── runtime_knowledge_routing.yaml
│       ├── coding_knowledge_routing.yaml
│       └── senior_reviewer_knowledge_routing.yaml
│
├── modelfiles/
│   ├── Modelfile.siwa
│   ├── Modelfile.opung
│   ├── Modelfile.adit
│   ├── Modelfile.asep
│   ├── Modelfile.doni
│   ├── Modelfile.supri
│   └── Modelfile.senior_reviewer
│
├── schemas/
│   └── selfdev/
│       ├── manifest.schema.json
│       ├── target_system.schema.json
│       ├── agent.schema.json
│       ├── tool_grant.schema.json
│       ├── routing_rules.schema.json
│       ├── message.schema.json
│       ├── kanban.schema.json
│       ├── artifact.schema.json
│       ├── review.schema.json
│       ├── validation_request.schema.json
│       ├── verification_report.schema.json
│       ├── safety_report.schema.json
│       ├── apply_approval.schema.json
│       ├── commit_request.schema.json
│       └── commit_record.schema.json
│
├── selfdev/
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── siwa_orchestrator.py
│   │   ├── opung_coder.py
│   │   ├── adit_docs.py
│   │   ├── asep_security.py
│   │   ├── doni_devops.py
│   │   ├── supri_runtime.py
│   │   └── senior_reviewer.py
│   │
│   ├── tools/
│   │   ├── runner.py
│   │   ├── verification_engine.py
│   │   ├── safety_gate.py
│   │   ├── commit_gate.py
│   │   ├── kanban.py
│   │   ├── message_bus.py
│   │   ├── artifact_registry.py
│   │   ├── knowledge_router.py
│   │   ├── agent_registry.py
│   │   ├── tool_registry.py
│   │   └── policy_engine.py
│   │
│   ├── runtime/
│   │   ├── workflow_engine.py
│   │   ├── state_manager.py
│   │   ├── lock_manager.py
│   │   ├── trace_writer.py
│   │   ├── performance_logger.py
│   │   └── target_context_loader.py
│   │
│   ├── targets/
│   │   ├── base_target.py
│   │   ├── ai_rag_local.py
│   │   ├── python_project.py
│   │   ├── docs_project.py
│   │   └── generic_repo.py
│   │
│   └── policies/
│       ├── scope_policy.py
│       ├── tool_policy.py
│       ├── branch_policy.py
│       ├── risk_policy.py
│       ├── artifact_policy.py
│       ├── human_gate_policy.py
│       └── target_policy.py
│
├── workspace/
│   └── agent_workspace/
│       ├── kanban/
│       ├── agents/
│       ├── manifests/
│       ├── orchestration/
│       ├── plans/
│       ├── patches/
│       ├── final_patches/
│       ├── docs/
│       ├── reviews/
│       ├── runtime/
│       ├── requests/
│       ├── approvals/
│       ├── runner/
│       ├── verification/
│       ├── safety/
│       ├── commits/
│       ├── state/
│       ├── logs/
│       ├── traces/
│       ├── performance/
│       └── errors/
│
├── scripts/
│   ├── validate_manifest.py
│   ├── validate_registry.py
│   ├── run_siwa.py
│   ├── dry_run_task.py
│   ├── create_models.py
│   └── bootstrap_workspace.py
│
└── tests/
    └── selfdev/
        ├── test_manifest_gate.py
        ├── test_target_registry.py
        ├── test_routing_gate.py
        ├── test_tool_grants.py
        ├── test_message_bus.py
        ├── test_artifact_gate.py
        ├── test_safety_gate.py
        ├── test_runner_policy.py
        ├── test_verification_engine.py
        ├── test_commit_gate.py
        └── test_checkpoint_resume.py
```

If SelfDev is kept inside `ai-rag-local` during the early phase, the structure must still preserve the same boundaries. Do not make AI RAG Local the architectural parent.

---

## 11. Environment Configuration Policy

`.env` is not the authority layer.

`.env` should only store runtime locations and toggles.

Allowed examples:

```env
SELFDEV_ENABLED=true
SELFDEV_WORKSPACE_DIR=workspace/agent_workspace
SELFDEV_CONFIG_DIR=config/selfdev
SELFDEV_SCHEMA_DIR=schemas/selfdev
SELFDEV_MODELFILES_DIR=modelfiles
SELFDEV_TARGET_REGISTRY=config/selfdev/target_systems.yaml
OLLAMA_BASE_URL=http://localhost:11434
SELFDEV_MAX_CONCURRENT_AGENTS=1
SELFDEV_DEFAULT_MODE=sequential_first
```

Do not place tool grants, agent authority, routing, denied paths, or high-risk policy in `.env`.

Wrong pattern:

```env
OPUNG_CAN_COMMIT=true
DONI_CAN_DEPLOY=true
ASEP_CAN_RUN_ZAP=true
SIWA_ALLOWED_PATHS=app/,tests/
```

Authority must live in versioned YAML and schema-controlled policy files.

---

## 12. Agent Registry

Recommended file:

```text
config/selfdev/agents.yaml
```

Required fields:

```yaml
agent_id:
name:
role:
type:
model:
base_model:
temperature:
max_context_tokens:
responsibilities:
denied_responsibilities:
allowed_tools:
denied_tools:
request_only_tools:
output_artifacts:
required_gates:
```

Agent registry defines identity. Tool registry defines available tools. Tool grants define which agent can use which tool.

---

## 13. Agent Role Matrix

| Agent | Role | Primary output | Execution allowed | Commit allowed | Push allowed |
|---|---|---|---:|---:|---:|
| Siwa Miwa | Orchestrator, planner, router, dispatcher, evaluator, human-gate manager | Orchestration plan, routing decision, artifact summary, escalation request | No | No | No |
| Opung | Scoped coding implementer, small patch drafter, unit test drafter | Implementation plan, draft patch, test draft, patch notes | No | No | No |
| Adit | Documentation architect and docs maintainer | Docs plan, docs patch, gap report, style review, validation request | No | No | No |
| Asep | Defensive security reviewer and vulnerability intelligence analyst | Security review, vulnerability report, validation request, block decision | No | No | No |
| Doni | DevOps, CI/CD, IaC, deployment, observability reviewer | DevOps review, validation request, block decision | No | No | No |
| Supri | Read-only sysadmin analyst, runtime triage, incident classifier, SOP writer | Runtime summary, incident classification, troubleshooting checklist, SOP, read-only request | No | No | No |
| Senior Reviewer | Final reviewer, maintainability auditor, test-readiness reviewer, commit-request approver | Senior review, revision request, apply approval, commit request | No | No | No |

---

## 14. Siwa Miwa Design

### 14.1 Role

Siwa Miwa is the local orchestrator.

Siwa is responsible for:

```text
intake
manifest validation
risk classification
task decomposition
agent routing
Kanban update
message dispatch
artifact collection
artifact completeness checking
human escalation
routing to Senior Reviewer
workflow state writing
```

Siwa is not responsible for:

```text
writing source code patch
writing docs patch directly
applying patch
running shell
running tests
committing
pushing
merging
releasing
reading secrets
modifying .env
bypassing review gates
```

### 14.2 Siwa Gates

```text
Manifest Gate
Schema Gate
Routing Gate
Context Gate
Iteration Gate
Artifact Gate
Human Gate
```

### 14.3 Siwa Decisions

```text
dispatch_next
request_revision
request_security_review
request_devops_review
request_docs
request_runtime_review
route_to_senior
human_required
stop_blocked
done
```

---

## 15. Opung Design

### 15.1 Role

Opung is the small scoped coding implementer.

Opung can:

```text
read manifest
read allowed files
read git diff
retrieve same-repo context
retrieve coding references
write implementation plan
write small draft patch
write small test draft if manifest allows
write patch notes
request scope expansion
request specialist review
```

Opung cannot:

```text
apply patch
run shell
run tests
install dependency
modify .env
read secrets
git commit
git push
git merge
git rebase
delete files
large refactor
change architecture
change dependency
change public API without manifest
change security policy
change DevOps config
```

### 15.2 Opung Gates

```text
Manifest Gate
Scope Gate
Context Gate
Reference Gate
Patch Size Gate
Evidence Gate
Stop Gate
```

### 15.3 Opung Patch Limits

```yaml
opung_patch_limits:
  max_files_changed: 3
  max_lines_added: 180
  max_lines_removed: 80
  max_patch_bytes: 60000
```

### 15.4 Opung Decisions

```text
draft_patch_ready
needs_scope_expansion
needs_task_split
needs_senior_clarification
blocked_by_policy
```

---

## 16. Adit Design

### 16.1 Role

Adit is the documentation agent.

Adit can:

```text
read docs
read README
read CHANGELOG
read manifest
read selected source files if manifest allows
classify docs with Diataxis
write documentation plan
write documentation gap report
write docs patch
write README patch
write CHANGELOG patch
write API docs explanation
write runbook template
write style review
request docs validation
```

Adit cannot:

```text
modify source code
run shell
install dependency
run docs build directly
deploy docs
publish docs
execute runbook
commit
push
modify .env
read secrets
invent undocumented behavior
```

### 16.2 Adit Gates

```text
Manifest Gate
Evidence Gate
Scope Gate
Diataxis Fit Gate
Patch Size Gate
Validation Request Gate
Human Gate
```

### 16.3 Adit Docs Structure

Recommended docs structure:

```text
docs/
├── index.md
├── tutorials/
├── how-to/
├── reference/
├── explanation/
├── runbooks/
└── api/
```

Adit may suggest this structure. Adit must not migrate all docs without manifest and human approval.

---

## 17. Asep Design

### 17.1 Role

Asep is the defensive security reviewer and vulnerability intelligence analyst.

Asep can:

```text
read manifest
read git diff
read changed files within scope
retrieve selected security references
classify security risk
map findings to CWE if evidence supports it
map findings to CAPEC only as context
add MITRE ATT&CK context only as context
request NVD lookup
request CISA KEV lookup
request ZAP or Nuclei validation through Runner only
write security review
block unsafe patch
```

Asep cannot:

```text
run scanner directly
execute exploit
generate live-target payload
generate reverse shell
perform brute force
perform credential theft instruction
perform persistence instruction
perform lateral movement instruction
run shell
apply patch
commit
push
merge
modify .env
bypass Safety Gate
bypass Senior Reviewer
```

### 17.2 Asep Gates

```text
Input Scope Gate
Reference Retrieval Gate
Finding Evidence Gate
Tool Execution Gate
Decision Gate
```

### 17.3 Asep Decisions

```text
approve_security
request_revision
block
```

---

## 18. Doni Design

### 18.1 Role

Doni is the DevOps, CI/CD, IaC, deployment, observability, and runtime reviewer.

Doni can:

```text
read manifest
read git diff
read DevOps files within scope
review GitHub Actions
review Dockerfile
review Docker Compose
review Kubernetes manifests
review Helm charts
review Terraform files
review Ansible playbooks
review Grafana dashboards
review Prometheus rules
review runbooks and rollback procedures
request safe validation through Runner or Verification Engine
write DevOps review
block high-risk configuration
```

Doni cannot:

```text
run shell
docker build
docker compose up
kubectl apply
kubectl delete
helm install
helm upgrade
terraform apply
terraform destroy
ansible-playbook
deploy to cloud
restart service
modify .env
commit
push
delete file
```

### 18.2 Doni Gates

```text
Scope Gate
File-Type Routing Gate
Reference Retrieval Gate
Evidence Gate
Validation Request Gate
Decision Gate
```

### 18.3 Doni Decisions

```text
approve_devops
request_revision
block
human_required
```

---

## 19. Supri Design

### 19.1 Role

Supri is the read-only local sysadmin reviewer, runtime status analyst, log triage assistant, incident classifier, hardening checklist assistant, and SOP writer.

Supri can:

```text
read manifest
read Runner report
read Verification Engine report
read Safety Gate report
read error reports
read log excerpts that are provided
read service status snapshots
read resource snapshots
read incident tickets
write runtime summary
write incident classification
write troubleshooting checklist
write backup restore SOP
write user management SOP
write hardening checklist
write read-only check request
```

Supri cannot:

```text
run shell
restart service
stop service
kill process
delete file
edit config
modify .env
read secrets
create user
delete user
change password
edit sudoers
install package
run ansible-playbook
run OpenSCAP remediation
apply CIS hardening
reload nginx, apache, or ssh
terraform apply
kubectl apply
docker compose up or down
git commit
git push
```

### 19.2 Supri Gates

```text
Manifest Gate
Scope Gate
Read-Only Gate
Evidence Gate
Classification Gate
Escalation Gate
Stop Gate
```

### 19.3 Supri Decisions

```text
runtime_summary_ready
incident_classified
needs_more_evidence
needs_read_only_check
needs_asep_review
needs_doni_review
needs_human_owner
blocked_by_policy
```

Supri must not output:

```text
restart_done
config_changed
hardening_applied
backup_restored
user_created
issue_fixed
```

---

## 20. Senior Reviewer Design

### 20.1 Role

Senior Reviewer is the final review agent.

Senior Reviewer reads artifacts from Opung, Adit, Asep, Doni, Supri, Runner, Verification Engine, and Safety Gate.

Senior Reviewer can:

```text
read manifest
read git diff
read draft patch
read final patch
read specialist reviews
read Runner report
read Verification Engine report
read Safety Gate report
read static analysis result
read linter result
read coverage result
write senior review
write revision request
write specialist review request
write apply approval
write commit request
```

Senior Reviewer cannot:

```text
run shell
apply patch
run tests
run CodeQL
run Semgrep
run Sonar
run linter
install dependency
modify .env
read secrets
git commit
git push
git merge
git rebase
delete file
deploy
bypass Safety Gate
bypass Verification Engine
bypass Human Owner
```

### 20.2 Senior Reviewer Gates

```text
Manifest Gate
Artifact Completeness Gate
Scope Gate
Diff Gate
Specialist Precedence Gate
Evidence Gate
Test Readiness Gate
Static Analysis Gate
Decision Gate
Commit Request Gate
```

### 20.3 Senior Reviewer Decisions

```text
approve_for_runner
request_revision
request_specialist_review
request_validation
block
human_required
request_commit
```

### 20.4 Specialist Precedence Rule

```text
If Asep blocks security, Senior Reviewer cannot approve.
If Doni blocks DevOps, Senior Reviewer cannot approve.
If Safety Gate blocks, Senior Reviewer cannot approve.
If Verification Engine fails blocking checks, Senior Reviewer cannot request commit.
```

---

## 21. Core Tools

### 21.1 Runner

Runner is the controlled executor. Runner executes only approved actions.

Runner can:

```text
run git apply check
apply approved final patch
run safe validation command
run dry-run command
run test command
run lint command
run docs build check
run schema validation
run controlled tool execution
write execution report
```

Runner cannot:

```text
git push
git merge
git reset hard
git clean fd
modify .env
read secrets
terraform apply
terraform destroy
kubectl apply real cluster
kubectl delete
helm upgrade real cluster
ansible-playbook real server
restart service
deploy to cloud
execute exploit
run brute force
generate payload
```

### 21.2 Verification Engine

Verification Engine validates results. It does not fix.

Verification Engine checks:

```text
branch policy
changed files
denied path
secret pattern
diff limit
schema validation
unit tests
import checks
documentation checks
OpenAPI validation
AsyncAPI validation
YAML validation
DevOps config validation
security validation result parsing
```

### 21.3 Safety Gate

Safety Gate blocks unsafe request, patch, command, tool change, or commit request.

Safety Gate blocks:

```text
denied path access
secret access
unsafe command
destructive command
oversized diff
scope drift
unapproved dependency change
agent permission escalation
unapproved network scan
production data access
commit or push bypass attempt
Senior Reviewer bypass attempt
Safety Gate modification attempt
Commit Gate policy weakening
```

### 21.4 Commit Gate

Commit Gate creates local commit only when all conditions pass.

Commit Gate requires:

```text
manifest allows local commit
Senior approval exists
Safety Gate PASS
Verification Engine PASS
denied path check PASS
secret check PASS
branch policy PASS
diff limit PASS
commit_request.yaml exists
commit message valid
allow_push is false
```

Commit Gate must never push.

---

## 22. State Tools

### 22.1 Kanban

Kanban path:

```text
workspace/agent_workspace/kanban/board.json
```

Statuses:

```text
todo
picked
in_progress
blocked
needs_review
needs_revision
ready_for_senior
ready_for_runner
ready_for_verification
verification_failed
verified
commit_ready
done
rejected
human_required
```

### 22.2 Message Bus

Message bus path:

```text
workspace/agent_workspace/agents/{agent_id}/inbox/
workspace/agent_workspace/agents/{agent_id}/outbox/
```

Message types:

```text
task_assignment
artifact_ready
revision_request
specialist_review_request
validation_request
read_only_request
human_escalation
status_update
```

### 22.3 State Manager

State path:

```text
workspace/agent_workspace/state/{task_id}.state.json
```

State must include:

```text
task_id
run_id
target_system
stage
current_agent
last_successful_checkpoint
status
reason
retry_count
artifacts
blocked_by
```

### 22.4 Artifact Registry

Artifact registry path:

```text
workspace/agent_workspace/artifacts/{task_id}.artifact_index.json
```

Every artifact must be registered.

---

## 23. Manifest Contract

Every task must start with a manifest.

Required fields:

```yaml
task_id:
title:
target_system:
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

Recommended fields:

```yaml
owner:
priority:
branch:
created_at:
expected_artifacts:
validation_required:
human_gate_required:
max_revision_rounds:
max_dispatch_rounds:
notes:
```

Example:

```yaml
task_id: task-ai-rag-local-001
title: Add docs for collection import flow
target_system: ai_rag_local
risk_level: low
mode: plan
task_type: documentation
objective: Create a documentation plan for JSONL import flow.
allowed_paths:
  - docs/
  - README.md
denied_paths:
  - .env
  - .env.*
  - .git/
  - data/secrets/
required_outputs:
  - doc_gap_report
  - docs_plan
required_reviews:
  - senior_reviewer
stop_conditions:
  - manifest_invalid
  - evidence_missing
  - denied_path_needed
```

---

## 24. Routing Rules

Recommended file:

```text
config/selfdev/routing_rules.yaml
```

Initial routing:

```yaml
routing_rules:
  documentation:
    primary: adit
    required_review:
      - senior_reviewer

  implementation:
    primary: opung
    required_review:
      - senior_reviewer

  implementation_with_security_risk:
    primary: opung
    required_review:
      - asep
      - senior_reviewer

  implementation_with_devops_risk:
    primary: opung
    required_review:
      - doni
      - senior_reviewer

  security_review:
    primary: asep
    required_review:
      - senior_reviewer

  dependency_change:
    primary: doni
    required_review:
      - asep
      - senior_reviewer
    requires_human_review: true

  devops_review:
    primary: doni
    required_review:
      - senior_reviewer

  ci_or_docker:
    primary: doni
    required_review:
      - senior_reviewer

  runtime_issue:
    primary: supri
    required_review:
      - doni
      - senior_reviewer

  security_runtime_issue:
    primary: supri
    required_review:
      - asep
      - senior_reviewer

  docs_with_runtime_sop:
    primary: adit
    required_review:
      - supri
      - senior_reviewer

  agent_permission_change:
    primary: asep
    required_review:
      - senior_reviewer
    requires_human_review: true

  tool_registry_change:
    primary: asep
    required_review:
      - doni
      - senior_reviewer
    requires_human_review: true

  architecture_change:
    primary: senior_reviewer
    required_review:
      - asep
      - doni
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

## 25. Artifact Contract

### 25.1 Common Rules

Every artifact must:

```text
exist
be non-empty
match expected path
match expected format
include task_id
include agent_id or tool_id
include decision when applicable
include evidence when making findings
include affected files when applicable
be registered in artifact index
be linked from Kanban
```

### 25.2 Main Artifacts

| Artifact | Owner | Path |
|---|---|---|
| Orchestration plan | Siwa | `workspace/agent_workspace/orchestration/{task_id}.siwa_plan.md` |
| Artifact summary | Siwa | `workspace/agent_workspace/orchestration/{task_id}.artifact_summary.md` |
| Human review request | Siwa | `workspace/agent_workspace/requests/{task_id}.human_review_required.md` |
| Implementation plan | Opung | `workspace/agent_workspace/plans/{task_id}.opung_plan.md` |
| Draft patch | Opung | `workspace/agent_workspace/patches/{task_id}.opung_draft.patch` |
| Test draft patch | Opung | `workspace/agent_workspace/patches/{task_id}.opung_tests.patch` |
| Patch notes | Opung | `workspace/agent_workspace/notes/{task_id}.opung_notes.md` |
| Documentation plan | Adit | `workspace/agent_workspace/docs/{task_id}.adit_docs_plan.md` |
| Documentation gap report | Adit | `workspace/agent_workspace/docs/{task_id}.doc_gap_report.md` |
| Documentation patch | Adit | `workspace/agent_workspace/patches/{task_id}.adit_docs.patch` |
| Security review | Asep | `workspace/agent_workspace/reviews/{task_id}.asep_security_review.md` |
| Security validation request | Asep | `workspace/agent_workspace/requests/{task_id}.security_validation_request.yaml` |
| DevOps review | Doni | `workspace/agent_workspace/reviews/{task_id}.doni_devops_review.md` |
| DevOps validation request | Doni | `workspace/agent_workspace/requests/{task_id}.doni_validation_request.yaml` |
| Runtime summary | Supri | `workspace/agent_workspace/runtime/{task_id}.supri_runtime_summary.md` |
| Incident classification | Supri | `workspace/agent_workspace/runtime/{task_id}.supri_incident_classification.md` |
| Troubleshooting checklist | Supri | `workspace/agent_workspace/runtime/{task_id}.supri_troubleshooting_checklist.md` |
| Senior review | Senior Reviewer | `workspace/agent_workspace/reviews/senior/{task_id}.senior_review.md` |
| Revision request | Senior Reviewer | `workspace/agent_workspace/revision_requests/{task_id}.senior_revision_request.md` |
| Apply approval | Senior Reviewer | `workspace/agent_workspace/approvals/{task_id}.apply_approval.yaml` |
| Commit request | Senior Reviewer | `workspace/agent_workspace/approvals/{task_id}.commit_request.yaml` |
| Runner report | Runner | `workspace/agent_workspace/runner/{task_id}.runner_report.md` |
| Verification report | Verification Engine | `workspace/agent_workspace/verification/{task_id}.verification.md` |
| Safety report | Safety Gate | `workspace/agent_workspace/safety/{task_id}.safety_report.md` |
| Commit record | Commit Gate | `workspace/agent_workspace/commits/{task_id}.commit_record.md` |

---

## 26. Workflow Modes

### 26.1 Documentation Workflow

```text
Human Owner
  ↓
Manifest
  ↓
Siwa
  ↓
Adit
  ↓
Senior Reviewer
  ↓
Safety Gate if patch exists
  ↓
Runner if apply is approved
  ↓
Verification Engine
  ↓
Commit Gate if approved
```

### 26.2 Code Implementation Workflow

```text
Human Owner
  ↓
Manifest
  ↓
Siwa
  ↓
Opung
  ↓
Asep if security risk
  ↓
Doni if dependency, CI, config, or deployment risk
  ↓
Senior Reviewer
  ↓
Safety Gate
  ↓
Runner
  ↓
Verification Engine
  ↓
Senior Reviewer commit request
  ↓
Commit Gate
```

### 26.3 Runtime Issue Workflow

```text
Human Owner
  ↓
Manifest
  ↓
Siwa
  ↓
Supri
  ↓
Asep if security indicator
  ↓
Doni if service, CI, Docker, Terraform, Kubernetes, or deployment issue
  ↓
Senior Reviewer or Human Owner
```

### 26.4 DevOps Workflow

```text
Human Owner
  ↓
Manifest
  ↓
Siwa
  ↓
Doni
  ↓
Asep if secret, permission, supply-chain, auth, or security risk
  ↓
Senior Reviewer
  ↓
Safety Gate
  ↓
Runner safe validation only
  ↓
Verification Engine
```

### 26.5 Security Workflow

```text
Human Owner
  ↓
Manifest
  ↓
Siwa
  ↓
Asep
  ↓
Runner request only if authorized
  ↓
Verification Engine parses validation result
  ↓
Senior Reviewer
  ↓
Human Owner if high risk
```

---

## 27. Knowledge Base Policy

Knowledge base is not execution authority.

Allowed use:

```text
pattern reference
checklist
rubric
taxonomy
syntax reference
style reference
validation planning
offline evaluation
```

Disallowed use:

```text
automatic dependency adoption
copy external code without review
active scan without scope
production decision without local evidence
automatic framework migration
cloud deployment
secret handling
```

Every knowledge base item should include metadata:

```json
{
  "agent": "opung",
  "source_type": "coding_reference",
  "allowed_use": "pattern_or_reference_only",
  "runtime_dependency": false,
  "can_execute": false,
  "requires_runner": false,
  "risk": "low"
}
```

---

## 28. Performance Budget

System-level defaults:

```yaml
performance_budget:
  max_total_runtime_seconds: 900
  max_dispatch_rounds: 3
  max_revision_rounds: 2
  max_agent_wait_seconds: 300
  max_llm_calls_per_stage: 1
  max_context_chars: 30000
```

Agent-specific budgets:

| Agent | Files read | Reference chunks | LLM calls | Patch or report limit |
|---|---:|---:|---:|---|
| Siwa | 8 | 8 | 1 per stage | plan and summary only |
| Opung | 6 | 8 | 2 per task | 3 files, 180 added lines |
| Adit | 12 | 10 | 1 per stage | 5 files, 400 added lines |
| Asep | 10 | 12 | 2 per review | 350 report lines |
| Doni | 12 | 10 | 2 per review | 350 report lines |
| Supri | scoped inputs only | 10 | 2 per task | structured report only |
| Senior Reviewer | artifacts only plus diff | 10 | 2 per review | structured review only |

If budget is exceeded, write:

```text
workspace/agent_workspace/performance/{task_id}.performance_warning.md
```

---

## 29. Human Gate Triggers

Human Owner approval is required for:

```text
dependency change
architecture change
agent permission change
tool registry change
safety policy change
commit policy change
production data access
secret access
external active scan
ZAP active scan
Nuclei external target scan
Docusaurus migration
docs deployment
terraform plan against real environment
terraform apply
terraform destroy
kubectl apply real cluster
kubectl delete
helm upgrade real cluster
ansible-playbook real server
service restart
service stop
user creation
password change
SSH hardening
firewall change
backup restore
push
merge
release
production deploy
```

---

## 30. Failure Handling Matrix

| Failure | Detection | Response |
|---|---|---|
| Manifest invalid | Schema fail | Stop and write manifest error |
| Target system unknown | Registry lookup fail | Human review required |
| Routing unknown | No routing rule | Human review required |
| Agent timeout | Wait counter exceeded | Retry once, then blocked |
| Output schema invalid | Schema fail | Retry once, then human review |
| Artifact missing | Artifact Gate fail | Request missing artifact |
| Patch outside scope | Path scan fail | Block |
| Denied path touched | Scope check fail | Block |
| Secret detected | Secret scan fail | Critical block and Asep route |
| Unsafe command detected | Safety Gate | Block |
| Dependency change without approval | Safety Gate or Doni | Human review required |
| Security risk ignored | Senior Reviewer | Route to Asep |
| DevOps risk ignored | Senior Reviewer | Route to Doni |
| Runtime action requested | Supri Stop Gate | Human Owner required |
| Verification failed | Verification Engine | Request revision |
| Review loop exceeded | State Manager | Human review required |
| Commit request incomplete | Commit Gate | Block |
| Push requested | Safety Gate | Block and Human Owner only |

---

## 31. Initial Implementation Roadmap

### Phase 0: Contract Freeze

Deliverables:

```text
config/selfdev/target_systems.yaml
config/selfdev/agents.yaml
config/selfdev/tools.yaml
config/selfdev/agent_tool_grants.yaml
config/selfdev/routing_rules.yaml
schemas/selfdev/*.schema.json
```

Exit criteria:

```text
all schema files validate
all agents have explicit deny list
no agent can execute shell
no agent can commit
no agent can push
no agent can read .env or secrets
```

### Phase 1: Deterministic Skeleton

Deliverables:

```text
selfdev/tools/kanban.py
selfdev/tools/message_bus.py
selfdev/tools/artifact_registry.py
selfdev/runtime/state_manager.py
selfdev/agents/agent_registry.py
selfdev/agents/siwa_orchestrator.py
```

Exit criteria:

```text
a documentation task can route to Adit without LLM
a coding task can route to Opung without LLM
a runtime task can route to Supri without LLM
state and message files are written
```

### Phase 2: Specialist Artifacts

Deliverables:

```text
Opung implementation plan and draft patch
Adit docs plan and gap report
Asep security review
Doni DevOps review
Supri runtime summary
Senior review
```

Exit criteria:

```text
all artifacts follow contract
all artifacts are registered
missing artifact is detected
```

### Phase 3: Safety and Verification

Deliverables:

```text
Safety Gate report
Runner safe validation mode
Verification Engine report
```

Exit criteria:

```text
denied path is blocked
secret pattern is blocked
unsafe command is blocked
failed verification blocks commit
```

### Phase 4: Controlled Patch Apply

Deliverables:

```text
Senior apply approval
Runner git apply check
Runner approved patch apply
Verification report
```

Exit criteria:

```text
Runner can apply only approved final patch
Runner cannot execute denied commands
Verification Engine validates output
```

### Phase 5: Local Commit Gate

Deliverables:

```text
Senior commit request
Commit Gate validation
Local commit record
```

Exit criteria:

```text
Commit Gate creates local commit only after all PASS
allow_push is always false
Human Owner controls push and merge
```

---

## 32. Test Plan

Minimum tests:

```text
test_manifest_missing_required_field
test_target_system_unknown
test_routing_unknown_task_type
test_siwa_cannot_write_patch
test_opung_cannot_apply_patch
test_opung_patch_size_limit
test_adit_cannot_modify_source
test_adit_evidence_gap
test_asep_blocks_secret_exposure
test_asep_blocks_agent_shell_grant
test_doni_blocks_terraform_destroy
test_doni_blocks_plaintext_secret
test_supri_blocks_restart_request
test_supri_redacts_secret_log
test_senior_blocks_missing_artifact
test_senior_blocks_missing_verification
test_runner_blocks_denied_command
test_verification_fails_on_denied_path
test_safety_gate_blocks_push
test_commit_gate_requires_senior_review
test_commit_gate_requires_verification_pass
test_commit_gate_never_pushes
test_checkpoint_resume
test_revision_loop_limit
```

---

## 33. Acceptance Criteria

SelfDev is ready for early use if:

```text
can load target system registry
can load valid manifest
can reject invalid manifest
can route documentation task to Adit
can route implementation task to Opung
can route security review to Asep
can route DevOps review to Doni
can route runtime issue to Supri
can route final review to Senior Reviewer
can write Kanban state
can write message bus files
can collect artifacts
can detect missing artifacts
can block denied path
can block secret pattern
can block unsafe command
can request verification
can refuse commit when verification fails
can create local commit only after all required gates pass
cannot push automatically
```

---

## 34. Open Items

Items still need implementation-level confirmation:

```text
exact schema definitions
exact target adapter interface
exact patch format policy
exact Runner command allowlist
exact Verification Engine plugin interface
exact Safety Gate scanner rules
exact Commit Gate branch policy
exact storage format for artifact index
exact model loading strategy
exact Chroma or knowledge retrieval integration
exact dry-run CLI commands
exact UI or dashboard, if any
```

---

## 35. Final Revised Summary

SelfDev is now defined as a standalone local multi-agent self-development and maintenance system.

AI RAG Local is no longer the foundation. AI RAG Local is a managed system and assistant product that SelfDev can develop and maintain.

Final formula:

```text
SelfDev plans, routes, reviews, verifies, and prepares local commits.
Agents write artifacts.
Runner executes controlled actions.
Verification Engine proves results.
Safety Gate blocks risk.
Commit Gate creates local commits only after all checks pass.
Human Owner controls high-risk action, push, merge, release, and deployment.
```
