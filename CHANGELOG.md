# Changelog

All notable changes to SelfDev will be documented in this file.

This project uses a simple changelog format.

## Unreleased

### Added

- Added root project README for SelfDev as a standalone local multi-agent self-development system.
- Added short-term development plan for documentation, repository skeleton, config contract, schema contract, and test contract.
- Added system specification for agents, core tools, target systems, config files, schemas, workspace, and test coverage.
- Added implementation status tracker to separate completed documentation from missing runtime implementation.
- Added test plan for config integrity, routing, tool grants, workspace structure, and script relationships.

### Changed

- Reframed SelfDev from an AI RAG Local helper into a standalone system that can manage AI RAG Local and other local projects.
- Reframed AI RAG Local as the first managed target system rather than the foundation of SelfDev.

### Fixed

- No runtime fixes yet. Runtime implementation has not started.

### Security

- Documented deny-by-default rule for agent tools.
- Documented that no agent may push, merge, release, read secrets, modify `.env`, or run arbitrary shell.

## 0.0.0-docs-baseline

### Added

- Initial design documents under `docs/`.
- Agent development plans under `docs/agents/`.
- Agent knowledge base documents under `docs/knowledge_base/`.
