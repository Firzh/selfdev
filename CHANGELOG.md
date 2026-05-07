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

### Changed

- Reframed SelfDev as a standalone system rather than a subsystem of `ai-rag-local`.
- Clarified that `ai-rag-local` is only the first managed target system.
- Clarified that agents cannot execute shell commands, apply patches, commit, push, merge, deploy, or release.
- Clarified that execution must go through controlled runtime components.
- Clarified that Runner remains a validator in the current phase.
- Clarified that Commit Gate evaluates readiness only and does not execute `git commit`.
- Expanded read-only API capabilities for future UI integration.

### Security

- Added denied tool baseline for all agents.
- Added denied path baseline for `.env`, `.env.*`, `.git/`, and `data/secrets/`.
- Added initial Safety Gate checks for denied actions and denied paths.
- Added artifact path escape validation.
- Added human gate requirement for high-risk task types.
- Added HTTP rejection for POST, PUT, and DELETE in read-only API.
- Added task ID single-segment validation for `/state/{task_id}` and `/actions/{task_id}`.
- Added action availability model so UI does not infer authority client-side.

### Tests

- Contract tests are green at Documentation Milestone 02.
- Current local commit count reported by operator: 22.
