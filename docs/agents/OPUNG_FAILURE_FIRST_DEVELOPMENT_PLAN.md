# Opung Failure-First Development Plan

**Project:** `self-development-agent` untuk `ai-rag-local`  
**Agent:** Opung  
**Primary model:** `qwen2.5-coder:1.5b-instruct`  
**Role:** scoped coding implementer, small patch drafter, unit test drafter, local code assistant  
**Status:** development plan  
**Created:** 2026-05-07 13:53:01

---

# Ringkasan Eksekutif

Dokumen ini merancang **Opung** sebagai agent coding kecil yang bekerja dalam batas sempit. Opung bertugas membaca manifest, memahami konteks kode terbatas, membuat rencana implementasi, menulis draft patch kecil, menulis test kecil jika diminta, dan menjelaskan alasan perubahan.

Opung bukan agent eksekutor. Opung tidak boleh menjalankan shell, apply patch, menjalankan test, install dependency, commit, push, merge, atau mengubah `.env`.

Asumsi utama:

```text
Opung memakai model kecil.
Kemungkinan salah konteks, salah patch, atau over-edit tinggi.
Maka Opung harus dirancang failure-first.
```

Formula inti:

```text
Opung = small scoped coding implementer
Official docs = source of truth
Repo context = prioritas utama
Dataset bug/code review = offline evaluation and pattern reference
Runner = execution
Verification Engine = validation
Safety Gate = risk blocker
Senior Reviewer = final approval
```

---

# Bagian A
# Pondasi Anti-Gagal Opung

Bagian ini dipisahkan dari referensi. Jika semua referensi eksternal gagal, Opung tetap harus aman.

---

## A1. Posisi Opung dalam Multi-Agent System

Opung berada pada jalur implementasi kecil.

Alur dasar:

```text
Human Owner or Siwa
  ↓
Task Manifest
  ↓
Siwa routes scoped coding task
  ↓
Opung reads manifest and allowed files
  ↓
Opung writes implementation plan
  ↓
Opung writes draft patch
  ↓
Asep reviews security if needed
  ↓
Doni reviews DevOps if needed
  ↓
Senior Reviewer approves final patch
  ↓
Safety Gate checks
  ↓
Runner applies patch
  ↓
Verification Engine runs checks
  ↓
Commit Gate may create local commit after all PASS
```

Opung tidak boleh menjalankan patch. Opung hanya membuat **draft patch**.

---

## A2. Opung Role Boundaries

Opung boleh:

```text
membaca manifest
membaca file dalam allowed_paths
membaca git diff
membaca error report
mengambil konteks repo terbatas
mengambil referensi coding terbatas
menulis implementation plan
menulis draft patch kecil
menulis test kecil jika manifest mengizinkan
menulis notes
meminta scope expansion
meminta validasi melalui Siwa atau Senior Reviewer
```

Opung tidak boleh:

```text
apply patch
run shell
run tests
install dependency
modify .env
read secrets
git commit
git push
git merge
git rebase
delete files
large refactor
change architecture
change dependency
change public API without manifest
change security policy
change DevOps config
```

---

## A3. Failure Taxonomy Opung

| Failure | Contoh | Dampak | Respons |
|---|---|---|---|
| Context salah | Opung membaca file tidak relevan | Patch salah | Context Gate |
| Patch terlalu besar | Refactor banyak file | Scope drift | Patch limit |
| API hallucination | Memakai function yang tidak ada | Runtime error | Official docs and repo evidence |
| Test weakening | Mengubah test agar pass | False pass | Senior Reviewer and Verification Engine |
| Dependency creep | Menambah package baru | Build risk | Stop and request Doni review |
| Error swallowing | `except Exception: pass` | Bug tersembunyi | Block by review |
| Secret exposure | Membaca atau menulis `.env` | Critical | Safety Gate block |
| Path unsafe | Operasi file ke denied path | Security risk | Safety Gate block |
| Over-retrieval | Context terlalu banyak | Model bingung | Retrieval budget |
| Dataset mismatch | Bug JS dipakai untuk Python | Patch tidak relevan | Language filter |
| Copy-paste besar | Algorithm repo disalin mentah | License and quality risk | Pattern-only rule |
| No verification | Patch terlihat benar tapi gagal test | Bug masuk | Runner and Verification Engine |
| Silent failure | Opung gagal tanpa report | Tidak bisa audit | Error artifact wajib |

---

## A4. Anti-Failure Gates untuk Opung

Opung harus melewati tujuh gate.

```text
Manifest Gate
Scope Gate
Context Gate
Reference Gate
Patch Size Gate
Evidence Gate
Stop Gate
```

### A4.1 Manifest Gate

Opung hanya boleh bekerja jika manifest valid.

Required fields:

```yaml
task_id:
task_type:
objective:
allowed_paths:
denied_paths:
required_outputs:
risk_level:
mode:
```

Jika manifest tidak valid:

```text
status = manifest_invalid
```

Opung menulis:

```text
data/agent_workspace/errors/{task_id}.opung_manifest_error.md
```

---

### A4.2 Scope Gate

Opung hanya boleh membaca dan membuat draft patch pada path yang diizinkan.

Allowed examples:

```text
app/
tests/
scripts/
docs/ only if task allows docs patch
```

Denied examples:

```text
.env
.env.*
.git/
data/secrets/
production data
credentials
deployment secrets
```

Jika butuh file di luar scope, Opung harus berhenti dan menulis request:

```text
data/agent_workspace/requests/{task_id}.opung_scope_request.md
```

---

### A4.3 Context Gate

Opung tidak boleh membaca seluruh repo. Karena model kecil, konteks harus sempit.

Budget awal:

```yaml
opung_context_budget:
  max_files_read: 6
  max_retrieved_files: 5
  max_retrieved_chunks: 8
  max_chunk_chars: 1800
  max_total_context_chars: 12000
  prefer_same_repo: true
  prefer_same_language: true
  prefer_changed_file_neighbors: true
```

Prioritas konteks:

```text
1. Manifest
2. Changed file
3. Nearby tests
4. Existing similar code in same repo
5. Official language or library docs
6. Dataset or external example only if still unclear
```

---

### A4.4 Reference Gate

Referensi eksternal harus dipakai sesuai fungsi.

```text
Official docs = boleh jadi source of truth
Standard library docs = boleh jadi source of truth
Repo examples = prioritas utama
Algorithm repos = pattern only
Bug datasets = offline evaluation only
StackOverflow datasets = secondary error pattern only
Research papers = design pattern only
```

Opung tidak boleh mengambil patch dari dataset lalu langsung menerapkannya.

---

### A4.5 Patch Size Gate

Batas patch awal:

```yaml
opung_patch_limits:
  max_files_changed: 3
  max_lines_added: 180
  max_lines_removed: 80
  max_patch_bytes: 60000
```

Jika melebihi batas:

```text
Opung must stop and request task split.
```

---

### A4.6 Evidence Gate

Setiap perubahan harus punya alasan.

Minimum evidence:

```yaml
change_reason:
  affected_file:
  related_manifest_objective:
  existing_pattern_used:
  expected_behavior:
  test_needed:
```

Opung tidak boleh menulis patch yang tidak bisa dijelaskan.

---

### A4.7 Stop Gate

Opung harus berhenti jika task butuh:

```text
dependency change
architecture change
large refactor
security-sensitive change
DevOps change
.env change
secret access
shell command
test execution
database migration
production data
new network call
unbounded file operation
```

Output:

```text
data/agent_workspace/requests/{task_id}.opung_stop_request.md
```

---

## A5. Opung Decision Model

Opung hanya boleh menghasilkan keputusan:

```text
draft_patch_ready
needs_scope_expansion
needs_task_split
needs_senior_clarification
blocked_by_policy
```

Opung tidak boleh menghasilkan keputusan:

```text
apply_patch
commit
push
deploy
merge
release
```

---

## A6. Failure-First Patch Policy

Patch Opung harus:

```text
small
scoped
minimal
readable
testable
manifest-bound
reversible
aligned with existing style
```

Patch Opung tidak boleh:

```text
rewrite unrelated code
rename public API casually
change dependency
change config outside scope
delete files
weaken tests
swallow errors silently
hardcode secret
introduce broad exception handling
add network call without approval
```

---

## A7. Error Handling Rules

Opung harus mengikuti aturan berikut:

```text
Fix root cause.
Do not hide exceptions.
Do not add broad `except Exception` unless justified.
Do not return silent defaults if caller needs failure.
Use clear error messages.
Keep exception handling local.
Preserve existing behavior unless manifest asks change.
```

Common safe pattern:

```python
if not path.exists():
    raise FileNotFoundError(f"Input file not found: {path}")
```

Avoid:

```python
try:
    do_work()
except Exception:
    pass
```

---

## A8. Degrade Gracefully Policy

| Kondisi | Fallback |
|---|---|
| Official docs unavailable | Use local repo pattern only |
| Repo context unclear | Ask scope clarification |
| Dataset mismatch | Skip dataset |
| Patch would be too large | Request task split |
| Test change needed but not allowed | Write test suggestion only |
| Dependency change needed | Stop and request Doni review |
| Security-sensitive code touched | Request Asep review |
| DevOps file touched | Request Doni review |
| Output schema invalid | Retry once, then Senior review |

---

## A9. Performance Budget

Metrik:

```text
files read
retrieved chunks
LLM calls
patch size
test draft count
error count
revision count
Senior rejection rate
Verification failure rate
```

Budget awal:

```yaml
opung_performance_budget:
  max_llm_calls_per_task: 2
  max_files_read: 6
  max_reference_chunks: 8
  max_review_duration_seconds: 180
  max_patch_files: 3
  max_report_lines: 250
```

Jika melewati batas, Opung menulis:

```text
data/agent_workspace/performance/{task_id}.opung_performance_warning.md
```

---

## A10. Error Artifact

Jika gagal, Opung wajib menulis:

```text
data/agent_workspace/errors/{task_id}.opung_error.md
```

Template:

```md
# Opung Error Report

## Task ID

## Stage

## Error Type

## Reason

## Inputs Reviewed

## Safe To Resume
yes/no

## Recommended Recovery
```

---

# Bagian B
# Development Plan Opung

---

## B1. Identity Configuration

File:

```text
config/agents.yaml
```

```yaml
opung:
  name: "Opung"
  type: "llm_agent"
  role: "scoped_coding_implementer"
  model: "opung:latest"
  base_model: "qwen2.5-coder:1.5b-instruct"
  temperature: 0.1
  max_context_tokens: 8192

  can_assign_tasks: false
  can_write_patch: true
  can_write_draft_patch: true
  can_apply_patch: false
  can_run_tests: false
  can_run_shell: false
  can_commit: false
  can_push: false

  responsibilities:
    - read_task_manifest
    - read_allowed_files
    - read_git_diff
    - retrieve_small_coding_context
    - write_implementation_plan
    - write_draft_patch
    - write_small_unit_test_patch_if_allowed
    - write_patch_notes
    - request_scope_expansion
    - stop_when_task_exceeds_scope

  denied_responsibilities:
    - apply_patch
    - run_shell
    - run_tests
    - install_dependency
    - modify_env
    - read_secret
    - git_commit
    - git_push
    - git_merge
    - git_rebase
    - delete_file
    - broad_refactor
    - architecture_change
    - dependency_change
```

---

## B2. Modelfile Opung

File:

```text
modelfiles/Modelfile.opung
```

```dockerfile
FROM qwen2.5-coder:1.5b-instruct

PARAMETER temperature 0.1
PARAMETER top_p 0.75
PARAMETER num_ctx 8192

SYSTEM """
You are Opung, the scoped coding implementer for ai-rag-local.

Your job:
- read task manifests;
- read only allowed files;
- use small, relevant coding references;
- write implementation plans;
- draft small patches;
- draft focused unit tests if allowed;
- write clear patch notes;
- stop when the task exceeds scope.

You must not:
- run shell commands;
- apply patches;
- run tests;
- install dependencies;
- modify .env;
- read secrets;
- commit;
- push;
- merge;
- delete files;
- perform broad refactors;
- change architecture;
- change dependencies.

Your patch must be small, scoped, readable, and evidence-based.
If context is insufficient, stop and ask for scope clarification.
"""
```

Command:

```bash
ollama create opung -f modelfiles/Modelfile.opung
```

---

## B3. Tool Permission

Allowed tools:

```yaml
opung_tools:
  allow:
    - read_manifest
    - read_file
    - list_files
    - git_diff
    - retrieve_coding_reference
    - retrieve_official_language_docs
    - retrieve_standard_library_docs
    - retrieve_unit_testing_pattern
    - retrieve_error_message_reference
    - retrieve_same_repo_context
    - write_implementation_plan
    - write_draft_patch
    - write_test_draft_patch
    - write_patch_notes
    - write_scope_request
    - write_stop_request
```

Denied tools:

```yaml
opung_tools:
  deny:
    - apply_patch
    - run_shell
    - run_tests
    - install_dependency
    - modify_env
    - read_secret
    - git_commit
    - git_push
    - git_merge
    - git_rebase
    - delete_file
    - docker_build
    - docker_compose_up
    - terraform_apply
    - kubectl_apply
```

Request-only tools:

```yaml
opung_request_tools:
  allow:
    - request_runner_test
    - request_import_check
    - request_unit_test_run
    - request_scope_expansion
    - request_senior_review
    - request_asep_review
    - request_doni_review
```

---

## B4. Knowledge Base Design

Collection:

```text
opung_coding_knowledge
```

Knowledge domains:

```yaml
opung_knowledge_domains:
  official_language_docs:
    - Python official docs
    - Python language reference
    - Python tutorial
    - Python standard library
    - CPython repository

  standard_library:
    - pathlib
    - json
    - csv
    - re
    - datetime
    - collections
    - itertools
    - functools
    - dataclasses
    - enum
    - typing
    - argparse
    - logging
    - traceback
    - tempfile
    - sqlite3

  unit_testing:
    - pytest docs
    - pytest unittest integration
    - pytest fixtures
    - pytest parametrization
    - pytest monkeypatch
    - unittest
    - unittest.mock
    - coverage.py

  debugging:
    - Python errors and exceptions
    - Python exception hierarchy
    - traceback
    - logging HOWTO
    - pytest failures

  refactoring:
    - Martin Fowler Refactoring
    - Refactoring Guru
    - Clean Code Python
    - PEP 8

  api_usage:
    - FastAPI
    - Pydantic
    - Requests
    - HTTPX
    - Chroma
    - Ollama API
    - Sentence Transformers

  algorithms_and_data_structures:
    - TheAlgorithms Python
    - TheAlgorithms JavaScript
    - Python data structures tutorial
    - heapq
    - bisect
    - graphlib

  bug_fix_datasets:
    - CodeSearchNetRetrieval
    - GHPR Dataset
    - BugsJS
    - FixEval
    - InferredBugs
    - Software defect datasets

  code_review_datasets:
    - Code Review Assistant
    - RosaliaTufano code_review
    - NAIST code review dataset
    - GHPR Dataset

  research_patterns:
    - RepoCoder
    - repo-level-codegen-papers
```

---

## B5. Knowledge Routing

File:

```text
config/opung_knowledge_routing.yaml
```

```yaml
opung_knowledge_routing:
  python_patch:
    - Python official docs
    - Python standard library
    - CPython
    - PEP 8

  unit_test_task:
    - pytest docs
    - pytest unittest integration
    - pytest fixtures
    - unittest.mock

  bug_fix_task:
    - Python errors and exceptions
    - Python exception hierarchy
    - GHPR Dataset
    - FixEval
    - CodeSearchNetRetrieval

  code_review_note:
    - Code Review Assistant
    - RosaliaTufano code_review
    - NAIST code review dataset

  repo_level_context:
    - RepoCoder
    - repo-level-codegen-papers
    - CodeSearchNetRetrieval

  algorithm_helper:
    - TheAlgorithms Python
    - Python standard library algorithm modules

  data_structure_helper:
    - Python data structures tutorial
    - collections
    - dataclasses
    - heapq
    - queue

  api_task:
    - FastAPI docs
    - Pydantic docs
    - Requests docs
    - HTTPX docs

  rag_task:
    - Chroma docs
    - Ollama API docs
    - Sentence Transformers docs

  javascript_task:
    - MDN JavaScript
    - TypeScript Handbook
    - BugsJS
    - TheAlgorithms JavaScript

  error_message:
    - Python exceptions docs
    - traceback
    - StackOverflow Python Questions
    - StackLite
```

---

## B6. Chroma Metadata

Official docs:

```json
{
  "agent": "opung",
  "source_type": "official_language_docs",
  "allowed_use": "coding_reference",
  "runtime_dependency": false,
  "can_execute": false,
  "risk": "low",
  "topic": "python_standard_library"
}
```

Bug-fix dataset:

```json
{
  "agent": "opung",
  "source_type": "bug_fix_dataset",
  "allowed_use": "offline_evaluation_only",
  "runtime_dependency": false,
  "can_generate_patch_directly": false,
  "requires_same_language_filter": true,
  "risk": "medium"
}
```

Code review dataset:

```json
{
  "agent": "opung",
  "source_type": "code_review_dataset",
  "allowed_use": "review_style_and_patch_note_reference",
  "runtime_dependency": false,
  "final_review_authority": false,
  "risk": "medium"
}
```

Research:

```json
{
  "agent": "opung",
  "source_type": "repo_level_codegen_research",
  "allowed_use": "design_pattern_only",
  "runtime_dependency": false,
  "risk": "low"
}
```

Algorithm examples:

```json
{
  "agent": "opung",
  "source_type": "educational_algorithm_reference",
  "allowed_use": "pattern_reference_only",
  "runtime_dependency": false,
  "can_copy_large_code": false,
  "risk": "medium"
}
```

---

## B7. Output Contract

### B7.1 Implementation Plan

Path:

```text
data/agent_workspace/plans/{task_id}.opung_implementation_plan.md
```

Template:

```md
# Opung Implementation Plan

## Task ID

## Objective

## Scope

## Files Reviewed

## Existing Pattern Found

## Proposed Change

## Risk Notes

## Test Needed

## Stop Conditions

## Decision
draft_patch_ready | needs_scope_expansion | needs_task_split | blocked_by_policy
```

---

### B7.2 Draft Patch

Path:

```text
data/agent_workspace/patches/{task_id}.opung_draft.patch
```

Rules:

```text
patch must be unified diff
patch must touch allowed_paths only
patch must stay within patch limits
patch must not include secrets
patch must not include unrelated formatting
```

---

### B7.3 Test Draft Patch

Path:

```text
data/agent_workspace/patches/{task_id}.opung_tests.patch
```

Use only if manifest allows tests.

Rules:

```text
test must verify changed behavior
test must not weaken existing tests
test must not delete assertions
test must not skip tests without reason
```

---

### B7.4 Patch Notes

Path:

```text
data/agent_workspace/notes/{task_id}.opung_notes.md
```

Template:

```md
# Opung Patch Notes

## Task ID

## Summary

## Files Changed

## Why This Change

## Expected Behavior

## Tests Suggested

## Risks

## Needs Review From
Asep | Doni | Senior Reviewer | none
```

---

### B7.5 Scope Request

Path:

```text
data/agent_workspace/requests/{task_id}.opung_scope_request.md
```

Template:

```md
# Opung Scope Request

## Task ID

## Current Scope

## Missing Context

## Why Needed

## Files Requested

## Risk

## Recommended Next Action
```

---

### B7.6 Stop Request

Path:

```text
data/agent_workspace/requests/{task_id}.opung_stop_request.md
```

Template:

```md
# Opung Stop Request

## Task ID

## Stop Reason

## Trigger

## Why This Exceeds Opung Scope

## Suggested Routing
Asep | Doni | Senior Reviewer | Human Owner

## Recommended Next Action
```

---

# Bagian C
# Implementation Roadmap

---

## C1. Phase 0: Contract Freeze

Deliverables:

```text
config/agents.yaml
config/opung_knowledge_routing.yaml
config/opung_guardrails.yaml
schemas/opung_implementation_plan.schema.json
schemas/opung_patch_notes.schema.json
schemas/opung_scope_request.schema.json
```

Exit criteria:

```text
Opung has no execution tools.
Opung cannot apply patch.
Opung cannot run tests.
Opung cannot commit.
Opung cannot push.
Opung cannot modify .env.
```

---

## C2. Phase 1: Read and Plan Only

Capabilities:

```text
read manifest
read allowed files
read git diff
write implementation plan
write stop request
```

Exit criteria:

```text
Opung can produce implementation plan without patch.
Opung stops when task exceeds scope.
```

---

## C3. Phase 2: Small Draft Patch

Capabilities:

```text
write unified diff draft patch
respect allowed_paths
respect patch size limits
write patch notes
```

Exit criteria:

```text
Opung can draft patch touching max 3 files.
No apply.
No execution.
```

---

## C4. Phase 3: Test Drafting

Capabilities:

```text
write small unit test patch
use pytest or unittest based on existing repo style
use tmp_path, monkeypatch, mock when needed
```

Exit criteria:

```text
Opung drafts test without weakening existing tests.
Runner remains responsible for execution.
```

---

## C5. Phase 4: Error Message Assistance

Capabilities:

```text
read error report
classify exception
retrieve official exception docs
suggest root-cause fix
write draft patch if scope allows
```

Exit criteria:

```text
Opung can handle common Python errors with evidence.
```

---

## C6. Phase 5: Repo-Level Context Retrieval

Capabilities:

```text
retrieve same-repo related files
use RepoCoder-style limited retrieval
use CodeSearchNet-like retrieval benchmark for evaluation
```

Exit criteria:

```text
Opung retrieves relevant context without context overload.
```

---

## C7. Phase 6: Offline Evaluation with Datasets

Use datasets only for evaluation:

```text
CodeSearchNetRetrieval
GHPR Dataset
FixEval
BugsJS
InferredBugs
Code-Review-Assistant
Software defect prediction datasets
StackOverflow datasets
```

Metrics:

```text
patch relevance
context relevance
syntax correctness after Runner check
test pass rate after Verification Engine
Senior acceptance rate
false fix rate
scope violation rate
```

Exit criteria:

```text
Datasets improve evaluation, not direct patch generation.
```

---

## C8. Phase 7: Stabilization

Metrics:

```text
draft patch acceptance rate
Senior revision count
Verification pass rate
patch size
context size
task stop accuracy
dependency escalation accuracy
security escalation accuracy
```

Exit criteria:

```text
Opung consistently writes small scoped patches with low scope violation.
```

---

# Bagian D
# Referensi Terpisah dari Pondasi Anti-Gagal

Referensi tidak menjadi dependency inti. Referensi hanya menjadi knowledge base, pattern, or offline evaluation material.

---

## D1. Compatibility Score

| Criteria | Weight |
|---|---:|
| Matches small scoped coding use | 20 |
| Can be used read-only | 15 |
| Supports same-language filtering | 15 |
| Supports test or validation | 10 |
| Low copy-paste risk | 10 |
| Low overengineering risk | 10 |
| Clear examples or docs | 10 |
| Can be scoped by file type | 10 |

Decision:

```text
>= 80  core knowledge
60-79  optional knowledge
40-59  offline evaluation or pattern only
< 40   exclude
```

---

## D2. Official Language and Standard Library References

| Reference | Link | Use |
|---|---|---|
| Python official docs | https://docs.python.org/3/ | Python language and library reference |
| Python tutorial | https://docs.python.org/3/tutorial/ | Basic syntax and usage |
| Python language reference | https://docs.python.org/3/reference/ | Exact syntax and semantics |
| Python standard library | https://docs.python.org/3/library/index.html | Built-in modules |
| CPython | https://github.com/python/cpython | Official Python source and stdlib reference |
| PEP 8 | https://peps.python.org/pep-0008/ | Python style |
| PEP 257 | https://peps.python.org/pep-0257/ | Docstring conventions |
| PEP 484 | https://peps.python.org/pep-0484/ | Type hints |

Adoption:

```text
Core knowledge.
```

---

## D3. Testing References

| Reference | Link | Use |
|---|---|---|
| pytest docs | https://docs.pytest.org/en/stable/ | Python test framework |
| pytest unittest integration | https://docs.pytest.org/en/stable/how-to/unittest.html | Run unittest tests with pytest |
| pytest fixtures | https://docs.pytest.org/en/stable/how-to/fixtures.html | Fixtures |
| pytest parametrization | https://docs.pytest.org/en/stable/how-to/parametrize.html | Parametrized tests |
| pytest monkeypatch | https://docs.pytest.org/en/stable/how-to/monkeypatch.html | Monkeypatch |
| unittest | https://docs.python.org/3/library/unittest.html | Built-in tests |
| unittest.mock | https://docs.python.org/3/library/unittest.mock.html | Mocking |

Adoption:

```text
Core knowledge for test drafting.
```

---

## D4. Algorithm and Data Structure References

| Reference | Link | Use |
|---|---|---|
| TheAlgorithms Python | https://github.com/TheAlgorithms/Python | Educational algorithm examples |
| TheAlgorithms Python fork | https://github.com/subbarayudu-j/TheAlgorithms-Python | Educational mirror/fork |
| TheAlgorithms general fork | https://github.com/dsc-iem/TheAlgorithms | Educational algorithm examples |
| TheAlgorithms JavaScript | https://github.com/kansiris/TheAlgorithms-Javascript | JavaScript algorithm examples |
| Python data structures tutorial | https://docs.python.org/3/tutorial/datastructures.html | Python data structures |
| collections | https://docs.python.org/3/library/collections.html | Built-in specialized containers |
| heapq | https://docs.python.org/3/library/heapq.html | Priority queue |
| bisect | https://docs.python.org/3/library/bisect.html | Binary search |
| graphlib | https://docs.python.org/3/library/graphlib.html | Topological sort |

Adoption:

```text
Educational pattern only.
Prefer standard library.
No large copy-paste.
```

---

## D5. Refactoring and Code Quality References

| Reference | Link | Use |
|---|---|---|
| Clean Code Python | https://github.com/zedr/clean-code-python | Readability and refactoring guidance |
| Martin Fowler Refactoring | https://martinfowler.com/books/refactoring.html | Refactoring principles |
| Martin Fowler Code Smell | https://martinfowler.com/bliki/CodeSmell.html | Code smell |
| Refactoring Guru | https://refactoring.guru/refactoring | Refactoring catalog |
| Refactoring Guru smells | https://refactoring.guru/refactoring/smells | Code smell catalog |
| Refactoring Guru techniques | https://refactoring.guru/refactoring/techniques | Refactoring techniques |

Adoption:

```text
Supporting knowledge.
Small refactor only.
No broad architecture change.
```

---

## D6. Code Retrieval and Repo-Level Coding References

| Reference | Link | Use |
|---|---|---|
| CodeSearchNetRetrieval | https://huggingface.co/datasets/mteb/CodeSearchNetRetrieval | Code retrieval benchmark |
| RepoCoder paper | https://arxiv.org/abs/2303.12570 | Repository-level retrieval and generation design |
| Repo-level codegen papers | https://github.com/allanj/repo-level-codegen-papers | Research map |
| CPython | https://github.com/python/cpython | Official repo-level reference |

Adoption:

```text
Design pattern and retrieval benchmark.
Do not import full implementation.
```

---

## D7. Bug-Fix and Defect Dataset References

| Reference | Link | Use |
|---|---|---|
| Defect Datasets index | https://defect-datasets.github.io/ | Dataset discovery |
| Software Defect Prediction | https://www.kaggle.com/datasets/semustafacevik/software-defect-prediction | Offline defect prediction evaluation |
| Software Defect Prediction Dataset | https://www.kaggle.com/datasets/ziya07/software-defect-prediction-dataset | Offline evaluation |
| Bug Prediction Dataset | https://www.kaggle.com/datasets/syedzubair/bug-prediction-dataset | Offline evaluation |
| GHPR Dataset | https://github.com/feiwww/GHPR_dataset | Pull-request bug-fix dataset |
| BugsJS | https://github.com/BugsJS/bug-dataset | JavaScript bug benchmark |
| FixEval | https://github.com/mahimanzum/FixEval | Execution-based code repair evaluation |
| InferredBugs | https://github.com/microsoft/InferredBugs | Static-analysis derived bug/fix dataset |
| Software bug prediction | https://github.com/YousefGh/software_bug_prediction | Bug prediction reference |

Adoption:

```text
Offline evaluation only.
No direct patch generation authority.
Language filter required.
```

---

## D8. Code Review Dataset References

| Reference | Link | Use |
|---|---|---|
| Code Review Data v2 | https://www.kaggle.com/datasets/bulivington/code-review-data-v2 | Code review data |
| Code Review Assistant | https://huggingface.co/datasets/alenphilip/Code-Review-Assistant | Review instruction dataset |
| RosaliaTufano code_review | https://github.com/RosaliaTufano/code_review | Code review research package |
| NAIST code review dataset list | https://naist-se.github.io/code-review/dataset/ | Code review dataset index |
| GHPR Dataset | https://github.com/feiwww/GHPR_dataset | Pull request and bug-fix examples |

Adoption:

```text
Review style and patch note reference only.
Senior Reviewer remains final authority.
```

---

## D9. StackOverflow and Error KB References

| Reference | Link | Use |
|---|---|---|
| StackLite | https://www.kaggle.com/datasets/stackoverflow/stacklite | Secondary Q&A retrieval |
| StackOverflow Python Questions | https://www.kaggle.com/datasets/stackoverflow/pythonquestions | Python error and Q&A examples |
| Python exceptions docs | https://docs.python.org/3/library/exceptions.html | Official exception behavior |
| Python errors tutorial | https://docs.python.org/3/tutorial/errors.html | Exception handling |
| Pydantic errors | https://docs.pydantic.dev/latest/errors/errors/ | Validation error handling |
| FastAPI errors | https://fastapi.tiangolo.com/tutorial/handling-errors/ | API error handling |

Adoption:

```text
Official docs first.
StackOverflow datasets secondary and noisy.
```

---

## D10. API Usage References

| Reference | Link | Use |
|---|---|---|
| FastAPI | https://fastapi.tiangolo.com/ | API framework |
| FastAPI testing | https://fastapi.tiangolo.com/tutorial/testing/ | TestClient |
| Pydantic | https://docs.pydantic.dev/latest/ | Data validation |
| Requests | https://requests.readthedocs.io/en/latest/ | HTTP client |
| HTTPX | https://www.python-httpx.org/ | HTTP client |
| Chroma docs | https://docs.trychroma.com/ | Vector DB API |
| Chroma GitHub | https://github.com/chroma-core/chroma | Chroma source |
| Ollama API | https://github.com/ollama/ollama/blob/main/docs/api.md | Local model API |
| Sentence Transformers | https://www.sbert.net/ | Embedding model docs |

Adoption:

```text
Conditional core depending on repo usage.
No new network behavior without manifest.
No collection reset without explicit approval.
```

---

# Bagian E
# Test and Acceptance Criteria

---

## E1. Minimum Acceptance Criteria

Opung is ready for early use if:

```text
Can read manifest.
Can read allowed files.
Can detect denied scope.
Can write implementation plan.
Can write small draft patch.
Can write patch notes.
Can stop when task exceeds scope.
Can request Senior clarification.
Can avoid execution.
```

---

## E2. Failure Acceptance Criteria

The system is safe if:

```text
Opung cannot run shell.
Opung cannot apply patch.
Opung cannot run tests.
Opung cannot install dependency.
Opung cannot commit.
Opung cannot push.
Opung cannot modify .env.
Opung cannot read secrets.
Opung cannot delete files.
Opung writes error artifact when failing.
```

---

## E3. First Dry-Run Scenario

Input:

```yaml
task_id: task-opung-001
task_type: implementation
risk_level: low
mode: draft_patch
allowed_paths:
  - app/importers/
  - tests/importers/
denied_paths:
  - .env
  - .git/
required_outputs:
  - implementation_plan
  - draft_patch
  - patch_notes
```

Expected:

```text
Opung reads manifest.
Opung reads relevant allowed files.
Opung writes implementation plan.
Opung writes draft patch.
Opung writes patch notes.
Opung does not apply patch.
Opung does not run tests.
```

---

## E4. Scope Failure Scenario

Input:

```yaml
task_id: task-opung-002
task_type: implementation
risk_level: medium
allowed_paths:
  - app/
denied_paths:
  - .env
changed_need:
  - pyproject.toml
```

Expected:

```text
Opung detects dependency/config change outside scope.
Opung stops.
Opung writes scope request.
No patch.
```

---

## E5. Error Fix Scenario

Input:

```yaml
task_id: task-opung-003
task_type: bug_fix
risk_level: low
error: JSONDecodeError
allowed_paths:
  - app/importers/
  - tests/importers/
```

Expected:

```text
Opung retrieves Python json and exception docs.
Opung reviews importer file.
Opung drafts small fix with clear error handling.
Opung drafts test if allowed.
No execution.
```

---

# Final Summary

Opung must be built as a **failure-first small coding implementer**.

Final rule:

```text
Opung reads.
Opung plans.
Opung writes small draft patches.
Opung writes small tests if allowed.
Runner executes.
Verification Engine validates.
Senior Reviewer approves.
Opung never executes or commits.
```

This keeps Opung useful for local coding tasks without turning it into an unsafe autonomous developer.
