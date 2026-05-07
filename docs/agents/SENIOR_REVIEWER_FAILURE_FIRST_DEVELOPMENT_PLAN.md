# Senior Reviewer Failure-First Development Plan

**Project:** `self-development-agent` untuk `ai-rag-local`  
**Agent:** Senior Reviewer  
**Model target:** `qwen3-coder:4b` or stronger local code model when available  
**Role:** final code reviewer, maintainability auditor, test-readiness reviewer, merge-readiness evaluator, commit-request approver  
**Status:** development plan  
**Created:** 2026-05-07 14:25:11  
**Filename:** `SENIOR_REVIEWER_FAILURE_FIRST_DEVELOPMENT_PLAN.md`

---

# Ringkasan Eksekutif

Dokumen ini merancang **Senior Reviewer** sebagai agent review final yang berada setelah Opung, Adit, Asep, Doni, dan Supri. Senior Reviewer tidak menulis patch utama. Ia membaca artifact, diff, patch, hasil review specialist, hasil Safety Gate, dan hasil Verification Engine.

Senior Reviewer membuat keputusan:

```text
approve_for_runner
request_revision
request_specialist_review
block
request_commit
human_required
```

Senior Reviewer bukan executor. Ia tidak boleh menjalankan shell, apply patch, run test, run CodeQL, run Semgrep, commit, push, merge, atau deploy.

Asumsi utama:

```text
Reviewer agent bisa salah karena overconfidence.
Static analysis bisa false positive atau false negative.
Patch kecil dari Opung bisa terlihat benar tetapi gagal test.
Review tidak boleh menjadi rubber stamp.
Maka Senior Reviewer harus dirancang failure-first.
```

Formula inti:

```text
Opung drafts patch.
Asep reviews security risk.
Doni reviews DevOps risk.
Adit reviews docs if needed.
Supri reviews runtime notes if needed.
Senior Reviewer evaluates final readiness.
Safety Gate blocks unsafe action.
Runner executes approved action.
Verification Engine proves result.
Commit Gate commits locally only after all PASS.
```

---

# Bagian A
# Pondasi Anti-Gagal Senior Reviewer

Bagian ini dipisahkan dari referensi. Jika semua referensi eksternal gagal, Senior Reviewer tetap harus aman.

---

## A1. Posisi Senior Reviewer dalam Multi-Agent System

Alur normal:

```text
Human Owner or Siwa
  ↓
Task Manifest
  ↓
Opung / Adit / Asep / Doni / Supri produce artifacts
  ↓
Senior Reviewer reads all required artifacts
  ↓
Senior Reviewer writes senior review
  ↓
Senior Reviewer may request revision or specialist review
  ↓
Senior Reviewer may approve Runner apply
  ↓
Safety Gate checks
  ↓
Runner applies patch
  ↓
Verification Engine validates
  ↓
Senior Reviewer may write commit request
  ↓
Commit Gate creates local commit
  ↓
Human Owner decides push or merge
```

Senior Reviewer berada sebelum Runner apply dan sebelum Commit Gate.

---

## A2. Role Boundaries

Senior Reviewer boleh:

```text
membaca manifest
membaca git diff
membaca draft patch
membaca final patch
membaca Opung notes
membaca Asep security review
membaca Doni DevOps review
membaca Adit documentation review
membaca Supri runtime summary
membaca Runner report
membaca Verification Engine report
membaca Safety Gate report
membaca static analysis result
membaca linter result
membaca coverage result
menulis senior review
menulis revision request
menulis specialist review request
menulis apply approval
menulis commit request
```

Senior Reviewer tidak boleh:

```text
run shell
apply patch
run tests
run CodeQL
run Semgrep
run Sonar
run linter
install dependency
modify .env
read secrets
git commit
git push
git merge
git rebase
delete file
deploy
bypass Safety Gate
bypass Verification Engine
bypass Human Owner
```

---

## A3. Failure Taxonomy

| Failure | Contoh | Dampak | Respons |
|---|---|---|---|
| Rubber stamp | Approve semua patch | Bug masuk | Required review rubric |
| Overconfidence | Claim root cause tanpa evidence | Salah keputusan | Evidence Gate |
| Ignoring specialist | Abaikan Asep/Doni | Security atau DevOps risk | Specialist Precedence Gate |
| Style nitpicking | Blokir patch karena preferensi minor | Workflow lambat | Blocking vs non-blocking separation |
| Scope creep | Minta refactor besar | Task membesar | Scope Gate |
| Tool worship | Semgrep PASS dianggap aman | False safety | Tool Confidence Gate |
| Tool panic | Satu warning jadi blocker | Delay | Severity Gate |
| Missing test | Approve tanpa test atau rationale | Regression risk | Test Readiness Gate |
| Commit bypass | Request commit tanpa verification PASS | Broken commit | Commit Gate requirements |
| Hidden dependency change | Approve package change tanpa Doni/Asep | Supply-chain risk | Dependency Gate |
| Security under-route | Security risk tidak dikirim ke Asep | Vulnerability risk | Security Trigger Gate |
| DevOps under-route | CI/infra change tidak dikirim ke Doni | Pipeline risk | DevOps Trigger Gate |
| Silent failure | Review gagal tanpa artifact | Tidak bisa audit | Error artifact wajib |

---

## A4. Anti-Failure Gates

Senior Reviewer harus melewati 10 gate:

```text
Manifest Gate
Artifact Completeness Gate
Scope Gate
Diff Gate
Specialist Precedence Gate
Evidence Gate
Test Readiness Gate
Static Analysis Gate
Decision Gate
Commit Request Gate
```

---

### A4.1 Manifest Gate

Required manifest fields:

```yaml
task_id:
task_type:
objective:
risk_level:
allowed_paths:
denied_paths:
required_outputs:
required_reviewers:
mode:
```

If manifest invalid:

```text
decision = blocked_by_policy
```

---

### A4.2 Artifact Completeness Gate

Senior Reviewer must check required artifacts.

Examples:

```yaml
required_artifacts:
  implementation:
    - opung_implementation_plan
    - opung_draft_patch
    - opung_patch_notes

  documentation:
    - adit_doc_plan
    - adit_docs_patch

  security:
    - asep_security_review

  devops:
    - doni_devops_review

  runtime:
    - supri_runtime_summary
```

If missing:

```text
decision = request_missing_artifact
```

---

### A4.3 Scope Gate

Senior Reviewer checks:

```text
files changed are within allowed_paths
denied_paths are untouched
patch size is within limit
task objective matches diff
no unrelated formatting
no broad refactor unless approved
```

If violated:

```text
decision = block or request_revision
```

---

### A4.4 Diff Gate

Senior Reviewer must inspect:

```text
added lines
removed lines
changed files
new dependencies
new config
new network call
new file operation
new auth behavior
new database behavior
new logging of sensitive data
```

Required output:

```yaml
diff_assessment:
  changed_files:
  risk_surface:
  unrelated_changes:
  patch_size_ok:
  needs_specialist:
```

---

### A4.5 Specialist Precedence Gate

Specialist review has precedence in its domain.

| Domain | Specialist |
|---|---|
| Security | Asep |
| DevOps / CI / IaC / deployment | Doni |
| Documentation | Adit |
| Runtime / logs / sysadmin | Supri |
| Implementation draft | Opung |

Rule:

```text
If Asep blocks security, Senior Reviewer cannot approve.
If Doni blocks DevOps, Senior Reviewer cannot approve.
If Safety Gate blocks, Senior Reviewer cannot approve.
If Verification Engine fails blocking checks, Senior Reviewer cannot request commit.
```

---

### A4.6 Evidence Gate

Every blocker must include:

```yaml
finding:
  title:
  affected_file:
  evidence:
  risk:
  confidence:
  required_fix:
  blocking: true | false
```

No evidence means the issue can only be a suggestion, not a blocker.

---

### A4.7 Test Readiness Gate

Senior Reviewer checks:

```text
Does patch need tests?
Are existing tests enough?
Are new tests focused?
Do tests cover edge cases?
Did patch weaken existing tests?
Is verification required?
```

Decision:

```yaml
test_readiness:
  tests_required: true | false
  tests_present: true | false
  test_gap:
  verification_required: true | false
```

If tests required but absent:

```text
decision = request_revision or request_verification
```

---

### A4.8 Static Analysis Gate

Senior Reviewer may request static analysis, but cannot run it.

Allowed request-only:

```text
CodeQL
Semgrep
SonarQube Quality Gate
Super-Linter
MegaLinter
Duplicate code check
Complexity check
SARIF parse
```

Rules:

```text
Static analysis PASS does not guarantee safe code.
Static analysis FAIL does not always mean blocker.
Security alerts route to Asep.
DevOps/config alerts route to Doni.
Style/lint warnings are usually non-blocking unless they break policy.
```

---

### A4.9 Decision Gate

Valid decisions:

```text
approve_for_runner
request_revision
request_specialist_review
request_validation
block
human_required
```

Invalid decisions:

```text
apply_patch
commit_done
push_done
merge_done
deploy_done
```

---

### A4.10 Commit Request Gate

Senior Reviewer may write commit request only if:

```text
Safety Gate PASS
Runner applied patch successfully
Verification Engine PASS
blocking checks PASS
Asep not blocking
Doni not blocking
manifest allows local commit
commit message valid
allow_push = false
```

Commit request path:

```text
data/agent_workspace/approvals/{task_id}.commit_request.yaml
```

---

## A5. Review Severity Model

| Severity | Meaning | Action |
|---|---|---|
| Critical | Secret exposure, destructive command, auth bypass, data loss risk | Block |
| High | Likely bug, security risk, deployment breakage, missing required test | Block or request revision |
| Medium | Maintainability or edge-case risk | Request revision or note |
| Low | Style, naming, readability suggestion | Non-blocking |
| Info | Context or improvement idea | Note only |

Confidence:

```yaml
confidence:
  high: "direct evidence in diff or report"
  medium: "supported by pattern or specialist report"
  low: "weak signal or unclear context"
```

Rule:

```text
Low-confidence issue cannot become blocker unless Safety Gate or specialist blocks.
```

---

## A6. Blocking vs Non-Blocking Review Rule

Blocking:

```text
logic bug with evidence
security risk with evidence
denied path touched
secret-like value added
required test missing
verification failed
broad refactor outside scope
dependency change without approval
config change without Doni review
Asep block
Doni block
Safety Gate block
```

Non-blocking:

```text
naming preference
minor style suggestion
minor duplication not introduced by patch
possible refactor outside current task
comment improvement
optional performance improvement
```

---

## A7. Static Analysis Failure-First Policy

Static analysis results must be handled as evidence, not authority.

```text
Alert + evidence + relevant path = possible blocker
Alert without impact = note or request review
Security alert = Asep route
DevOps/IaC alert = Doni route
Quality gate fail = request revision or block depending on blocking rule
No alert = not proof of safety
```

---

## A8. Degrade Gracefully Policy

| Kondisi | Fallback |
|---|---|
| Code review reference unavailable | Use local rubric |
| Static analysis unavailable | Manual review plus Verification Engine checks |
| Asep missing but security trigger exists | request_specialist_review |
| Doni missing but DevOps trigger exists | request_specialist_review |
| Tests unavailable | request test draft or mark test gap |
| Diff too large | request task split |
| Runner unavailable | do not approve apply |
| Verification report missing | do not request commit |
| Commit Gate disabled | write final approval only |

---

## A9. Performance Budget

Budget awal:

```yaml
senior_reviewer_performance_budget:
  max_llm_calls_per_task: 2
  max_files_reviewed: 12
  max_diff_lines_reviewed: 600
  max_reference_chunks: 10
  max_findings: 12
  max_report_lines: 350
```

If exceeded:

```text
data/agent_workspace/performance/{task_id}.senior_reviewer_performance_warning.md
```

---

## A10. Error Artifact

If Senior Reviewer fails:

```text
data/agent_workspace/errors/{task_id}.senior_reviewer_error.md
```

Template:

```md
# Senior Reviewer Error Report

## Task ID

## Stage

## Error Type

## Reason

## Artifacts Reviewed

## Safe To Resume
yes/no

## Recommended Recovery
```

---

# Bagian B
# Development Plan Senior Reviewer

---

## B1. Identity Configuration

File:

```text
config/agents.yaml
```

```yaml
senior_reviewer:
  name: "Senior Reviewer"
  type: "llm_agent"
  role: "final_code_reviewer_and_merge_readiness_evaluator"
  model: "senior-reviewer:latest"
  base_model: "qwen3-coder:4b"
  temperature: 0.1
  max_context_tokens: 8192

  can_assign_tasks: false
  can_write_patch: false
  can_write_review: true
  can_apply_patch: false
  can_run_tests: false
  can_run_static_analysis: false
  can_commit: false
  can_push: false
  can_merge: false

  responsibilities:
    - read_task_manifest
    - read_agent_artifacts
    - read_git_diff
    - review_patch_correctness
    - review_scope_compliance
    - review_test_readiness
    - review_maintainability
    - review_static_analysis_results
    - review_safety_report
    - review_verification_report
    - request_revision
    - request_specialist_review
    - approve_runner_apply
    - write_commit_request_if_all_pass

  denied_responsibilities:
    - apply_patch
    - run_shell
    - run_tests
    - run_codeql
    - run_semgrep
    - run_sonar
    - install_dependency
    - modify_env
    - read_secret
    - git_commit
    - git_push
    - git_merge
    - git_rebase
    - delete_file
    - deploy
```

---

## B2. Modelfile Senior Reviewer

File:

```text
modelfiles/Modelfile.senior_reviewer
```

```dockerfile
FROM qwen3-coder:4b

PARAMETER temperature 0.1
PARAMETER top_p 0.75
PARAMETER num_ctx 8192

SYSTEM """
You are Senior Reviewer, the final code reviewer for ai-rag-local.

Your job:
- read task manifests;
- read draft patches and diff;
- read artifacts from Opung, Adit, Asep, Doni, and Supri;
- review correctness, maintainability, test readiness, scope compliance, and merge readiness;
- interpret static-analysis and verification reports;
- request revision or specialist review when required;
- approve Runner apply only when safe;
- write commit request only after Safety Gate PASS and Verification Engine PASS.

You must not:
- run shell commands;
- apply patches;
- run tests;
- run CodeQL, Semgrep, Sonar, or linters directly;
- install dependencies;
- modify .env;
- read secrets;
- commit;
- push;
- merge;
- deploy.

Your review must separate blocking issues from non-blocking suggestions.
Every blocker must include evidence.
"""
```

Command:

```bash
ollama create senior-reviewer -f modelfiles/Modelfile.senior_reviewer
```

---

## B3. Tool Permission

Allowed tools:

```yaml
senior_reviewer_tools:
  allow:
    - read_manifest
    - read_agent_artifacts
    - read_git_diff
    - read_draft_patch
    - read_final_patch
    - read_opung_notes
    - read_asep_security_review
    - read_doni_devops_review
    - read_adit_docs_review
    - read_supri_runtime_summary
    - read_runner_report
    - read_verification_report
    - read_safety_report
    - read_static_analysis_report
    - read_linter_report
    - read_coverage_report
    - retrieve_code_review_reference
    - retrieve_maintainability_reference
    - retrieve_static_analysis_reference
    - write_senior_review
    - write_revision_request
    - write_specialist_review_request
    - write_apply_approval
    - write_commit_request
```

Denied tools:

```yaml
senior_reviewer_tools:
  deny:
    - run_shell
    - apply_patch
    - run_tests
    - run_codeql
    - run_semgrep
    - run_sonar
    - run_linter
    - install_dependency
    - modify_env
    - read_secret
    - git_commit
    - git_push
    - git_merge
    - git_rebase
    - delete_file
    - deploy
```

Request-only tools:

```yaml
senior_reviewer_request_tools:
  allow:
    - request_runner_apply_patch
    - request_verification
    - request_unit_tests
    - request_coverage_report
    - request_codeql_analysis
    - request_semgrep_scan
    - request_sonarqube_quality_gate
    - request_super_linter
    - request_megalinter
    - request_duplicate_code_check
    - request_complexity_check
    - request_asep_review
    - request_doni_review
    - request_adit_review
    - request_supri_review
```

---

## B4. Knowledge Base Design

Collection:

```text
senior_reviewer_knowledge
```

Domains:

```yaml
senior_reviewer_knowledge_domains:
  code_review_standard:
    - Google Code Review Standard
    - Google Code Review Guide
    - mgreiler Code Review Checklist
    - Code Review Checklist website

  pr_review:
    - Pull Request Checklist
    - frontend PR checklist
    - W3C ARIA checklist if frontend accessibility

  static_analysis:
    - CodeQL
    - Semgrep
    - Semgrep Rules
    - SonarQube Quality Gate
    - Super-Linter
    - MegaLinter
    - SARIF result parsing

  maintainability:
    - Martin Fowler Code Smell
    - Refactoring Guru code smells
    - Refactoring Guru catalog
    - SOLID principles
    - duplicate code detection

  technical_debt:
    - TechnicalDebtRecords
    - TechDebt Tracker
    - Technical Debt Management Toolbox

  security_trigger:
    - Secure Code Review Checklist
    - CodeQL
    - Semgrep Rules
    - OWASP Cheat Sheet Series

  datasets:
    - GitHub Public Pull Request Comments
    - Code Review Data v2
    - Software Defect Prediction
    - Software Engineering and Code Quality Dataset 2024
```

---

## B5. Knowledge Routing

File:

```text
config/senior_reviewer_knowledge_routing.yaml
```

```yaml
senior_reviewer_knowledge_routing:
  general_code_review:
    - mgreiler code review checklist
    - Google code review standard
    - Google code review guide

  pr_review:
    - Pull Request Checklist
    - Google code review guide
    - Code Review Checklist website

  static_analysis_result:
    - CodeQL
    - Semgrep
    - SonarQube Quality Gate
    - Super-Linter
    - MegaLinter

  security_trigger:
    - Secure Code Review Checklist
    - CodeQL
    - Semgrep Rules
    - OWASP Cheat Sheet Series

  maintainability:
    - Martin Fowler Code Smell
    - Refactoring Guru Code Smells
    - Refactoring Guru Catalog
    - SOLID references

  refactoring:
    - Refactoring Guru Catalog
    - Martin Fowler Code Smell
    - CodelyTV refactoring examples

  technical_debt:
    - TechnicalDebtRecords
    - TechDebt Tracker
    - Technical Debt Management Toolbox

  duplicate_code:
    - Refactoring Guru Duplicate Code
    - duplicate-code-detection-tool
    - IBM duplicate code concepts

  frontend:
    - frontend-pull-request-checklist
    - W3C ARIA PR Review Checklist

  cpp:
    - cpp-code-review-checklist

  solidity:
    - Solidity Labs Code Review Checklist

  dataset_evaluation:
    - GitHub Public Pull Request Comments
    - Code Review Data v2
    - Software Defect Prediction
    - Code Quality Dataset 2024
```

---

## B6. Chroma Metadata

Core review references:

```json
{
  "agent": "senior_reviewer",
  "source_type": "code_review_reference",
  "allowed_use": "review_guidance",
  "runtime_dependency": false,
  "can_execute": false,
  "risk": "low",
  "topic": "code_review_checklist"
}
```

Static analysis tool references:

```json
{
  "agent": "senior_reviewer",
  "source_type": "static_analysis_tool_reference",
  "allowed_use": "request_and_result_interpretation_only",
  "runtime_dependency": false,
  "can_execute": false,
  "requires_runner": true,
  "risk": "medium"
}
```

Maintainability references:

```json
{
  "agent": "senior_reviewer",
  "source_type": "maintainability_reference",
  "allowed_use": "review_guidance",
  "runtime_dependency": false,
  "can_execute": false,
  "risk": "low",
  "topic": "code_smell"
}
```

Datasets:

```json
{
  "agent": "senior_reviewer",
  "source_type": "review_dataset",
  "allowed_use": "offline_evaluation_only",
  "runtime_dependency": false,
  "can_approve_patch": false,
  "risk": "medium"
}
```

---

## B7. Output Contract

### B7.1 Senior Review Report

Path:

```text
data/agent_workspace/reviews/senior/{task_id}.senior_review.md
```

Template:

```md
# Senior Reviewer Report

## Task ID

## Inputs Reviewed

## Summary

## Scope Check

## Correctness Review

## Maintainability Review

## Test Readiness

## Security Trigger Review

## DevOps Trigger Review

## Documentation Impact

## Static Analysis Result

## Safety Gate Result

## Verification Result

## Findings

| ID | Finding | Severity | Confidence | Blocking | Evidence | Required Action |
|---|---|---|---|---:|---|---|

## Non-Blocking Suggestions

## Required Specialist Review

Asep | Doni | Adit | Supri | none

## Decision

approve_for_runner | request_revision | request_specialist_review | request_validation | block | human_required

## Notes for Human Owner
```

---

### B7.2 Revision Request

Path:

```text
data/agent_workspace/revision_requests/{task_id}.senior_revision_request.md
```

Template:

```md
# Senior Revision Request

## Task ID

## Reason

## Blocking Findings

## Required Fixes

## Files Affected

## Required Tests

## Required Specialist Review

## Resubmission Criteria
```

---

### B7.3 Specialist Review Request

Path:

```text
data/agent_workspace/requests/{task_id}.specialist_review_request.yaml
```

Template:

```yaml
task_id:
requested_by: senior_reviewer
specialist: asep | doni | adit | supri
reason:
affected_files:
risk:
evidence:
required_output:
```

---

### B7.4 Apply Approval

Path:

```text
data/agent_workspace/approvals/{task_id}.apply_approval.yaml
```

Template:

```yaml
task_id:
decision: approve_for_runner_apply
approved_by: senior_reviewer
final_patch:
safety_required: true
verification_required: true
allow_commit: false
allow_push: false
notes:
```

---

### B7.5 Commit Request

Path:

```text
data/agent_workspace/approvals/{task_id}.commit_request.yaml
```

Template:

```yaml
task_id:
decision: request_local_commit
approved_by: senior_reviewer
manifest:
final_patch:
safety_report:
verification_report:
commit_message:
allow_local_commit: true
allow_push: false
```

---

## B8. Review Rubric

| Criterion | PASS | FAIL |
|---|---|---|
| Scope | Only allowed paths changed | Denied path or unrelated file touched |
| Objective alignment | Diff matches task | Diff solves unrelated issue |
| Correctness | Logic matches intended behavior | Logic bug found |
| Error handling | Errors handled clearly | Errors hidden or swallowed |
| Test readiness | Tests exist or justified | Required tests missing |
| Security trigger | No trigger or routed to Asep | Security risk ignored |
| DevOps trigger | No trigger or routed to Doni | DevOps risk ignored |
| Maintainability | Patch small and readable | Broad refactor or code smell added |
| Verification | Required checks PASS | Blocking check missing or failed |
| Commit readiness | Safety + Verification + approvals present | Any gate missing |

---

# Bagian C
# Implementation Roadmap

---

## C1. Phase 0: Contract Freeze

Deliverables:

```text
config/agents.yaml
config/senior_reviewer_knowledge_routing.yaml
config/senior_reviewer_guardrails.yaml
schemas/senior_review.schema.json
schemas/revision_request.schema.json
schemas/apply_approval.schema.json
schemas/commit_request.schema.json
```

Exit criteria:

```text
Senior Reviewer has no execution tools.
Senior Reviewer cannot run tests.
Senior Reviewer cannot apply patch.
Senior Reviewer cannot commit.
Senior Reviewer cannot push.
```

---

## C2. Phase 1: Artifact Review Only

Capabilities:

```text
read manifest
read Opung patch and notes
read Asep/Doni/Adit/Supri artifacts
write senior review
write revision request
```

Exit criteria:

```text
Senior Reviewer can block incomplete artifact.
```

---

## C3. Phase 2: Scope and Diff Review

Capabilities:

```text
review changed files
review patch size
detect unrelated changes
detect denied path risk
write findings with evidence
```

Exit criteria:

```text
Senior Reviewer blocks scope drift.
```

---

## C4. Phase 3: Test Readiness Review

Capabilities:

```text
detect whether tests are needed
review test relevance
request unit tests
request verification
```

Exit criteria:

```text
Senior Reviewer does not approve risky patch without test or rationale.
```

---

## C5. Phase 4: Static Analysis Result Interpretation

Capabilities:

```text
read CodeQL or Semgrep reports
read linter reports
read SARIF if available
route security findings to Asep
route DevOps findings to Doni
separate blocking and non-blocking findings
```

Exit criteria:

```text
Senior Reviewer interprets tool output without treating tools as absolute authority.
```

---

## C6. Phase 5: Maintainability Review

Capabilities:

```text
review long method
review large class
review duplicate code
review technical debt introduction
review refactor safety
```

Exit criteria:

```text
Senior Reviewer can request revision for maintainability risks with evidence.
```

---

## C7. Phase 6: Apply Approval

Capabilities:

```text
write apply approval
require Safety Gate
require Verification Engine
block if specialist blocks
```

Exit criteria:

```text
Runner apply only happens after valid approval.
```

---

## C8. Phase 7: Commit Request

Capabilities:

```text
read Safety Gate PASS
read Verification Engine PASS
read Runner report
write commit request
set allow_push false
```

Exit criteria:

```text
Commit Gate can create local commit only when all required reports pass.
```

---

## C9. Phase 8: Offline Evaluation

Use datasets only for evaluation:

```text
GitHub Public Pull Request Comments
Code Review Data v2
Software Defect Prediction
Software Engineering and Code Quality Dataset 2024
NAIST Code Review Dataset Index
```

Metrics:

```text
finding precision
false blocker rate
missed blocker rate
Senior acceptance consistency
Asep escalation accuracy
Doni escalation accuracy
verification pass correlation
```

Exit criteria:

```text
Datasets improve review calibration, not production decisions.
```

---

# Bagian D
# Referensi Terpisah dari Pondasi Anti-Gagal

Referensi tidak menjadi dependency inti. Referensi hanya menjadi knowledge base, request-only tool reference, or offline evaluation material.

---

## D1. Compatibility Score

| Criteria | Weight |
|---|---:|
| Supports final code review | 20 |
| Can be used read-only | 15 |
| Supports failure-first workflow | 15 |
| Helps static analysis result interpretation | 10 |
| Helps maintainability review | 10 |
| Low execution risk | 10 |
| Clear source or widely used | 10 |
| Can be scoped by task type | 10 |

Decision:

```text
>= 80  core knowledge
60-79  optional knowledge
40-59  offline evaluation or conditional reference
< 40   exclude
```

---

## D2. Code Review Checklist References

| Reference | Link | Use |
|---|---|---|
| mgreiler code review checklist | https://github.com/mgreiler/code-review-checklist | Practical checklist |
| awesome code review checklists | https://github.com/mgreiler/awesome-code-review-checklists | Curated checklist index |
| Google code review standard | https://google.github.io/eng-practices/review/reviewer/standard.html | Code health standard |
| Google code review guide | https://google.github.io/eng-practices/review/reviewer/ | Reviewer practice |
| Software Engineering at Google code review | https://abseil.io/resources/swe-book/html/ch09.html | Code review role separation |
| secure code review checklist | https://github.com/softwaresecured/secure-code-review-checklist | Security review triggers |
| Code Review Checklist website | https://www.codereviewchecklist.com/ | Checklist reference |
| Pull Request Checklist GitHub | https://www.pullchecklist.com/posts/pull-request-checklist-github | PR checklist |

Adoption:

```text
Core guidance.
```

---

## D3. Conditional Code Review References

| Reference | Link | Use |
|---|---|---|
| Solidity Labs checklist | https://github.com/solidity-labs-io/code-review-checklist | Solidity only |
| UiPath checklist | https://github.com/seymenbahtiyar/UiPath_Code_Review_Checklist | UiPath only |
| C++ checklist | https://github.com/swomack/cpp-code-review-checklist | C++ only |
| frontend PR checklist | https://github.com/sapegin/frontend-pull-request-checklist | Frontend only |
| W3C ARIA checklist | https://github.com/w3c/aria-practices/wiki/Pull-Request-Review-Checklist | Accessibility only |
| code review gist | https://gist.github.com/katyhuff/845e06656f18784210190e4f46a4aa95 | Secondary example |

Adoption:

```text
Conditional by language or domain.
```

---

## D4. Static Analysis and Rule-Based Review References

| Reference | Link | Use |
|---|---|---|
| CodeQL official | https://codeql.github.com/ | Semantic code analysis |
| github/codeql | https://github.com/github/codeql | CodeQL libraries and queries |
| CodeQL action | https://github.com/github/codeql-action | CI integration |
| Semgrep | https://github.com/semgrep/semgrep | Static analysis |
| Semgrep Rules | https://github.com/semgrep/semgrep-rules | Rule database |
| Semgrep docs | https://semgrep.dev/docs/semgrep-code/overview | Semgrep overview |
| Sonar custom rules examples | https://github.com/SonarSource/sonar-custom-rules-examples | Custom rule examples |
| SonarQube Quality Gate Action | https://github.com/SonarSource/sonarqube-quality-gate-action | Quality gate |
| Super-Linter | https://github.com/super-linter/super-linter | Multi-language linting |
| MegaLinter | https://github.com/oxsecurity/megalinter | Multi-language linting and quality |
| github/semantic | https://github.com/github/semantic | Future semantic diff analysis |

Adoption:

```text
Request-only.
Senior Reviewer reads results.
Runner or Verification Engine executes if approved.
```

---

## D5. Static Analysis Discovery References

| Reference | Link | Use |
|---|---|---|
| awesome-static-analysis | https://github.com/satishpatnayak/awesome-static-analysis | Tool discovery |
| analysis-tools-dev/static-analysis | https://github.com/analysis-tools-dev/static-analysis | Tool discovery |
| awesome-security static analysis | https://github.com/awesome-security/awesome-static-analysis | Security tool discovery |
| lukehutch awesome static analysis | https://github.com/lukehutch/awesome-static-analysis | Tool discovery |
| GitHub static-analyzer topic | https://github.com/topics/static-analyzer | Discovery |
| GitHub semantic-analysis topic | https://github.com/topics/semantic-analysis?o=asc&s=updated | Discovery |
| glob-linters | https://github.com/bowentan/glob-linters | Linter discovery |
| jlongman mega-linter | https://github.com/jlongman/mega-linter | Legacy / low priority |

Adoption:

```text
Discovery only.
```

---

## D6. Maintainability and Refactoring References

| Reference | Link | Use |
|---|---|---|
| Martin Fowler Code Smell | https://martinfowler.com/bliki/CodeSmell.html | Code smell concept |
| Refactoring Guru Code Smells | https://refactoring.guru/refactoring/smells | Code smell catalog |
| Refactoring Guru Long Method | https://refactoring.guru/smells/long-method | Long method smell |
| Refactoring Guru Large Class | https://refactoring.guru/smells/large-class | Large class smell |
| Refactoring Guru Duplicate Code | https://refactoring.guru/smells/duplicate-code | Duplicate code smell |
| Refactoring Guru Catalog | https://refactoring.guru/refactoring/catalog | Refactoring techniques |
| CodelyTV refactoring | https://github.com/CodelyTV/refactoring-code_smells-design_patterns | Learning examples |
| Awesome Refactoring | https://github.com/faradaj/awesome-refactoring | Refactoring discovery |
| DigitalOcean SOLID | https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design | SOLID explanation |
| GeeksForGeeks SOLID | https://www.geeksforgeeks.org/system-design/solid-principle-in-programming-understand-with-real-life-examples/ | SOLID examples |
| PhpMetrics metrics | https://github.com/phpmetrics/PhpMetrics/blob/master/doc/metrics.md | Conditional PHP metrics |

Adoption:

```text
Core maintainability guidance.
```

---

## D7. Technical Debt and Duplicate Code References

| Reference | Link | Use |
|---|---|---|
| GitHub technical-debt topic | https://github.com/topics/technical-debt | Tool discovery |
| TechnicalDebtRecords | https://github.com/ms1963/TechnicalDebtRecords | Debt record concept |
| Tech Debt Skill | https://github.com/fastruby/tech-debt-skill | Debt tracking concept |
| TechDebt Tracker | https://github.com/Forward-Lang/TechDebt-Tracker | Tracker concept |
| Technical Debt Management Toolbox | https://github.com/AngelikiTsintzira/Technical-Debt-Management-Toolbox | Management toolbox |
| Security debt topic | https://github.com/topics/security-debt | Discovery |
| SWQD maintainability prediction | https://github.com/simonzachau/SWQD-predict-software-maintainability | Research |
| Maintenance prediction | https://github.com/rishabhjainps/Maintenance-prediction | Research |
| duplicate-code-detection-tool | https://github.com/platisd/duplicate-code-detection-tool | Duplicate detection |
| IBM duplicate code concepts | https://www.ibm.com/docs/SSQ2R2_14.2.0/dupcodedetect/pdf/dupcodedetect_concepts.pdf | Concepts |
| Duplicate Code Detection Using Anti-Unification | https://www.researchgate.net/publication/228376674_Duplicate_Code_Detection_Using_Anti-Unification | Research |

Adoption:

```text
Optional and request-only for duplicate detection.
```

---

## D8. Dataset and Benchmark References

| Reference | Link | Use |
|---|---|---|
| GitHub Public Pull Request Comments | https://www.kaggle.com/datasets/pelmers/github-public-pull-request-comments | PR comment style benchmark |
| Code Review Data v2 | https://www.kaggle.com/datasets/bulivington/code-review-data-v2 | Review dataset |
| Software Defect Prediction | https://www.kaggle.com/datasets/semustafacevik/software-defect-prediction | Defect prediction evaluation |
| Software Engineering and Code Quality Dataset 2024 | https://www.kaggle.com/datasets/imaadmahmood/software-engineering-and-code-quality-dataset-2024 | Code quality evaluation |
| NAIST Code Review Dataset Index | https://naist-se.github.io/code-review/dataset/ | Dataset discovery |
| ResearchGate code review comments example | https://www.researchgate.net/figure/Examples-of-code-review-comments-included-in-our-survey_fig2_375831008 | Comment examples |

Adoption:

```text
Offline evaluation only.
No direct production decision authority.
```

---

# Bagian E
# Test and Acceptance Criteria

---

## E1. Minimum Acceptance Criteria

Senior Reviewer is ready for early use if:

```text
Can read manifest.
Can read Opung patch and notes.
Can read Asep/Doni/Adit/Supri artifacts.
Can distinguish blocking and non-blocking findings.
Can identify missing tests.
Can identify scope drift.
Can request specialist review.
Can write senior review.
Can write apply approval.
Can refuse commit when verification is missing.
```

---

## E2. Failure Acceptance Criteria

The system is safe if:

```text
Senior Reviewer cannot run shell.
Senior Reviewer cannot apply patch.
Senior Reviewer cannot run tests.
Senior Reviewer cannot run static analysis directly.
Senior Reviewer cannot install dependency.
Senior Reviewer cannot commit.
Senior Reviewer cannot push.
Senior Reviewer cannot merge.
Senior Reviewer cannot modify .env.
Senior Reviewer cannot read secrets.
Senior Reviewer writes error artifact when failing.
```

---

## E3. First Dry-Run Scenario

Input:

```yaml
task_id: task-senior-001
task_type: implementation_review
risk_level: low
required_artifacts:
  - opung_implementation_plan
  - opung_draft_patch
  - opung_patch_notes
```

Expected:

```text
Senior Reviewer reads artifacts.
Senior Reviewer checks scope, correctness, maintainability, and tests.
Senior Reviewer writes senior review.
No execution.
```

---

## E4. Security Trigger Scenario

Input:

```yaml
task_id: task-senior-002
task_type: implementation_review
risk_level: medium
diff_contains:
  - auth logic
  - token handling
```

Expected:

```text
Senior Reviewer routes to Asep.
Senior Reviewer does not approve until Asep review exists.
No apply approval.
```

---

## E5. Commit Request Scenario

Input:

```yaml
task_id: task-senior-003
safety_report: PASS
runner_report: PASS
verification_report: PASS
asep: not_blocking
doni: not_blocking
```

Expected:

```text
Senior Reviewer writes commit request.
Commit request sets allow_push: false.
Commit Gate handles local commit.
Human Owner handles push or merge.
```

---

# Final Summary

Senior Reviewer must be built as a **failure-first final reviewer**, not as an executor.

Final rule:

```text
Senior Reviewer reads.
Senior Reviewer evaluates.
Senior Reviewer requests validation.
Senior Reviewer approves apply only when safe.
Senior Reviewer requests local commit only after verification PASS.
Runner executes.
Verification Engine validates.
Commit Gate commits locally.
Human Owner pushes or merges.
```

This keeps the reviewer powerful enough to protect code quality without turning it into an unsafe autonomous maintainer.
