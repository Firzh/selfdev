# Milestone 04 Summary

## Milestone Name

Documentation Milestone 04

## Trigger

Documentation was refreshed after completing the Milestone 03 next-work list.
This document captures the read-only operator UI, read API payload envelope, and
expanded redaction policy contracts before the next implementation cycle.

## Completed Since Documentation Milestone 03

```text
Static UI polish and read-only operator usability
UI artifact list to preview integration
UI target detail panel
Read-only API payload consistency pass
Redaction policy coverage expansion
```

## Current Safety Position

SelfDev remains deterministic. No LLM execution is active. No agent command
execution is active. No agent can apply patches. No agent can write VCS history.
No push, merge, deployment, or release automation is active.

The HTTP API and static UI remain read-only observation surfaces.

## Current HTTP Endpoints

```text
GET /health
GET /summary
GET /agents
GET /tools
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
```

## Current CLI Read Surface

```text
python scripts/selfdev/read_api.py health
python scripts/selfdev/read_api.py summary
python scripts/selfdev/read_api.py targets
python scripts/selfdev/read_api.py target --target-id <target_id>
python scripts/selfdev/read_api.py artifacts
python scripts/selfdev/read_api.py artifact --artifact-id <artifact_id>
python scripts/selfdev/read_api.py artifact-preview --artifact-id <artifact_id>
python scripts/selfdev/check_read_api_payloads.py --resources health,summary
python scripts/selfdev/show_actions.py --task-id <task_id>
python scripts/selfdev/redact_text.py --text <text>
python scripts/selfdev/preview_artifact.py --artifact-id <artifact_id>
```

## New Contract Guarantees

```text
static UI read-only operator usability is documented
artifact cards can drive redacted preview reads
target detail reads are documented as read-only
read API response envelopes use selfdev.read_api.payload.v1
redaction covers common token, secret, URL, email, and user-path shapes
RedactionResult remains structured and legacy compatible
```

## Next Work

```text
Read API envelope parity for every endpoint and CLI command
Static UI empty, loading, and error state polish
Operator troubleshooting and smoke-check documentation
Artifact preview metadata and redaction finding presentation polish
Target and artifact filtering for read-only operator navigation
```
