# Changelog

All notable changes to SelfDev are documented here.

## Unreleased

### Added

- Added baseline documentation for SelfDev as a standalone local multi-agent system.
- Added contract test runner.
- Added baseline repository structure checks.
- Added baseline config integrity tests.
- Added agent tool grant tests.
- Added deterministic runtime skeleton.
- Added file-based `StateManager`.
- Added file-based `MessageBus`.
- Added file-based `KanbanBoard`.
- Added initial deterministic `Safety Gate`.
- Added initial deterministic `Verification Engine`.
- Added non-executing `Runner` skeleton.
- Added non-committing `Commit Gate` readiness evaluator.
- Added manifest schema file.
- Added manifest validator.
- Added manifest validation CLI.
- Added example manifest under `examples/manifests/`.
- Added deterministic routing gate.
- Added routing CLI.
- Added dispatch flow from manifest to Kanban, state, and message bus.
- Added artifact registry.
- Added artifact gate.
- Added artifact registration CLI.
- Added artifact collection flow.
- Added senior review gate skeleton.
- Added senior review CLI.
- Added Safety Gate integration flow.
- Added safety decision CLI.
- Added Verification Report Flow.
- Added verification report CLI.
- Added Runner Request Flow.
- Added runner report CLI.
- Added Commit Readiness Flow.
- Added commit readiness CLI.
- Added Full Deterministic Dry Run Flow.
- Added full dry run CLI.
- Added read-only API service layer.
- Added read-only API CLI.
- Added minimal local HTTP API skeleton with Python standard library.
- Added HTTP CLI server.
- Added API Action Availability Model.
- Added action availability CLI.
- Added `/actions/{task_id}` endpoint to read-only HTTP API.
- Added minimal static operator console under `selfdev/ui/web/`.
- Added static UI serving through `GET /ui`, `GET /ui/index.html`, `GET /ui/app.js`, and `GET /ui/styles.css`.
- Added target registry read API through `GET /targets`, `GET /targets/{target_id}`, and matching CLI commands.
- Added artifact viewer read API through `GET /artifacts/{artifact_id}` and matching CLI command.
- Added deterministic redaction service skeleton and `scripts/selfdev/redact_text.py`.
- Added redacted artifact preview helper and `scripts/selfdev/preview_artifact.py`.
- Added redacted artifact preview read API through `GET /artifact-previews/{artifact_id}` and matching CLI command.
- Added redacted artifact preview panel to the static UI.
- Added absolute UI asset paths so `/ui` loads `styles.css` and `app.js` reliably.

### Changed

- Reframed SelfDev as a standalone system rather than a subsystem of `ai-rag-local`.
- Clarified that `ai-rag-local` is only the first managed target system.
- Clarified that agents cannot execute shell commands, apply patches, commit, push, merge, deploy, or release.
- Clarified that execution must go through controlled runtime components.
- Clarified that Runner remains a validator in the current phase.
- Clarified that Commit Gate evaluates readiness only and does not execute `git commit`.
- Expanded read-only API capabilities for future UI integration.
- Expanded the static UI from a basic read-only console to include target registry and redacted artifact preview surfaces.

### Security

- Added denied tool baseline for all agents.
- Added denied path baseline for `.env`, `.env.*`, `.git/`, and `data/secrets/`.
- Added initial Safety Gate checks for denied actions and denied paths.
- Added artifact path escape validation.
- Added human gate requirement for high-risk task types.
- Added HTTP rejection for POST, PUT, and DELETE in read-only API.
- Added task ID single-segment validation for `/state/{task_id}` and `/actions/{task_id}`.
- Added target ID and artifact ID single-segment validation for read API paths.
- Added action availability model so UI does not infer authority client-side.
- Added deterministic secret redaction for environment-style secrets, bearer tokens, GitHub tokens, and generic secret keys.
- Added bounded redacted artifact previews so sensitive content is masked before operator display.
- Kept UI read-only: no shell, patch, commit, push, merge, deploy, release, or mutation controls.

### Tests

- Contract tests are green at Documentation Milestone 03.
- Documentation Milestone 03 records the implementation cycle after Documentation Milestone 02.
- The cycle completed the static UI console, UI static serving, target registry read API, artifact viewer read API, redaction skeleton, redacted artifact preview helper, redacted preview API, artifact preview UI panel, and UI root asset path fix.

<!-- SELFDEV:MILESTONE_04_START -->
## Documentation Milestone 04 - Read-only operator surface stabilized

Date: 2026-05-11

### Added

- Documented the completed static operator UI polish cycle.
- Documented artifact browser to redacted preview integration.
- Documented target detail panel read-only observation flow.
- Documented the read API payload consistency contract.
- Documented Redaction policy coverage expansion for deterministic secret masking.
- Added Milestone 04 summary documentation.

### Changed

- Refreshed implementation status, short-term development plan, specification,
  and test plan around the current read-only operator and API contracts.

### Safety

- SelfDev remains deterministic and read-only at the operator/API boundary.
- No LLM execution, command execution, patch application, VCS write, push, merge,
  deploy, or release automation is active.
<!-- SELFDEV:MILESTONE_04_END -->
