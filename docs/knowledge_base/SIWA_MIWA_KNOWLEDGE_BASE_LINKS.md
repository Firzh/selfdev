# Siwa Miwa Knowledge Base Links

**Agent:** Siwa Miwa  
**Role:** Local AI agent orchestrator, planner, router, dispatcher, evaluator, and human-gate manager  
**Purpose:** daftar rujukan knowledge base untuk agent routing policy, tool selection policy, multi-agent workflow pattern, handoff protocol, agent evaluation rubric, task decomposition prompt, dan local AI agent orchestration  
**Created:** 2026-05-05 19:29:19

---

# 1. Fungsi Knowledge Base Siwa Miwa

Knowledge base ini dipakai untuk memperkuat Siwa Miwa sebagai **orchestrator agent**.

Siwa Miwa memakai referensi ini untuk:

```text
agent routing policy
tool selection policy
multi-agent workflow pattern
handoff protocol
agent evaluation rubric
task decomposition prompt
local AI agent orchestration
workflow state machine
human-in-the-loop gate
agent registry and tool registry governance
```

Siwa Miwa tidak boleh memakai referensi ini sebagai izin untuk:

```text
menulis source code patch
apply patch
run shell
commit
push
merge
release
modify .env
read secrets
bypass Safety Gate
bypass Senior Reviewer
```

Prinsip dasar:

```text
References = pattern and knowledge
Runtime authority = local policy
Execution = Runner or deterministic tools
High-risk action = Human Owner approval
```

---

# 2. Core Base Knowledge untuk Siwa Miwa

| Domain | Isi yang perlu dipahami | Fungsi Siwa |
|---|---|---|
| Agent routing policy | Rule untuk memilih agent berdasarkan task type, risk, file type, dan required review | Menentukan Opung, Adit, Asep, Doni, Supri, atau Senior Reviewer |
| Tool selection policy | Allow/deny tool, trusted operation, permission boundary | Mencegah agent memakai tool di luar scope |
| Multi-agent workflow pattern | Sequential, parallel, handoff, supervisor, reviewer, evaluator | Menyusun alur kerja agent |
| Handoff protocol | Structured message, task assignment, artifact return, revision request | Mengirim pekerjaan ke agent lain |
| Agent evaluation rubric | Artifact completeness, evidence, format compliance, risk, verification readiness | Mengevaluasi output agent |
| Task decomposition prompt | Memecah request besar menjadi subtask kecil | Membuat Kanban subtask |
| Local AI orchestration | State machine, checkpoint, local runner, file-based workspace | Mengatur workflow lokal tanpa cloud dependency |

---

# 3. Agent Routing Policy Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Mentis | https://github.com/foreveryh/mentis | Planner, supervisor, specialist agent routing, evaluator loop |
| 2 | Multi-Agent Orchestration Framework | https://github.com/yx-fan/multi-agent-orchestration-framework | AgentRouter, YAML workflow config, StateManager pattern |
| 3 | A2A Multi-Agent System Prototype | https://github.com/tubasarikaya/a2a-multi-agent-system-prototype | Main orchestrator, department orchestrator, specialist routing, task dependency |
| 4 | AI Orc | https://github.com/fabi29061985/ai-orc | Hierarchical process: organization, department, task agent |
| 5 | LangGraph Agent | https://github.com/moiz-q/langgraph-agent | Planner, router, evaluator, conditional routing, loop control |

Use for Siwa:

```text
Select agent by task type.
Route implementation to Opung.
Route documentation to Adit.
Route security risk to Asep.
Route DevOps/CI/IaC risk to Doni.
Route runtime issue to Supri.
Route final review to Senior Reviewer.
Escalate high-risk task to Human Owner.
```

Suggested local file:

```text
config/routing_rules.yaml
```

Example:

```yaml
routing_rules:
  implementation:
    primary: opung
    required_review:
      - senior_reviewer

  documentation:
    primary: adit
    required_review:
      - senior_reviewer

  security_review:
    primary: asep
    required_review:
      - senior_reviewer

  devops_review:
    primary: doni
    required_review:
      - senior_reviewer

  runtime_issue:
    primary: supri
    required_review:
      - doni

  high_risk:
    primary: siwa
    required_review:
      - asep
      - doni
      - senior_reviewer
    requires_human_review: true
```

---

# 4. Tool Selection Policy Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Agent Tool Scaffold | https://github.com/offlabel-scaffolds/agent-tool-scaffold | Tool registry, prompt manager, memory, validation, logging, metrics |
| 2 | Agent Registry | https://github.com/SocioProphet/agent-registry | Agent identity, sessions, memories, tool grants, revocation, runtime authority |
| 3 | OpenAI Agents TS Kit | https://github.com/maunappl8/openai-agents-ts-kit | Guardrails, typed tools, specialist handoff, session tracing |
| 4 | Order Product Agent SDK Assignment | https://github.com/huzaifaqazi/Order_Product_Agent_SDK_Assignment | Input guardrail, handoff, conditional tool function |
| 5 | Gemini Agent SDK Course | https://github.com/tertiarycourses/TGS-2024042961-gemini_agent_sdk_course | Guardrail, handoff, multi-tools, MCP, structured output examples |
| 6 | GraphQL Go Tools | https://github.com/wundergraph/graphql-go-tools | Router/gateway analogy, trusted operation, middleware, timeout, retry |

Use for Siwa:

```text
Decide which tool each agent may use.
Enforce allow-list and deny-list.
Prevent shell, commit, push, merge, delete, and .env access.
Treat tool calls as trusted operations.
Require policy check before dispatch.
```

Suggested local files:

```text
config/tools.yaml
config/agent_tool_grants.yaml
config/siwa_guardrails.yaml
```

Example:

```yaml
siwa_tools:
  allow:
    - kanban_create_task
    - kanban_assign_task
    - message_send
    - message_read_reply
    - agent_registry_lookup
    - tool_registry_lookup
    - workflow_state_read
    - workflow_state_write
    - human_escalation_request

  deny:
    - read_env
    - read_secret
    - arbitrary_shell
    - write_patch
    - apply_patch
    - git_commit
    - git_push
    - git_merge
    - delete_file
```

---

# 5. Multi-Agent Workflow Pattern Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Microsoft Conductor | https://github.com/microsoft/conductor | YAML workflow, parallel execution, human gate, validation, loop limits |
| 2 | Microsoft Agent Framework | https://github.com/microsoft/agent-framework | Multi-agent workflow, checkpointing, HITL, observability, declarative agents |
| 3 | Mentis | https://github.com/foreveryh/mentis | Planner, supervisor, handoff, evaluator, specialist workflow |
| 4 | Gas City | https://github.com/gastownhall/gascity | Work tracking, runtime providers, mail/message concept, health patrol |
| 5 | Inkeep Agents | https://github.com/inkeep/agents | Agent management, subagents, tools, credentials, traces, evaluation |
| 6 | Multi-Agent Orchestration Framework | https://github.com/yx-fan/multi-agent-orchestration-framework | Declarative workflow, nodes, agents, tools, provider abstraction |

Use for Siwa:

```text
Create workflow graph.
Use sequential workflow first.
Enable limited parallel routing only after stability.
Add human gate for high-risk actions.
Add checkpoint and resume.
Add validation before runtime.
```

Suggested local file:

```text
config/workflow.yaml
```

Example:

```yaml
workflow:
  name: selfdev_multi_agent
  mode: sequential_first
  stages:
    - load_manifest
    - validate_manifest
    - classify_risk
    - split_task
    - route_agent
    - dispatch_message
    - collect_artifact
    - evaluate_artifact
    - route_to_senior
    - stop_or_continue

  safety_limits:
    max_dispatch_rounds: 3
    max_revision_rounds: 2
    max_agent_wait_seconds: 300
```

---

# 6. Handoff Protocol Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Mentis | https://github.com/foreveryh/mentis | Handoff from supervisor to specialist agent |
| 2 | OpenAI Agents TS Kit | https://github.com/maunappl8/openai-agents-ts-kit | Triage, handoff, typed tools, guardrail |
| 3 | A2A Multi-Agent System Prototype | https://github.com/tubasarikaya/a2a-multi-agent-system-prototype | A2A message, context ID, queue, response synthesis |
| 4 | Gas City | https://github.com/gastownhall/gascity | Mail/message concept and work assignment |
| 5 | Inkeep Agents | https://github.com/inkeep/agents | Subagent triggering, tool use, execution state |

Use for Siwa:

```text
Write task_assignment messages.
Track message_id.
Track task_id and run_id.
Require required_outputs.
Require stop_conditions.
Collect artifact_ready replies.
Send review_request to Asep, Doni, or Senior Reviewer.
```

Suggested folder:

```text
data/agent_workspace/agents/{agent_id}/inbox/
data/agent_workspace/agents/{agent_id}/outbox/
```

Message template:

```json
{
  "message_id": "msg-0001",
  "from_agent": "siwa",
  "to_agent": "opung",
  "task_id": "task-043A",
  "message_type": "task_assignment",
  "priority": "medium",
  "objective": "Implement a small scoped patch.",
  "allowed_paths": [],
  "denied_paths": [],
  "required_outputs": [
    "plan",
    "draft_patch",
    "notes"
  ],
  "stop_conditions": [
    "scope_unclear",
    "denied_path_needed",
    "dependency_change_needed"
  ]
}
```

---

# 7. Agent Evaluation Rubric Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | LangGraph Agent | https://github.com/moiz-q/langgraph-agent | Evaluator node, conditional path, confidence loop |
| 2 | Mentis | https://github.com/foreveryh/mentis | Evaluator and supervisor loop |
| 3 | Microsoft Agent Framework | https://github.com/microsoft/agent-framework | Evaluation, checkpointing, observability |
| 4 | Inkeep Agents | https://github.com/inkeep/agents | Execution evaluation, state, traces, observability |
| 5 | Agent Tool Scaffold | https://github.com/offlabel-scaffolds/agent-tool-scaffold | Logging, metrics, error tracking, validation |

Use for Siwa:

```text
Evaluate whether artifact exists.
Evaluate whether artifact format is valid.
Evaluate whether required sections exist.
Evaluate whether decision field is valid.
Evaluate whether task is ready for Senior Reviewer.
Evaluate whether human gate is required.
```

Rubric:

| Criterion | PASS | FAIL |
|---|---|---|
| Artifact exists | File exists | Missing file |
| Artifact non-empty | Meaningful content | Empty or placeholder |
| Schema valid | Required sections present | Missing required sections |
| Scope safe | No denied path | Denied path touched |
| Evidence included | Evidence path or diff noted | Claim without evidence |
| Decision valid | Approved decision enum | Unknown decision |
| Review complete | Required reviewer artifact exists | Missing required review |

Suggested output:

```text
data/agent_workspace/orchestration/{task_id}.artifact_summary.md
```

---

# 8. Task Decomposition Prompt Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Microsoft Conductor | https://github.com/microsoft/conductor | Workflow YAML, task breakdown, conditional routing |
| 2 | Mentis | https://github.com/foreveryh/mentis | Planner and execution plan pattern |
| 3 | LangGraph Agent | https://github.com/moiz-q/langgraph-agent | Planner node and evaluator loop |
| 4 | AutoGen Multi-Agent Conversation | https://github.com/chanirban/autogen-multiagent-conversation | Persona separation concept |
| 5 | AutoGen Multiagent GroupChat | https://github.com/SandeshGitHub2077/autogen_multiagent_groupChat | Planner, Engineer, Scientist, Executor, Admin, Critic idea |

Use for Siwa:

```text
Break user task into smaller subtasks.
Avoid broad tasks.
Assign one agent per subtask.
Attach required output per subtask.
Attach required review per subtask.
Stop if task cannot be decomposed safely.
```

Prompt skeleton:

```text
You are Siwa Miwa, a local multi-agent orchestrator.

Given a task manifest:
1. Summarize the objective.
2. Identify task type.
3. Classify risk.
4. Split the work into small subtasks.
5. Assign each subtask to the correct agent.
6. Add required outputs.
7. Add required reviews.
8. Add stop conditions.
9. Add human gate if needed.

Do not write code.
Do not apply patches.
Do not run shell.
Return strict JSON.
```

---

# 9. Local AI Agent Orchestration Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Microsoft Conductor | https://github.com/microsoft/conductor | Local workflow CLI pattern, YAML, safety limits, HITL |
| 2 | LangGraph Agent | https://github.com/moiz-q/langgraph-agent | State graph, evaluator, conditional edges |
| 3 | Multi-Agent Orchestration Framework | https://github.com/yx-fan/multi-agent-orchestration-framework | FastAPI + YAML + provider + state manager pattern |
| 4 | Gas City | https://github.com/gastownhall/gascity | Local runtime provider, work routing, health patrol |
| 5 | Agent Tool Scaffold | https://github.com/offlabel-scaffolds/agent-tool-scaffold | Local agent scaffold, memory, tool registry |
| 6 | Awesome Agent Infrastructure | https://github.com/backblaze-labs/awesome-agent-infrastructure | Infrastructure reference catalog |

Use for Siwa:

```text
Design local-first runtime.
Use file-based state.
Use deterministic tools for execution.
Use LLM only for planning and routing explanation.
Use checkpoints.
Use logs and traces.
```

Suggested folders:

```text
data/agent_workspace/state/
data/agent_workspace/logs/
data/agent_workspace/traces/
data/agent_workspace/errors/
data/agent_workspace/performance/
```

---

# 10. UI, Dashboard, and Observability References

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Inkeep Agents | https://github.com/inkeep/agents | Agent management UI, subagent config, traces |
| 2 | Microsoft Agent Framework | https://github.com/microsoft/agent-framework | Observability, workflow state, HITL |
| 3 | Gas City | https://github.com/gastownhall/gascity | Work tracking and health patrol concept |
| 4 | Agent Tool Scaffold | https://github.com/offlabel-scaffolds/agent-tool-scaffold | Logging, metrics, error tracking |

Use for Siwa:

```text
Future Kanban dashboard.
Agent health status.
Workflow traces.
Task history.
Human gate review screen.
```

Initial implementation should stay file-based. UI comes later.

---

# 11. Suggested Chroma Collection

Collection:

```text
siwa_orchestration_knowledge
```

Suggested metadata:

```json
{
  "agent": "siwa",
  "source_type": "orchestration_reference",
  "allowed_use": "design_pattern_only",
  "runtime_dependency": false,
  "can_execute": false,
  "risk": "low",
  "topic": "agent_routing_policy"
}
```

For framework-heavy references:

```json
{
  "agent": "siwa",
  "source_type": "framework_reference",
  "allowed_use": "pattern_only_until_approved",
  "runtime_dependency": false,
  "requires_human_approval_for_dependency": true,
  "risk": "medium"
}
```

---

# 12. Suggested Local Files

```text
config/agents.yaml
config/tools.yaml
config/routing_rules.yaml
config/workflow.yaml
config/siwa_guardrails.yaml
schemas/manifest.schema.json
schemas/message.schema.json
schemas/kanban.schema.json
schemas/siwa_output.schema.json
data/agent_workspace/kanban/board.json
data/agent_workspace/agents/siwa/inbox/
data/agent_workspace/agents/siwa/outbox/
data/agent_workspace/orchestration/
data/agent_workspace/state/
data/agent_workspace/logs/
data/agent_workspace/errors/
```

---

# 13. Ranking Referensi untuk Siwa Miwa

| Priority | Reference | Value for Siwa | Status |
|---:|---|---|---|
| 1 | Microsoft Conductor | Workflow YAML, human gate, safety limits | Core pattern |
| 2 | Mentis | Planner, supervisor, handoff, evaluator | Core pattern |
| 3 | LangGraph Agent | State machine, evaluator, loop prevention | Core pattern |
| 4 | A2A Multi-Agent System Prototype | Hierarchical routing, context ID, queue | Core pattern |
| 5 | Multi-Agent Orchestration Framework | YAML workflow, AgentRouter, StateManager | Optional pattern |
| 6 | Microsoft Agent Framework | Checkpointing, HITL, observability | Long-term roadmap |
| 7 | Gas City | Work tracking, mail, runtime provider | Optional pattern |
| 8 | Inkeep Agents | Agent UI, subagents, traces | UI roadmap |
| 9 | Agent Registry | Tool grants, identity, revocation | Governance pattern |
| 10 | Agent Tool Scaffold | Tool registry, memory, logs, metrics | Scaffold pattern |
| 11 | OpenAI Agents TS Kit | Guardrail and handoff examples | Guardrail pattern |
| 12 | Gemini Agent SDK Course | Structured output and tool examples | Reference only |
| 13 | GraphQL Go Tools | Router/gateway analogy | Concept only |
| 14 | AutoGen examples | Persona and group chat idea | Not core engine |
| 15 | Awesome Agent Infrastructure | Reference catalog | Reading list |

---

# 14. Final Policy

Siwa Miwa uses these links as **orchestration knowledge**, not as automatic dependencies.

```text
Siwa plans.
Siwa routes.
Siwa dispatches.
Siwa evaluates artifact completeness.
Siwa escalates high-risk decisions.
Siwa does not execute source changes.
```

Hard boundary:

```text
No shell.
No patch.
No apply.
No commit.
No push.
No secret access.
No Safety Gate bypass.
No Senior Reviewer bypass.
```
