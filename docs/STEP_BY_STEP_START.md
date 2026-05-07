# Step-by-Step Start

## Step 1: Add Documentation

Copy these files:

```text
README.md
CHANGELOG.md
docs/DEV_PLAN_SHORT_TERM.md
docs/SPECIFICATION.md
docs/IMPLEMENTATION_STATUS.md
docs/TEST_PLAN.md
```

Commit:

```bash
git add README.md CHANGELOG.md docs/DEV_PLAN_SHORT_TERM.md docs/SPECIFICATION.md docs/IMPLEMENTATION_STATUS.md docs/TEST_PLAN.md
git commit -m "docs: add SelfDev project baseline"
```

## Step 2: Create Folder Skeleton

```bash
mkdir -p config/selfdev schemas/selfdev
mkdir -p selfdev/{agents,tools,runtime,policies,api}
mkdir -p scripts/selfdev tests/selfdev
mkdir -p data/agent_workspace/{kanban,agents,manifests,orchestration,plans,patches,docs,reviews,safety,verification,runner,approvals,requests,audit,state,logs,traces,performance,errors}
```

Add placeholder files:

```bash
touch selfdev/__init__.py
for d in agents tools runtime policies api; do touch selfdev/$d/__init__.py; done
```

## Step 3: Add Initial Config Files

Create:

```text
config/selfdev/agents.yaml
config/selfdev/tools.yaml
config/selfdev/routing_rules.yaml
config/selfdev/workflow.yaml
config/selfdev/targets.yaml
config/selfdev/safety_policy.yaml
```

## Step 4: Add Test Scripts

Create files under:

```text
tests/selfdev/
scripts/selfdev/
```

Use the script bundle from this response.

## Step 5: Run First Tests

```bash
python scripts/selfdev/run_contract_tests.py
```

Or:

```bash
pytest tests/selfdev -q
```

## Step 6: Only After Tests Pass

Start deterministic modules:

```text
selfdev/runtime/state_manager.py
selfdev/runtime/message_bus.py
selfdev/runtime/kanban.py
selfdev/tools/safety_gate.py
selfdev/tools/verification_engine.py
selfdev/tools/runner.py
selfdev/tools/commit_gate.py
```

Do not implement LLM agent execution yet.
