# Short-Term Development Plan

## Purpose

This plan tracks the short-term implementation path for SelfDev. SelfDev is a standalone local multi-agent self-development system. It can manage `ai-rag-local`, but it is not limited to `ai-rag-local`.

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

### Goal 10: Verification Report Flow
Status: Done

### Goal 11: Runner Request Flow
Status: Done

### Goal 12: Commit Readiness Flow
Status: Done

### Goal 13: Full Dry Run
Status: Done

### Goal 14: Read-only API Service Layer
Status: Done

### Goal 15: Local HTTP API Skeleton
Status: Done

### Goal 16: API Action Availability Model
Status: Done

### Goal 17: Expose Action Availability in HTTP API
Status: Done

### Goal 18: Minimal UI Static Console
Status: Done
Outputs:

```text
selfdev/ui/web/index.html
selfdev/ui/web/app.js
selfdev/ui/web/styles.css
tests/selfdev/test_ui_static_files.py
```

### Goal 19: UI static file server route
Status: Done
Outputs:

```text
GET /ui
GET /ui/index.html
GET /ui/app.js
GET /ui/styles.css
```

### Goal 20: Read-only target registry API
Status: Done
Outputs:

```text
GET /targets
GET /targets/{target_id}
python scripts/selfdev/read_api.py targets
python scripts/selfdev/read_api.py target --target-id <target_id>
```

### Goal 21: Artifact viewer read API
Status: Done
Outputs:

```text
GET /artifacts/{artifact_id}
python scripts/selfdev/read_api.py artifact --artifact-id <artifact_id>
```

### Goal 22: Redaction service skeleton
Status: Done
Outputs:

```text
selfdev/runtime/redaction.py
scripts/selfdev/redact_text.py
tests/selfdev/test_redaction_service_skeleton.py
```

### Goal 23: Redacted artifact preview helper
Status: Done
Outputs:

```text
selfdev/runtime/artifact_preview.py
scripts/selfdev/preview_artifact.py
tests/selfdev/test_redacted_artifact_preview.py
```

### Goal 24: Expose redacted artifact preview through read API
Status: Done
Outputs:

```text
GET /artifact-previews/{artifact_id}
python scripts/selfdev/read_api.py artifact-preview --artifact-id <artifact_id>
```

### Goal 25: Add artifact preview panel to static UI
Status: Done
Outputs:

```text
selfdev/ui/web/index.html
selfdev/ui/web/app.js
selfdev/ui/web/styles.css
tests/selfdev/test_ui_artifact_preview_panel.py
```

### Goal 26: Fix static UI root asset paths
Status: Done
Outputs:

```text
/ui loads /ui/styles.css
/ui loads /ui/app.js
tests/selfdev/test_ui_root_asset_paths.py
```

## Next Short-Term Goals

### Goal 27: Documentation Milestone 03
Status: Current
Expected output:

```text
README.md
CHANGELOG.md
docs/IMPLEMENTATION_STATUS.md
docs/DEV_PLAN_SHORT_TERM.md
docs/SPECIFICATION.md
docs/TEST_PLAN.md
docs/MILESTONE_03_SUMMARY.md
tests/selfdev/test_milestone_03_docs.py
```

### Goal 28: Static UI polish and read-only operator usability
Status: Next
Expected behavior:

```text
improve layout and typography
make status cards easier to scan
keep zero build step
keep framework-free static files
keep read-only API calls only
keep no mutation controls
```

### Goal 29: UI artifact list to preview integration
Status: Pending
Expected behavior:

```text
select artifact from artifact list
load redacted preview without manual ID copying
keep preview bounded and redacted
```

### Goal 30: UI target detail panel
Status: Pending
Expected behavior:

```text
list targets
select one target
show read-only target details
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
UI mutation controls
```

<!-- SELFDEV:MILESTONE_04_START -->
## Short-term Plan After Documentation Milestone 04

### Completed Work Now Captured

```text
Static UI polish and read-only operator usability
UI artifact list to preview integration
UI target detail panel
Read-only API payload consistency pass
Redaction policy coverage expansion
```

### Next Work Candidates

```text
Read API envelope parity for every endpoint and CLI command
Static UI empty, loading, and error state polish
Operator troubleshooting and smoke-check documentation
Artifact preview metadata and redaction finding presentation polish
Target and artifact filtering for read-only operator navigation
```

### Guardrails For Next Work

```text
Keep HTTP API read-only
Reject POST, PUT, and DELETE
Do not expose mutation controls in static UI
Keep artifact previews bounded and redacted
Keep RedactionResult backward compatible
Keep all additions deterministic and contract-tested
```
<!-- SELFDEV:MILESTONE_04_END -->
