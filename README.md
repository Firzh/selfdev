# SelfDev

SelfDev is a local, failure-first, multi-agent self-development system.

SelfDev is designed as a standalone system. It is not only an extension of `ai-rag-local`. The original goal was to help develop and maintain `ai-rag-local`, but the long-term scope is broader. SelfDev can manage AI RAG Local, its own codebase, documentation systems, local automation tools, DevOps configuration, runtime procedures, and future local agent systems.

## Current Status

SelfDev is currently in the documentation and contract-freeze stage.

The repository already contains the main design documents in `docs/`, including the revised general design document, core tools and agent tooling document, UI control panel plan, UI tooling plan, agent development plans, and knowledge base documents.

The next step is not to build a large agent runtime immediately. The next step is to freeze the repository structure, create configuration contracts, create schema validation, and add tests that prove every configuration file and script relationship is valid.

## What SelfDev Is

SelfDev is a local operator-controlled system for:

- creating task manifests;
- routing work to specialist agents;
- producing small scoped patches;
- producing documentation updates;
- reviewing security risk;
- reviewing DevOps and runtime risk;
- collecting artifacts;
- validating outputs;
- enforcing safety policy;
- preparing local commit readiness.

## What SelfDev Is Not

SelfDev is not an autonomous production engineer.

SelfDev must not:

- push automatically;
- merge automatically;
- release automatically;
- deploy automatically;
- read secrets;
- modify `.env`;
- bypass Safety Gate;
- bypass Senior Reviewer;
- bypass Verification Engine;
- run arbitrary shell through an agent.

## High-Level Architecture

```text
Human Owner
  ↓
UI Control Panel or CLI
  ↓
Task Manifest
  ↓
Siwa Miwa
  ↓
Specialist Agents
  ├── Opung
  ├── Adit
  ├── Asep
  ├── Doni
  └── Supri
  ↓
Senior Reviewer
  ↓
Safety Gate
  ↓
Runner
  ↓
Verification Engine
  ↓
Commit Gate
  ↓
Local commit candidate
```

## Agent Roles

| Agent | Role | Execution Permission |
|---|---|---:|
| Siwa Miwa | Orchestrator, planner, router, dispatcher, artifact evaluator | No |
| Opung | Small scoped coding implementer and draft patch writer | No |
| Adit | Documentation architect and documentation maintainer | No |
| Asep | Defensive security reviewer and vulnerability intelligence analyst | No |
| Doni | DevOps, CI/CD, IaC, deployment, observability, and runtime reviewer | No |
| Supri | Read-only sysadmin, runtime, log, and incident analyst | No |
| Senior Reviewer | Final code reviewer and commit-readiness evaluator | No |

## Core Tools

| Tool | Function | Execution Risk |
|---|---|---:|
| Runner | Controlled executor for approved checks and patch application | High |
| Verification Engine | Deterministic validator for schema, tests, policy, and artifacts | Medium |
| Safety Gate | Hard policy boundary for denied paths, secrets, unsafe commands, and escalation | Critical |
| Commit Gate | Local commit controller after all approvals pass | High |

## Recommended Repository Structure

```text
selfdev/
├── README.md
├── CHANGELOG.md
├── docs/
│   ├── SPECIFICATION.md
│   ├── DEV_PLAN_SHORT_TERM.md
│   ├── IMPLEMENTATION_STATUS.md
│   ├── TEST_PLAN.md
│   ├── SELFDEV_GENERAL_DESIGN_DOCUMENT_REVISED.md
│   ├── SELFDEV_CORE_TOOLS_AND_AGENT_TOOLING_REVISED.md
│   ├── SELFDEV_UI_CONTROL_PANEL_FAILURE_FIRST_DEVELOPMENT_PLAN.md
│   ├── SELFDEV_UI_TOOLING_AND_WRAPPER_DECISION.md
│   ├── agents/
│   └── knowledge_base/
├── config/
│   └── selfdev/
├── schemas/
│   └── selfdev/
├── selfdev/
│   ├── agents/
│   ├── tools/
│   ├── runtime/
│   ├── policies/
│   └── api/
├── scripts/
│   └── selfdev/
└── tests/
    └── selfdev/
```

## Short-Term Development Rule

Build in this order:

1. Documentation baseline.
2. Repository skeleton.
3. Configuration files.
4. JSON schemas.
5. Configuration tests.
6. Relationship tests.
7. Deterministic tools.
8. Message bus and Kanban.
9. Safety Gate stub.
10. Verification Engine stub.
11. Runner in dry-run mode.
12. UI read-only dashboard.

Do not start with autonomous agent execution.

## First Local Setup

```bash
git clone https://github.com/Firzh/selfdev.git
cd selfdev
mkdir -p config/selfdev schemas/selfdev selfdev/{agents,tools,runtime,policies,api} scripts/selfdev tests/selfdev data/agent_workspace
```

Then add the documentation files in this package.

## First Test Goal

The first test suite must prove:

- every required config exists;
- every agent has a model, role, allowed tools, and denied tools;
- every routing target exists in the agent registry;
- every tool grant references a known tool;
- no non-core agent has commit, push, merge, release, arbitrary shell, or secret access;
- workspace folders exist;
- scripts referenced by tests exist.

## Safety Baseline

The default policy is deny-by-default.

An agent can only do what its role, manifest, tool grant, and Safety Gate allow.
