# Short-Term Development Plan

## Purpose

This plan tracks the short-term implementation path for SelfDev.

SelfDev is a standalone local multi-agent self-development system. It can manage `ai-rag-local`, but it is not limited to `ai-rag-local`.

## Milestone Rule

Every 10 commits or 10 phases, documentation must be updated before adding new feature code.

Documentation update includes:

```text
README.md
CHANGELOG.md
docs/IMPLEMENTATION_STATUS.md
docs/DEV_PLAN_SHORT_TERM.md
docs/SPECIFICATION.md
docs/TEST_PLAN.md
```

## Completed Short-Term Goals

### Goal 1: Contract baseline

Status: Done

### Goal 2: Runtime skeleton

Status: Done

### Goal 3: Manifest validation

Status: Done

### Goal 4: Routing Gate

Status: Done

### Goal 5: Dispatch Flow

Status: Done

### Goal 6: Artifact Registry and Artifact Gate

Status: Done

### Goal 7: Artifact Collection Flow

Status: Done

### Goal 8: Senior Review Gate Skeleton

Status: Done

### Goal 9: Safety Gate Integration

Status: Done

Outputs:

```text
selfdev/runtime/safety_flow.py
scripts/selfdev/write_safety_decision.py
tests/selfdev/test_safety_flow.py
```

### Goal 10: Verification Report Flow

Status: Done

Outputs:

```text
selfdev/runtime/verification_flow.py
scripts/selfdev/write_verification_report.py
tests/selfdev/test_verification_flow.py
```

### Goal 11: Runner Request Flow

Status: Done

Outputs:

```text
selfdev/runtime/runner_flow.py
scripts/selfdev/write_runner_report.py
tests/selfdev/test_runner_flow.py
```

### Goal 12: Commit Readiness Flow

Status: Done

Outputs:

```text
selfdev/runtime/commit_readiness_flow.py
scripts/selfdev/evaluate_commit_readiness.py
tests/selfdev/test_commit_readiness_flow.py
```

### Goal 13: Full Dry Run

Status: Done

Outputs:

```text
selfdev/runtime/full_dry_run.py
scripts/selfdev/run_full_dry_run.py
tests/selfdev/test_full_dry_run.py
```

### Goal 14: Read-only API Service Layer

Status: Done

Outputs:

```text
selfdev/api/read_api.py
scripts/selfdev/read_api.py
tests/selfdev/test_read_api.py
```

### Goal 15: Local HTTP API Skeleton

Status: Done

Outputs:

```text
selfdev/api/http_server.py
scripts/selfdev/serve_read_api.py
tests/selfdev/test_http_read_api.py
```

### Goal 16: API Action Availability Model

Status: Done

Outputs:

```text
selfdev/api/action_availability.py
scripts/selfdev/show_actions.py
tests/selfdev/test_action_availability.py
```

### Goal 17: Expose Action Availability in HTTP API

Status: Done

Output:

```text
GET /actions/{task_id}
```

## Next Short-Term Goals

### Goal 18: Minimal UI Static Console

Status: Next

Required outputs:

```text
selfdev/ui/web/index.html
selfdev/ui/web/app.js
selfdev/ui/web/styles.css
tests/selfdev/test_ui_static_files.py
```

Expected behavior:

```text
static console can call read-only HTTP API
shows health
shows summary
shows task list
shows action availability
no mutation
no shell
no patch apply
no commit
```

### Goal 19: UI static file server route

Status: Pending

Expected output:

```text
GET /
GET /ui/app.js
GET /ui/styles.css
```

### Goal 20: Read-only target registry API

Status: Pending

Expected output:

```text
GET /targets
GET /targets/{target_id}
```

### Goal 21: Artifact viewer read API

Status: Pending

Expected output:

```text
GET /artifact/{artifact_id}
```

Must include path safety check and redaction placeholder.

### Goal 22: Redaction service skeleton

Status: Pending

Expected output:

```text
selfdev/api/redaction.py
```

### Goal 23: UI artifact browser

Status: Pending

Expected output:

```text
artifact list
artifact detail read-only view
redacted preview
```

## Do Not Implement Yet

```text
LLM calls
automatic patch application
automatic shell execution
automatic commit
push
merge
release
deployment
desktop wrapper
real scanner execution
write API actions
```
