# SelfDev Test Plan

**Status:** initial test plan  
**Date:** 2026-05-07

## 1. Purpose

The first test suite must verify that SelfDev configuration, scripts, and module relationships are coherent before any autonomous workflow is implemented.

## 2. Test Philosophy

Test contracts before testing intelligence.

The first tests do not need LLM calls. They must verify deterministic structure.

## 3. Test Groups

### 3.1 Repository Structure Tests

Checks:

```text
required folders exist
required documentation exists
required config folder exists
required schema folder exists
required script folder exists
required test folder exists
```

### 3.2 Config Integrity Tests

Checks:

```text
agents.yaml exists
tools.yaml exists
routing_rules.yaml exists
workflow.yaml exists
targets.yaml exists
safety_policy.yaml exists
```

### 3.3 Agent Registry Tests

Checks:

```text
required agents exist
agent IDs are unique
each agent has role, model, allowed_tools, denied_tools
normal agents do not have forbidden tools
Senior Reviewer cannot commit directly
Siwa cannot write patch
Opung cannot apply patch
Adit cannot modify source code
Asep cannot run scanner directly
Doni cannot deploy
Supri cannot run shell
```

### 3.4 Tool Registry Tests

Checks:

```text
every tool has ID, category, risk level
every tool grant references known tool
execution tools are marked as gated
core tools exist
forbidden tools are denied by default
```

### 3.5 Routing Tests

Checks:

```text
every routing primary agent exists
every required reviewer exists
high-risk routes require human review
dependency change routes to Doni and requires Asep and Senior Reviewer
runtime issue routes to Supri and requires Doni and Senior Reviewer
```

### 3.6 Workspace Tests

Checks:

```text
data/agent_workspace folders exist
agent inbox/outbox folders exist or can be created
artifact paths are inside workspace
path traversal is rejected
```

### 3.7 Script Relationship Tests

Checks:

```text
scripts exist
scripts are import-safe
scripts do not execute shell on import
scripts have main guard
scripts return non-zero on failed validation
```

### 3.8 Core Module Import Tests

Checks:

```text
selfdev.tools.safety_gate imports
selfdev.tools.verification_engine imports
selfdev.tools.runner imports
selfdev.tools.commit_gate imports
selfdev.runtime.state_manager imports
selfdev.runtime.message_bus imports
selfdev.runtime.kanban imports
```

## 4. First Test Command

```bash
python scripts/selfdev/run_contract_tests.py
```

Equivalent direct command:

```bash
pytest tests/selfdev -q
```

## 5. Minimum Passing Criteria

The first passing state requires:

```text
all required files exist
all required folders exist
all required agents exist
all routing references resolve
all tool grants resolve
no unsafe tool is granted to normal agents
workspace paths are valid
scripts are present
```

## 6. Tests to Add Later

```text
manifest schema validation
message schema validation
artifact schema validation
Safety Gate denied path check
Safety Gate secret pattern check
Runner denied action check
Verification Engine report check
Commit Gate pass/fail check
UI action availability check
```
