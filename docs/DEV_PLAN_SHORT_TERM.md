# Short-Term Development Plan

**Project:** SelfDev  
**Scope:** short-term implementation plan  
**Status:** active planning  
**Date:** 2026-05-07

## 1. Goal

The short-term goal is to turn SelfDev from a documentation-first repository into a tested local system skeleton.

The first development cycle must not create autonomous execution. It must create a stable contract layer.

## 2. Current Baseline

| Area | Status | Notes |
|---|---|---|
| General design document | Done in documentation | Needs root-level navigation from README |
| Core tools design | Done in documentation | Runner, Verification Engine, Safety Gate, Commit Gate defined |
| UI design | Done in documentation | Local web app first, wrapper later |
| Agent dev plans | Done in documentation | Siwa, Opung, Adit, Asep, Doni, Supri, Senior Reviewer available |
| Knowledge base docs | Done in documentation | Available per agent |
| Runtime code | Not implemented | Must start with deterministic skeleton |
| Config files | Not implemented | Must create `config/selfdev/*.yaml` |
| JSON schemas | Not implemented | Must create `schemas/selfdev/*.schema.json` |
| Tests | Not implemented | Must add config and relationship tests first |
| UI | Not implemented | Start read-only after state files exist |
| Runner | Not implemented | Start dry-run only |
| Verification Engine | Not implemented | Start schema and path checks only |
| Safety Gate | Not implemented | Start denied path and unsafe tool check |
| Commit Gate | Not implemented | Implement last |

## 3. Short-Term Phases

### Phase 0: Documentation Baseline

Deliverables:

```text
README.md
CHANGELOG.md
docs/SPECIFICATION.md
docs/DEV_PLAN_SHORT_TERM.md
docs/IMPLEMENTATION_STATUS.md
docs/TEST_PLAN.md
```

Exit criteria:

```text
Root README explains SelfDev as standalone system.
Short-term plan records done and not done items.
Specification defines required config, schema, tools, and tests.
```

### Phase 1: Repository Skeleton

Deliverables:

```text
config/selfdev/
schemas/selfdev/
selfdev/agents/
selfdev/tools/
selfdev/runtime/
selfdev/policies/
selfdev/api/
scripts/selfdev/
tests/selfdev/
data/agent_workspace/
```

Exit criteria:

```text
All required directories exist.
Directory validation test passes.
```

### Phase 2: Configuration Contract

Deliverables:

```text
config/selfdev/agents.yaml
config/selfdev/tools.yaml
config/selfdev/routing_rules.yaml
config/selfdev/workflow.yaml
config/selfdev/targets.yaml
config/selfdev/safety_policy.yaml
```

Exit criteria:

```text
All config files exist.
All agent IDs are unique.
All routing targets exist.
All tool references exist.
No non-core agent has forbidden execution tools.
```

### Phase 3: Schema Contract

Deliverables:

```text
schemas/selfdev/agents.schema.json
schemas/selfdev/tools.schema.json
schemas/selfdev/routing_rules.schema.json
schemas/selfdev/manifest.schema.json
schemas/selfdev/message.schema.json
schemas/selfdev/artifact.schema.json
```

Exit criteria:

```text
All config files validate against schemas.
Invalid sample config fails.
```

### Phase 4: Deterministic State and Workspace

Deliverables:

```text
data/agent_workspace/kanban/
data/agent_workspace/agents/
data/agent_workspace/manifests/
data/agent_workspace/artifacts/
data/agent_workspace/reviews/
data/agent_workspace/safety/
data/agent_workspace/verification/
data/agent_workspace/runner/
data/agent_workspace/audit/
```

Exit criteria:

```text
Workspace check passes.
No tool writes outside `data/agent_workspace` in early phase.
```

### Phase 5: Minimal Script Layer

Deliverables:

```text
scripts/selfdev/validate_config.py
scripts/selfdev/check_tool_grants.py
scripts/selfdev/check_routing.py
scripts/selfdev/check_workspace.py
scripts/selfdev/run_contract_tests.py
```

Exit criteria:

```text
All scripts run without modifying source files.
Scripts return non-zero exit code on contract failure.
```

### Phase 6: Minimal Runtime Stubs

Deliverables:

```text
selfdev/tools/safety_gate.py
selfdev/tools/verification_engine.py
selfdev/tools/runner.py
selfdev/tools/commit_gate.py
selfdev/runtime/state_manager.py
selfdev/runtime/message_bus.py
selfdev/runtime/kanban.py
```

Exit criteria:

```text
Each module can be imported.
No runtime module executes shell on import.
No runtime module reads `.env` directly.
```

### Phase 7: Read-Only UI Preparation

Deliverables:

```text
selfdev/api/routes/health.py
selfdev/api/routes/agents.py
selfdev/api/routes/tools.py
selfdev/api/routes/kanban.py
selfdev/api/routes/artifacts.py
```

Exit criteria:

```text
API is read-only.
No action endpoint exists yet.
```

## 4. Done and Not Done Tracker

| Goal | Done | Not Done |
|---|---:|---:|
| Define SelfDev as standalone system | Yes | No |
| Define AI RAG Local as first target system | Yes | No |
| Define all agents | Yes | No |
| Define core tools | Yes | No |
| Define UI plan | Yes | No |
| Root README | Planned now | Needs commit |
| Config YAML | No | Yes |
| JSON schemas | No | Yes |
| Tests | No | Yes |
| Runtime modules | No | Yes |
| API | No | Yes |
| Desktop wrapper | No | Yes |

## 5. Priority for Next Commit

Recommended first commit title:

```text
docs: add SelfDev project baseline and short-term development plan
```

Recommended second commit title:

```text
chore: add SelfDev repository skeleton and config contract tests
```

## 6. Non-Goals for Short-Term Phase

Do not implement:

```text
LLM agent execution
patch application
local commit
push
merge
deployment
autonomous shell
full desktop wrapper
full UI
remote API access
```

## 7. Definition of Done

Short-term phase is done when:

```text
README and docs are available.
Config files exist.
Schemas exist.
Config tests pass.
Relationship tests pass.
Workspace tests pass.
No agent has unsafe tool grants.
No execution path bypasses Runner, Verification Engine, Safety Gate, or Commit Gate.
```
