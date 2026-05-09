# Milestone 03 Summary

## Milestone Name

Documentation Milestone 03

## Trigger

The implementation cycle after Documentation Milestone 02 completed. Documentation must be updated before continuing feature development.

## Completed Since Milestone 02

```text
Minimal UI Static Console
UI static file server route
Target registry read API
Artifact viewer read API
Redaction service skeleton
Redacted artifact preview helper
Redacted artifact preview read API
Static UI artifact preview panel
UI root asset path fix
```

## Current Safety Position

SelfDev is still deterministic.

No LLM agent is active.

No agent can execute shell.

No agent can apply patch.

No agent can commit.

No agent can push, merge, deploy, or release.

HTTP API is read-only. POST, PUT, and DELETE are rejected.

The static UI is read-only and must not expose mutation controls.

## Current Full Flow

```text
manifest
  ↓
validate
  ↓
route
  ↓
dispatch
  ↓
collect artifact
  ↓
senior review
  ↓
safety
  ↓
verification
  ↓
runner request validation
  ↓
commit readiness evaluation
  ↓
read-only API observation
  ↓
static UI observation
```

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
python scripts/selfdev/show_actions.py --task-id <task_id>
python scripts/selfdev/redact_text.py --text <text>
python scripts/selfdev/preview_artifact.py --artifact-id <artifact_id>
```

## New Contract Guarantees

```text
static UI assets are served from /ui paths
target IDs are single path segments
artifact IDs are single path segments
artifact detail reads are path-safe
artifact preview reads are bounded and redacted
JavaScript static asset MIME type is stable
UI has no mutation methods or unsafe action controls
```

## Next Work

```text
Static UI polish and read-only operator usability
UI artifact list to preview integration
UI target detail panel
Read-only API payload consistency pass
Redaction policy coverage expansion
```

## Required Commit Message

Recommended commit message for this documentation milestone:

```bash
git commit -m "docs: update SelfDev milestone 03 status"
```
