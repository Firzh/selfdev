# SelfDev

SelfDev is a standalone local multi-agent self-development system.

SelfDev is not only a helper for `ai-rag-local`. The first managed target can be `ai-rag-local`, but the system is designed to maintain and develop multiple local systems, including RAG systems, agent systems, documentation systems, backend projects, DevOps configurations, and runtime workflows.

## Current Status

SelfDev is in the contract-first implementation phase.

The system currently has deterministic foundations for:

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

No LLM execution is active yet.

No shell execution is allowed through agents.

No commit, push, merge, deployment, or release automation is active.

## Core Principle

SelfDev follows a failure-first architecture.

Agents may fail. LLM output may be wrong. Tools may fail. Artifacts may be incomplete. The system must still remain safe, auditable, and recoverable.

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

| Component | Function |
|---|---|
| Runner | Controlled executor, not active as a real executor yet |
| Verification Engine | Deterministic validation layer |
| Safety Gate | Hard policy boundary |
| Commit Gate | Local commit readiness evaluator, not committing yet |

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
```

## Run Tests

```bash
python scripts/selfdev/run_contract_tests.py
```

## Validate Example Manifest

```bash
python scripts/selfdev/validate_manifest.py examples/manifests/task-docs-001.yaml
```

## Route Example Manifest

```bash
python scripts/selfdev/route_manifest.py examples/manifests/task-docs-001.yaml
```

## Dispatch Example Manifest

```bash
python scripts/selfdev/dispatch_manifest.py examples/manifests/task-docs-001.yaml
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
