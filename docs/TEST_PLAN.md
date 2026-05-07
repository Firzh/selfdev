# Test Plan

## Purpose

This test plan defines the current SelfDev testing scope.

The test suite verifies contract consistency, config integrity, runtime skeleton behavior, manifest validation, routing, dispatch, artifact handling, and senior review flow.

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

Checks:

```text
routing rules load
documentation routes to Adit
implementation routes to Opung
dependency_change requires human review
invalid manifest does not route
CLI routes example manifest
```

### Dispatch Flow

Checks:

```text
documentation manifest creates message, state, and Kanban task
high-risk manifest goes to human_required
dispatch CLI accepts example manifest
```

### Artifact Registry and Artifact Gate

Checks:

```text
artifact can be registered
valid artifact passes gate
empty artifact fails
path escape fails
missing required artifact type fails
register artifact CLI works
```

### Artifact Collection Flow

Checks:

```text
artifact_ready reply registers artifact
Kanban is updated
state is updated
missing required artifact triggers needs_revision
invalid reply shape blocks collection
CLI collects artifact reply
```

### Senior Review Gate

Checks:

```text
approve_for_runner updates task to ready_for_verification
request_revision updates task to needs_revision
not-ready task is blocked
senior review CLI works
```

## Current Expected Result

All tests should pass before continuing.

Operator reported current state:

```text
Tests green
Commit completed
Local commit count: 12
```

## Required Test Rule

Before each commit:

```bash
python scripts/selfdev/run_contract_tests.py
```

Do not commit if tests are red.

## Next Test Scope

For the next phase, add tests for Safety Gate Integration:

```text
safety report is written
safety artifact is registered
safe changed paths pass
denied changed paths block
denied action blocks
Kanban is updated
state is updated
Runner is blocked when Safety Gate blocks
```
