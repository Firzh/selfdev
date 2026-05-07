# SelfDev

SelfDev is a standalone local multi-agent self-development system.

SelfDev is not only a helper for `ai-rag-local`. The first managed target can be `ai-rag-local`, but the system is designed to maintain and develop multiple local systems, including RAG systems, agent systems, documentation systems, backend projects, DevOps configurations, runtime workflows, and local operator consoles.

## Current Status

SelfDev is in the deterministic contract-first implementation phase.

The system currently supports:

- repository contract tests
- baseline configuration
- runtime skeleton
- manifest validation
- deterministic routing
- message dispatch
- artifact registry
- artifact gate
- artifact collection
- senior review gate
- safety gate integration
- verification report flow
- runner request flow
- commit readiness flow
- full deterministic dry run
- read-only API service layer
- read-only local HTTP API
- API action availability model
- `/actions/{task_id}` HTTP endpoint

No LLM execution is active yet.

No shell execution is allowed through agents.

No patch application, real git commit, push, merge, deployment, or release automation is active.

## Core Principle

SelfDev follows a failure-first architecture.

Agents may fail. LLM output may be wrong. Tools may fail. Artifacts may be incomplete. The system must still remain safe, auditable, deterministic, and recoverable.

## Main Agents

| Agent | Role | Execution Authority |
|---|---|---:|
| Siwa Miwa | Orchestrator, planner, router, dispatcher | No |
| Opung | Small scoped coding implementer | No |
| Adit | Documentation agent | No |
| Asep | Defensive security reviewer | No |
| Doni | DevOps reviewer | No |
| Supri | Read-only sysadmin analyst | No |
| Senior Reviewer | Final review gate | No |

## Core Runtime Components

| Component | Function | Current State |
|---|---|---|
| Runner | Controlled executor | Request validator only |
| Verification Engine | Deterministic validation layer | Report writer for required files |
| Safety Gate | Hard policy boundary | Denied action and path checker |
| Commit Gate | Commit readiness evaluator | Does not run git commit |

## Current Safe Flow

```text
Manifest
  ↓
Manifest Validator
  ↓
Routing Gate
  ↓
Dispatcher
  ↓
Kanban + State + Message Bus
  ↓
Agent Artifact Reply
  ↓
Artifact Collector
  ↓
Artifact Registry + Artifact Gate
  ↓
Senior Review Gate
  ↓
Safety Gate
  ↓
Verification Report Flow
  ↓
Runner Request Flow
  ↓
Commit Readiness Flow
```

## Full Dry Run

```bash
python scripts/selfdev/run_full_dry_run.py examples/manifests/task-docs-001.yaml
```

## Run Tests

```bash
python scripts/selfdev/run_contract_tests.py
```

## Read-only API CLI

```bash
python scripts/selfdev/read_api.py health
python scripts/selfdev/read_api.py summary
python scripts/selfdev/show_actions.py --task-id <task_id>
```

## Read-only HTTP API

Check mode:

```bash
python scripts/selfdev/serve_read_api.py --check
```

Run server:

```bash
python scripts/selfdev/serve_read_api.py --host 127.0.0.1 --port 8765
```

Available read-only endpoints:

```text
GET /health
GET /summary
GET /agents
GET /tools
GET /kanban
GET /artifacts
GET /state/{task_id}
GET /actions/{task_id}
```

## Development Rule

Every 10 commits or 10 implementation phases, update the project documentation before continuing feature development.

Required docs to update:

- `README.md`
- `CHANGELOG.md`
- `docs/IMPLEMENTATION_STATUS.md`
- `docs/DEV_PLAN_SHORT_TERM.md`
- `docs/SPECIFICATION.md`
- `docs/TEST_PLAN.md`
