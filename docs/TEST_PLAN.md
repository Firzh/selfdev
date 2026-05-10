# Test Plan

## Purpose

This test plan defines the current SelfDev testing scope. The test suite verifies contract consistency, config integrity, runtime skeleton behavior, manifest validation, routing, dispatch, artifact handling, review gates, dry run flow, read-only API behavior, static UI behavior, and redacted artifact preview behavior.

## Test Command

```bash
python scripts/selfdev/run_contract_tests.py
```

## Current Test Coverage

### Repository Structure

Verifies required directories and documentation files exist.

### Config Integrity

Verifies required config files exist:

```text
config/selfdev/agents.yaml
config/selfdev/tools.yaml
config/selfdev/routing_rules.yaml
config/selfdev/workflow.yaml
config/selfdev/targets.yaml
config/selfdev/safety_policy.yaml
```

### Agent Tool Grants

Checks:

```text
all allowed tools exist in tools.yaml
forbidden tools are not granted
baseline denied tools are explicitly denied
```

### Runtime Skeleton

Checks:

```text
StateManager write and read
MessageBus send and read
KanbanBoard create and update
Safety Gate blocks denied action
Safety Gate blocks denied path
Verification Engine detects missing file
Runner blocks denied action
Commit Gate blocks missing requirement
```

### Manifest Validator

Checks:

```text
valid manifest passes
missing required field fails
invalid risk level fails
denied path in allowed_paths fails
high-risk task requires human gate
manifest file validation works
CLI accepts example manifest
```

### Routing Gate

Checks deterministic routing by `task_type`.

### Dispatch Flow

Checks manifest dispatch to Kanban, State, and Message Bus.

### Artifact Registry and Artifact Gate

Checks artifact existence, non-empty content, type validation, required artifact checks, and path escape blocking.

### Artifact Collection Flow

Checks `artifact_ready` reply collection and status update.

### Senior Review Gate

Checks senior review decision mapping.

### Safety Gate Integration

Checks:

```text
safety report is written
safety artifact is registered
safe changed paths pass
denied changed paths block
denied action blocks
Kanban is updated
state is updated
```

### Verification Report Flow

Checks:

```text
verification report is written
required file PASS
missing file FAIL
Kanban is updated
state is updated
CLI PASS and FAIL exit codes
```

### Runner Request Flow

Checks:

```text
safe runner request is accepted
dangerous action is blocked
runner report is written
Kanban is updated
state is updated
CLI accepts and blocks correctly
```

### Commit Readiness Flow

Checks:

```text
required artifacts produce READY
missing artifacts produce BLOCKED
commit request report is written
no git commit is executed
```

### Full Deterministic Dry Run

Checks:

```text
manifest dispatch
mock artifact reply
artifact collection
senior review
safety
verification
runner
commit readiness
```

### Read-only API Service Layer

Checks:

```text
health
summary
agents
tools
kanban
artifacts
artifact detail
artifact preview
targets
target detail
state
action availability
```

### Read-only HTTP API

Checks:

```text
GET /health
GET /agents
GET /kanban
GET /artifacts
GET /artifacts/{artifact_id}
GET /artifact-previews/{artifact_id}
GET /state/{task_id}
GET /actions/{task_id}
GET /targets
GET /targets/{target_id}
GET /ui
GET /ui/index.html
GET /ui/app.js
GET /ui/styles.css
404 handling
405 for POST
invalid task_id rejection
invalid target_id rejection
invalid artifact_id rejection
static path traversal rejection
stable JavaScript content type
```

### API Action Availability Model

Checks action availability for:

```text
missing task
ready_for_senior
ready_for_verification
verified
commit_ready
human_required
```

### Static UI

Checks:

```text
index.html exists
app.js exists
styles.css exists
UI references read-only endpoints
UI does not contain mutation methods
UI does not expose shell, patch, commit, push, merge, deploy, or release actions
/ui loads assets from /ui paths
artifact preview panel is present
```

### Redaction and Artifact Preview

Checks:

```text
secret-like values are redacted
preview output is bounded
original secret values are not returned
unsafe artifact paths are blocked
missing artifacts return safe payloads
binary or non-UTF-8 content is not inlined
redaction markers remain visible in bounded previews
```

### Documentation Milestone 03

Checks:

```text
required documentation files mention Documentation Milestone 03
current read-only endpoints are documented
new static UI and redaction capabilities are documented
unsafe automation remains documented as not implemented
```

## Current Expected Result

All tests should pass before continuing.

Operator-reported expected state for this documentation milestone:

```text
Tests green
Implementation cycle after Documentation Milestone 02 completed
Documentation update required before next feature patch
```

## Required Test Rule

Before each commit:

```bash
python scripts/selfdev/run_contract_tests.py
```

Do not commit if tests are red.

## Next Test Scope

For the next phase, add tests for static UI polish and read-only operator usability:

```text
UI keeps read-only endpoint usage
UI remains framework-free
UI layout has stable named sections
UI does not introduce mutation controls
UI remains usable from /ui without a build step
```

<!-- SELFDEV:MILESTONE_04_START -->
## Documentation Milestone 04 Test Plan Addendum

### Focused Contract Tests

```bash
python -m pytest tests/selfdev/test_ui_operator_polish*.py -q
python -m pytest tests/selfdev/test_ui_artifact_list*.py -q
python -m pytest tests/selfdev/test_ui_target_detail*.py -q
python -m pytest tests/selfdev/test_read_api_payload_consistency.py -q
python -m pytest tests/selfdev/test_redaction_*compat.py tests/selfdev/test_redaction_policy_coverage.py -q
```

### Integration Regression Tests

```bash
python -m pytest tests/selfdev/test_artifact_preview_read_api.py tests/selfdev/test_redacted_artifact_preview.py -q
python -m pytest tests/selfdev/test_target_registry_read_api.py tests/selfdev/test_artifact_viewer_read_api.py -q
```

### Full Contract Suite

```bash
python scripts/selfdev/run_contract_tests.py
```
<!-- SELFDEV:MILESTONE_04_END -->
