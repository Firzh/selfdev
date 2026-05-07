# Opung Knowledge Base Links

**Agent:** Opung  
**Role:** scoped coding implementer, small patch drafter, unit test drafter, local code assistant  
**Primary model:** `qwen2.5-coder:1.5b-instruct`  
**Purpose:** revised knowledge base links untuk official language docs, standard library docs, code retrieval, bug-fix datasets, code review datasets, unit testing patterns, debugging, refactoring, error fixes, API usage examples, dan repo-level coding references  
**Created:** 2026-05-07 13:58:54  
**Filename:** `OPUNG_KNOWLEDGE_BASE_LINKS.md`

---

# 0. Status Dokumen

Dokumen ini adalah versi revisi dari knowledge base link untuk **Opung**.

Perubahan utama versi revisi:

```text
1. Menambahkan dataset CodeSearchNetRetrieval.
2. Menambahkan defect dataset dan bug prediction dataset.
3. Menambahkan GHPR, BugsJS, FixEval, dan InferredBugs.
4. Menambahkan Code Review Assistant dan code review datasets.
5. Menambahkan RepoCoder dan repo-level code generation papers.
6. Memisahkan official docs, dataset, GitHub repo, dan research reference.
7. Menegaskan bahwa dataset hanya untuk retrieval benchmark, pattern reference, atau offline evaluation.
8. Menegaskan bahwa Opung tidak boleh apply patch, run tests, install dependency, commit, atau push.
```

Dokumen ini boleh menimpa file sebelumnya dengan nama yang sama.

---

# 1. Fungsi Knowledge Base Opung

Knowledge base ini dipakai untuk memperkuat Opung sebagai **small scoped coding implementer**.

Opung memakai knowledge base ini untuk:

```text
membaca pola kode
menulis patch kecil
menulis unit test kecil
menganalisis error
memilih standard library yang tepat
memahami API usage
membuat patch notes
memperbaiki exception sederhana
menghindari API hallucination
mencari konteks repo secara terbatas
```

Opung tidak boleh memakai knowledge base ini sebagai izin untuk:

```text
apply patch sendiri
run shell
run tests sendiri
install dependency
mengubah .env
membaca secret
commit
push
merge
delete file
large refactor
mengubah arsitektur besar
mengubah dependency
mengubah public API tanpa manifest
```

Prinsip:

```text
Knowledge base = boleh dibaca
Draft patch = boleh dibuat sesuai manifest
Execution = Runner
Validation = Verification Engine
Risk enforcement = Safety Gate
Final approval = Senior Reviewer
```

---

# 2. Core Base Knowledge untuk Opung

| Domain | Isi yang perlu dipahami | Fungsi Opung |
|---|---|---|
| Official language docs | Syntax, semantics, language reference | Menulis kode benar |
| Standard library docs | `pathlib`, `json`, `typing`, `logging`, `argparse`, `dataclasses` | Memakai library bawaan |
| Code retrieval | Query-code matching, repo-level context | Mengambil konteks kode relevan |
| Algorithm examples | Searching, sorting, graph, queue, heap | Membantu helper kecil |
| Data structures | List, dict, set, deque, heap, dataclass | Memilih struktur data sederhana |
| Unit testing | pytest, unittest, fixture, mock, parametrization | Menulis test kecil |
| Debugging | traceback, exception hierarchy, logs | Menghubungkan error ke root cause |
| Refactoring | small extract function, rename, simplify conditional | Refactor kecil tanpa ubah behavior |
| Error KB | Common Python exceptions | Fix defensif dan jelas |
| API usage examples | FastAPI, Pydantic, Chroma, Ollama, Requests, HTTPX | Menggunakan API tanpa mengarang |
| Bug-fix datasets | GHPR, FixEval, BugsJS, InferredBugs | Offline evaluation dan pattern learning |
| Code review datasets | Code Review Assistant, NAIST, Tufano | Style review dan patch note |
| Repo-level research | RepoCoder, repo-level-codegen-papers | Desain retrieval terbatas |

---

# 3. Official Language Docs

## 3.1 Python Core Docs

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Python official docs | https://docs.python.org/3/ | Main Python documentation |
| 2 | Python tutorial | https://docs.python.org/3/tutorial/ | Syntax and basic usage |
| 3 | Python language reference | https://docs.python.org/3/reference/ | Exact syntax and semantics |
| 4 | Python standard library | https://docs.python.org/3/library/index.html | Standard library reference |
| 5 | Python built-in functions | https://docs.python.org/3/library/functions.html | Built-in function usage |
| 6 | Python built-in types | https://docs.python.org/3/library/stdtypes.html | `str`, `list`, `dict`, `set`, `tuple` |
| 7 | Python data model | https://docs.python.org/3/reference/datamodel.html | Object model and class behavior |
| 8 | Python glossary | https://docs.python.org/3/glossary.html | Terminology reference |
| 9 | CPython GitHub | https://github.com/python/cpython | Official Python source repository |

Use for Opung:

```text
Check syntax.
Avoid invented APIs.
Use official behavior.
Understand Python object model.
Keep patch compatible with existing Python version.
```

Restrictions:

```text
Opung must not change Python runtime version.
Opung must not install a new package only because docs mention it.
Opung must not copy large CPython implementation.
```

---

## 3.2 Python Style and Typing References

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | PEP 8 | https://peps.python.org/pep-0008/ | Python style guide |
| 2 | PEP 257 | https://peps.python.org/pep-0257/ | Docstring conventions |
| 3 | PEP 484 | https://peps.python.org/pep-0484/ | Type hints |
| 4 | Typing module docs | https://docs.python.org/3/library/typing.html | Type annotation usage |
| 5 | MyPy docs | https://mypy.readthedocs.io/en/stable/ | Static typing reference |
| 6 | Ruff docs | https://docs.astral.sh/ruff/ | Linting and formatting reference |
| 7 | Black docs | https://black.readthedocs.io/en/stable/ | Code formatting reference |

Use for Opung:

```text
Write readable Python.
Add type hints only when useful.
Keep style aligned with existing repo.
Avoid broad formatting changes.
```

Restrictions:

```text
Opung must not reformat entire repository.
Opung must not add mypy, ruff, or black unless manifest allows dependency or tooling change.
```

---

## 3.3 Optional JavaScript and TypeScript Docs

Use only if changed files include JavaScript or TypeScript.

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | MDN JavaScript Guide | https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide | JavaScript language guide |
| 2 | MDN JavaScript Reference | https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference | JavaScript API reference |
| 3 | TypeScript Handbook | https://www.typescriptlang.org/docs/handbook/intro.html | TypeScript syntax and patterns |
| 4 | Node.js docs | https://nodejs.org/docs/latest/api/ | Node.js standard APIs |
| 5 | npm package scripts | https://docs.npmjs.com/cli/v10/using-npm/scripts | npm script reference |

Restrictions:

```text
Only retrieve JS/TS docs when task needs JS/TS.
Do not add npm dependencies without manifest approval.
```

---

# 4. Standard Library Docs

## 4.1 Core Standard Library

| No | Module | Link | Use |
|---:|---|---|---|
| 1 | `pathlib` | https://docs.python.org/3/library/pathlib.html | Safe path handling |
| 2 | `os` | https://docs.python.org/3/library/os.html | OS interaction, use carefully |
| 3 | `shutil` | https://docs.python.org/3/library/shutil.html | File operations, use carefully |
| 4 | `json` | https://docs.python.org/3/library/json.html | JSON parsing and writing |
| 5 | `csv` | https://docs.python.org/3/library/csv.html | CSV parsing |
| 6 | `re` | https://docs.python.org/3/library/re.html | Regex handling |
| 7 | `datetime` | https://docs.python.org/3/library/datetime.html | Dates and times |
| 8 | `collections` | https://docs.python.org/3/library/collections.html | `deque`, `Counter`, `defaultdict` |
| 9 | `itertools` | https://docs.python.org/3/library/itertools.html | Iteration helpers |
| 10 | `functools` | https://docs.python.org/3/library/functools.html | `lru_cache`, decorators |
| 11 | `dataclasses` | https://docs.python.org/3/library/dataclasses.html | Structured data |
| 12 | `enum` | https://docs.python.org/3/library/enum.html | Enum values |
| 13 | `typing` | https://docs.python.org/3/library/typing.html | Type hints |
| 14 | `abc` | https://docs.python.org/3/library/abc.html | Abstract base classes |
| 15 | `argparse` | https://docs.python.org/3/library/argparse.html | CLI argument parsing |
| 16 | `logging` | https://docs.python.org/3/library/logging.html | Logging |
| 17 | `traceback` | https://docs.python.org/3/library/traceback.html | Traceback handling |
| 18 | `warnings` | https://docs.python.org/3/library/warnings.html | Warning handling |
| 19 | `tempfile` | https://docs.python.org/3/library/tempfile.html | Temporary files |
| 20 | `sqlite3` | https://docs.python.org/3/library/sqlite3.html | SQLite usage |
| 21 | `subprocess` | https://docs.python.org/3/library/subprocess.html | Sensitive command execution reference only |

Use for Opung:

```text
Prefer standard library before dependency.
Use pathlib for path handling.
Use json/csv with explicit encoding.
Use logging instead of print for application code.
Use dataclasses for structured records.
```

Failure-first note:

```text
os, shutil, and subprocess are sensitive.
Opung may read their docs.
Opung must not draft destructive operations without manifest scope and review.
```

---

## 4.2 Testing and Debugging Standard Library

| No | Module | Link | Use |
|---:|---|---|---|
| 1 | `unittest` | https://docs.python.org/3/library/unittest.html | Unit testing framework |
| 2 | `unittest.mock` | https://docs.python.org/3/library/unittest.mock.html | Mocking |
| 3 | `doctest` | https://docs.python.org/3/library/doctest.html | Docstring tests |
| 4 | `pdb` | https://docs.python.org/3/library/pdb.html | Debugger reference |
| 5 | `faulthandler` | https://docs.python.org/3/library/faulthandler.html | Dump Python tracebacks |
| 6 | `inspect` | https://docs.python.org/3/library/inspect.html | Introspection |
| 7 | `timeit` | https://docs.python.org/3/library/timeit.html | Microbenchmarking |
| 8 | `profile` and `pstats` | https://docs.python.org/3/library/profile.html | Profiling reference |

Restrictions:

```text
Opung may draft tests.
Opung must not run tests directly.
Runner runs tests.
```

---

# 5. Unit Testing Patterns

## 5.1 Core Testing References

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | pytest docs | https://docs.pytest.org/en/stable/ | Main pytest documentation |
| 2 | pytest getting started | https://docs.pytest.org/en/stable/getting-started.html | Basic pytest usage |
| 3 | pytest unittest integration | https://docs.pytest.org/en/stable/how-to/unittest.html | Running unittest-style tests with pytest |
| 4 | pytest fixtures | https://docs.pytest.org/en/stable/how-to/fixtures.html | Fixture patterns |
| 5 | pytest parametrization | https://docs.pytest.org/en/stable/how-to/parametrize.html | Parameterized tests |
| 6 | pytest monkeypatch | https://docs.pytest.org/en/stable/how-to/monkeypatch.html | Monkeypatching |
| 7 | pytest tmp_path | https://docs.pytest.org/en/stable/how-to/tmp_path.html | Temporary path testing |
| 8 | Python unittest | https://docs.python.org/3/library/unittest.html | Built-in unit testing |
| 9 | unittest.mock | https://docs.python.org/3/library/unittest.mock.html | Mocking |
| 10 | Hypothesis docs | https://hypothesis.readthedocs.io/en/latest/ | Property-based testing |
| 11 | Coverage.py docs | https://coverage.readthedocs.io/en/latest/ | Coverage measurement |

Use for Opung:

```text
Write small tests.
Test changed behavior only.
Use fixtures when needed.
Use tmp_path for filesystem behavior.
Use monkeypatch or mock for external calls.
Preserve unittest style if repo already uses it.
```

Restrictions:

```text
Opung writes tests only if manifest allows.
Opung does not run pytest directly.
Runner runs test.
Opung must not weaken tests.
```

---

## 5.2 Suggested Unit Test Template

```python
def test_expected_behavior():
    # arrange
    input_value = "example"

    # act
    result = function_under_test(input_value)

    # assert
    assert result == "expected"
```

Failure test pattern:

```python
import pytest

def test_invalid_input_raises_clear_error():
    with pytest.raises(ValueError, match="clear message"):
        function_under_test(None)
```

---

# 6. Algorithm and Data Structure Examples

## 6.1 Algorithm References

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | TheAlgorithms Python | https://github.com/TheAlgorithms/Python | Educational algorithm examples in Python |
| 2 | TheAlgorithms Python fork | https://github.com/subbarayudu-j/TheAlgorithms-Python | Educational mirror/fork |
| 3 | TheAlgorithms general fork | https://github.com/dsc-iem/TheAlgorithms | Educational algorithm examples |
| 4 | TheAlgorithms JavaScript | https://github.com/kansiris/TheAlgorithms-Javascript | JavaScript algorithm examples |
| 5 | The Algorithms website | https://the-algorithms.com/ | Multi-language algorithm reference |
| 6 | Python `bisect` | https://docs.python.org/3/library/bisect.html | Binary search helpers |
| 7 | Python `heapq` | https://docs.python.org/3/library/heapq.html | Heap queue |
| 8 | Python `graphlib` | https://docs.python.org/3/library/graphlib.html | Topological sorting |
| 9 | Python `statistics` | https://docs.python.org/3/library/statistics.html | Basic statistics |

Use for Opung:

```text
Understand algorithm patterns.
Draft simple helper when needed.
Prefer standard library.
Avoid copying large implementation.
```

Restrictions:

```text
Pattern-only.
No large copy-paste.
No algorithm replacement unless task requires it.
```

## 6.2 Data Structure References

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Python data structures tutorial | https://docs.python.org/3/tutorial/datastructures.html | Lists, tuples, sets, dictionaries |
| 2 | Python built-in types | https://docs.python.org/3/library/stdtypes.html | Built-in data structures |
| 3 | `collections` module | https://docs.python.org/3/library/collections.html | `deque`, `Counter`, `defaultdict`, `namedtuple` |
| 4 | `heapq` module | https://docs.python.org/3/library/heapq.html | Priority queue |
| 5 | `queue` module | https://docs.python.org/3/library/queue.html | Thread-safe queue |
| 6 | `dataclasses` module | https://docs.python.org/3/library/dataclasses.html | Structured data |
| 7 | TheAlgorithms data structures | https://github.com/TheAlgorithms/Python/tree/master/data_structures | Educational implementations |

Use for Opung:

```text
Use dict/list/set before custom structure.
Use dataclass for structured record.
Use deque for queue-like behavior.
Use heapq for priority behavior.
```

Restrictions:

```text
Do not introduce complex data model without Senior Reviewer approval.
Do not change public data schema without manifest approval.
```

---

# 7. Debugging Checklist and Error Knowledge Base

## 7.1 Debugging References

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Python errors tutorial | https://docs.python.org/3/tutorial/errors.html | Exception basics |
| 2 | Python exception hierarchy | https://docs.python.org/3/library/exceptions.html | Built-in exceptions |
| 3 | Traceback module | https://docs.python.org/3/library/traceback.html | Traceback parsing |
| 4 | Import system reference | https://docs.python.org/3/reference/import.html | Import behavior |
| 5 | `json.JSONDecodeError` | https://docs.python.org/3/library/json.html#json.JSONDecodeError | JSON parse error |
| 6 | `argparse` errors | https://docs.python.org/3/library/argparse.html | CLI parsing error |
| 7 | pytest failures | https://docs.pytest.org/en/stable/how-to/failures.html | Test failure output |
| 8 | Pydantic errors | https://docs.pydantic.dev/latest/errors/errors/ | Validation error handling |
| 9 | FastAPI errors | https://fastapi.tiangolo.com/tutorial/handling-errors/ | HTTP exception handling |
| 10 | Python FAQ | https://docs.python.org/3/faq/programming.html | Common programming questions |
| 11 | Logging HOWTO | https://docs.python.org/3/howto/logging.html | Logging guide |
| 12 | Logging cookbook | https://docs.python.org/3/howto/logging-cookbook.html | Advanced logging pattern |

## 7.2 Opung Debugging Checklist

```text
1. Read exact error message.
2. Identify exception type.
3. Identify file and line.
4. Check changed code first.
5. Check inputs and assumptions.
6. Check path handling and encoding.
7. Check None handling.
8. Check import path.
9. Check external dependency usage.
10. Suggest smallest patch.
11. Add or update focused test if manifest allows.
12. Do not add broad refactor.
```

Restrictions:

```text
Opung may use error reports.
Opung may not run interactive debugger.
Opung may not execute code directly.
```

## 7.3 Common Error Routing

```yaml
error_knowledge_routing:
  "ModuleNotFoundError":
    - Python import system reference
    - Packaging user guide
  "ImportError":
    - Python import system reference
  "FileNotFoundError":
    - pathlib
    - os
  "PermissionError":
    - built-in exceptions
  "KeyError":
    - built-in exceptions
    - dict docs
  "TypeError":
    - built-in exceptions
    - typing docs
  "ValueError":
    - built-in exceptions
  "JSONDecodeError":
    - json docs
  "ValidationError":
    - Pydantic errors
  "HTTPException":
    - FastAPI error handling
  "AssertionError":
    - pytest failures
```

---

# 8. Common Exception Fixes

| Exception | Common Cause | Safe Fix Pattern |
|---|---|---|
| `ModuleNotFoundError` | Import path or missing package | Check existing dependency, avoid adding dependency without manifest |
| `ImportError` | Wrong import name or circular import | Check module path and import order |
| `FileNotFoundError` | Wrong path or missing file | Use `pathlib`, validate path, clear error message |
| `PermissionError` | File permission issue | Do not bypass permission, report clearly |
| `KeyError` | Missing dict key | Validate key or use `.get()` only when default is correct |
| `TypeError` | Wrong type passed | Add type guard or fix caller |
| `ValueError` | Invalid value | Validate input and raise clear error |
| `JSONDecodeError` | Invalid JSON | Catch and return useful error if appropriate |
| `AttributeError` | Object is `None` or wrong type | Check construction and optional values |
| `IndexError` | Bad list index | Check length or iterate safely |
| `AssertionError` | Test expectation failed | Fix behavior, do not weaken test without reason |

Rules:

```text
Prefer fixing root cause.
Do not swallow exceptions silently.
Do not use broad `except Exception` unless justified.
Do not hide failing tests.
Add clear error messages.
Keep exception handling local.
Avoid changing public behavior without manifest.
```

---

# 9. Refactoring and Code Quality Patterns

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Martin Fowler Refactoring | https://martinfowler.com/books/refactoring.html | Refactoring principles |
| 2 | Martin Fowler Code Smell | https://martinfowler.com/bliki/CodeSmell.html | Code smell concept |
| 3 | Refactoring Guru | https://refactoring.guru/refactoring | Refactoring catalog |
| 4 | Refactoring Guru Code Smells | https://refactoring.guru/refactoring/smells | Code smell catalog |
| 5 | Refactoring Guru Techniques | https://refactoring.guru/refactoring/techniques | Refactoring techniques |
| 6 | SourceMaking Refactoring | https://sourcemaking.com/refactoring | Refactoring examples |
| 7 | Clean Code Python | https://github.com/zedr/clean-code-python | Python readability and refactoring guidance |

Use for Opung:

```text
Extract small function.
Rename confusing local variable.
Remove small duplication.
Simplify conditional.
Add guard clause.
Keep behavior unchanged.
```

Restrictions:

```text
No broad refactor.
No public API change without manifest.
No unrelated formatting.
No architecture change.
```

---

# 10. API Usage Examples

## 10.1 HTTP Client APIs

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Requests docs | https://requests.readthedocs.io/en/latest/ | HTTP client usage |
| 2 | HTTPX docs | https://www.python-httpx.org/ | Async/sync HTTP client |
| 3 | urllib.request | https://docs.python.org/3/library/urllib.request.html | Standard library HTTP |
| 4 | urllib.parse | https://docs.python.org/3/library/urllib.parse.html | URL parsing |
| 5 | aiohttp docs | https://docs.aiohttp.org/en/stable/ | Async HTTP if already used |

Use for Opung:

```text
Write small API calls.
Handle timeouts.
Handle status codes.
Avoid hardcoded secrets.
Avoid network calls unless manifest allows.
```

Restrictions:

```text
Opung must not add network call unless task explicitly requires it.
Opung must not hardcode token or secret URL.
```

## 10.2 FastAPI and Pydantic APIs

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | FastAPI docs | https://fastapi.tiangolo.com/ | FastAPI main docs |
| 2 | FastAPI testing | https://fastapi.tiangolo.com/tutorial/testing/ | TestClient usage |
| 3 | FastAPI error handling | https://fastapi.tiangolo.com/tutorial/handling-errors/ | HTTPException and error response |
| 4 | Pydantic docs | https://docs.pydantic.dev/latest/ | Data validation |
| 5 | Pydantic models | https://docs.pydantic.dev/latest/concepts/models/ | Model patterns |
| 6 | Pydantic errors | https://docs.pydantic.dev/latest/errors/errors/ | Validation error handling |

Use for Opung:

```text
Write or adjust small endpoint behavior.
Add validation model carefully.
Handle API errors consistently.
Write focused API tests.
```

Restrictions:

```text
Do not change public endpoint contract unless manifest allows.
Do not invent schema not present in source or task.
```

## 10.3 Chroma and RAG APIs

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Chroma docs | https://docs.trychroma.com/ | ChromaDB documentation |
| 2 | Chroma GitHub | https://github.com/chroma-core/chroma | Chroma source repository |
| 3 | LangChain Python docs | https://python.langchain.com/docs/ | LangChain reference if repo uses it |
| 4 | OpenAI API docs | https://platform.openai.com/docs/ | OpenAI API if repo uses it |
| 5 | Ollama API docs | https://github.com/ollama/ollama/blob/main/docs/api.md | Ollama local model API |
| 6 | Sentence Transformers docs | https://www.sbert.net/ | Embedding model usage |

Use for Opung:

```text
Understand RAG API usage.
Avoid confusing Chroma data with model weights.
Handle collection names carefully.
Respect collection reset policy.
```

Restrictions:

```text
Do not delete or reset Chroma collections unless manifest explicitly allows.
Do not modify production-like data.
```

## 10.4 CLI and Config API Examples

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | argparse docs | https://docs.python.org/3/library/argparse.html | CLI parser |
| 2 | Typer docs | https://typer.tiangolo.com/ | CLI framework if used |
| 3 | Click docs | https://click.palletsprojects.com/ | CLI framework if used |
| 4 | PyYAML docs | https://pyyaml.org/wiki/PyYAMLDocumentation | YAML parsing if used |
| 5 | `tomllib` docs | https://docs.python.org/3/library/tomllib.html | TOML parsing |
| 6 | python-dotenv docs | https://saurabh-kumar.com/python-dotenv/ | Env loading if already used |

Restrictions:

```text
Do not modify .env.
Do not print secrets.
Do not add destructive CLI flags.
```

---

# 11. Code Retrieval and Repo-Level Coding

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | CodeSearchNetRetrieval | https://huggingface.co/datasets/mteb/CodeSearchNetRetrieval | Code retrieval benchmark |
| 2 | RepoCoder paper | https://arxiv.org/abs/2303.12570 | Repository-level retrieval and generation design |
| 3 | Repo-level codegen papers | https://github.com/allanj/repo-level-codegen-papers | Research map for repo-level code generation |
| 4 | CPython | https://github.com/python/cpython | Official repo-level reference |

Use for Opung:

```text
Evaluate code retrieval quality.
Design limited repo context retrieval.
Find similar usage patterns.
Prevent single-file tunnel vision.
```

Failure-first rule:

```text
Prefer same repo.
Prefer same language.
Limit retrieved files.
Do not retrieve entire repo.
Do not use research repo as runtime dependency.
```

Suggested retrieval budget:

```yaml
opung_retrieval_budget:
  max_retrieved_files: 5
  max_retrieved_chunks: 8
  max_chunk_chars: 1800
  max_total_context_chars: 12000
  prefer_same_repo: true
  prefer_same_language: true
  prefer_changed_file_neighbors: true
```

---

# 12. Bug-Fix and Defect Dataset References

Datasets in this section are **offline evaluation only** unless later approved in a separate training plan.

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Defect Datasets index | https://defect-datasets.github.io/ | Dataset discovery |
| 2 | Software Defect Prediction | https://www.kaggle.com/datasets/semustafacevik/software-defect-prediction | Offline defect prediction evaluation |
| 3 | Software Defect Prediction Dataset | https://www.kaggle.com/datasets/ziya07/software-defect-prediction-dataset | Offline evaluation |
| 4 | Bug Prediction Dataset | https://www.kaggle.com/datasets/syedzubair/bug-prediction-dataset | Offline evaluation |
| 5 | GHPR Dataset | https://github.com/feiwww/GHPR_dataset | Pull-request bug-fix dataset |
| 6 | BugsJS | https://github.com/BugsJS/bug-dataset | JavaScript bug benchmark |
| 7 | FixEval | https://github.com/mahimanzum/FixEval | Execution-based code repair evaluation |
| 8 | InferredBugs | https://github.com/microsoft/InferredBugs | Static-analysis derived bug/fix dataset |
| 9 | Software bug prediction | https://github.com/YousefGh/software_bug_prediction | Bug prediction reference |

Use for Opung:

```text
Offline evaluation.
Bug-fix pattern reference.
Error category enrichment.
Testing repair quality.
```

Restrictions:

```text
No direct patch generation authority.
No fine-tuning without cleaning plan.
Language filter required.
Not production truth source.
```

Suggested metadata:

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

---

# 13. Code Review Dataset References

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Code Review Data v2 | https://www.kaggle.com/datasets/bulivington/code-review-data-v2 | Code review data |
| 2 | Code Review Assistant | https://huggingface.co/datasets/alenphilip/Code-Review-Assistant | Review instruction dataset |
| 3 | RosaliaTufano code_review | https://github.com/RosaliaTufano/code_review | Code review research package |
| 4 | NAIST code review dataset list | https://naist-se.github.io/code-review/dataset/ | Code review dataset index |
| 5 | GHPR Dataset | https://github.com/feiwww/GHPR_dataset | Pull request and bug-fix examples |

Use for Opung:

```text
Patch note style.
Review comment style.
Learning how to explain small patch.
```

Restrictions:

```text
Opung is not final reviewer.
Senior Reviewer remains final authority.
Do not copy review text blindly.
Do not use synthetic data as factual evidence.
```

Suggested metadata:

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

---

# 14. StackOverflow and Q&A Datasets

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | StackLite | https://www.kaggle.com/datasets/stackoverflow/stacklite | Secondary Q&A retrieval |
| 2 | StackOverflow Python Questions | https://www.kaggle.com/datasets/stackoverflow/pythonquestions | Python error and Q&A examples |

Use for Opung:

```text
Secondary error-message enrichment.
Common exception context.
Common API usage confusion.
```

Restrictions:

```text
Official docs first.
StackOverflow datasets are noisy.
Do not treat Q&A as source of truth.
Do not copy obsolete fixes.
```

---

# 15. Software Engineering and Code Quality Datasets

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Software Engineering and Code Quality Dataset 2024 | https://www.kaggle.com/datasets/imaadmahmood/software-engineering-and-code-quality-dataset-2024 | Offline code quality evaluation |
| 2 | Clean Code Python | https://github.com/zedr/clean-code-python | Code quality reference |
| 3 | Code Review Assistant | https://huggingface.co/datasets/alenphilip/Code-Review-Assistant | Review style reference |

Use for Opung:

```text
Offline evaluation.
Patch note quality.
Small refactoring style reference.
```

Restrictions:

```text
No broad refactor.
No automatic code quality rewrite.
No final review authority.
```

---

# 16. Suggested Knowledge Routing

Suggested file:

```text
config/opung_knowledge_routing.yaml
```

```yaml
opung_knowledge_routing:
  "*.py":
    - Python official docs
    - Python standard library
    - PEP 8
    - pytest docs

  "tests/**/*.py":
    - pytest docs
    - pytest unittest integration
    - unittest.mock
    - pytest fixtures
    - pytest parametrization

  "app/api":
    - FastAPI docs
    - Pydantic docs
    - HTTP exception handling

  "app/retrieval":
    - Chroma docs
    - LangChain docs
    - Sentence Transformers docs
    - CodeSearchNetRetrieval

  "app/importers":
    - pathlib docs
    - json docs
    - csv docs
    - argparse docs

  "cli":
    - argparse docs
    - Typer docs
    - Click docs

  "bug_fix_task":
    - Python exceptions docs
    - GHPR Dataset
    - FixEval
    - CodeSearchNetRetrieval

  "code_review_note":
    - Code Review Assistant
    - RosaliaTufano code_review
    - NAIST code review dataset

  "repo_level_context":
    - RepoCoder
    - repo-level-codegen-papers
    - CodeSearchNetRetrieval

  "algorithm_helper":
    - TheAlgorithms Python
    - Python standard library algorithm modules

  "javascript_task":
    - MDN JavaScript
    - BugsJS
    - TheAlgorithms JavaScript

  "error:ModuleNotFoundError":
    - Python import system
    - Python exceptions

  "error:JSONDecodeError":
    - json docs
    - Python exceptions

  "error:ValidationError":
    - Pydantic errors
```

---

# 17. Suggested Chroma Collection

Collection:

```text
opung_coding_knowledge
```

Metadata for official docs:

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

Metadata for algorithm examples:

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

Metadata for API examples:

```json
{
  "agent": "opung",
  "source_type": "api_usage_reference",
  "allowed_use": "small_patch_guidance",
  "runtime_dependency": false,
  "requires_manifest_scope": true,
  "risk": "medium"
}
```

Metadata for bug-fix datasets:

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

Metadata for code review datasets:

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

Metadata for research references:

```json
{
  "agent": "opung",
  "source_type": "repo_level_codegen_research",
  "allowed_use": "design_pattern_only",
  "runtime_dependency": false,
  "risk": "low"
}
```

---

# 18. Suggested Local Files

```text
config/opung_knowledge_routing.yaml
config/opung_guardrails.yaml
data/agent_workspace/plans/
data/agent_workspace/patches/
data/agent_workspace/notes/
data/agent_workspace/errors/
data/agent_workspace/performance/
```

---

# 19. Opung Patch Policy

Allowed patch style:

```text
small
scoped
minimal
readable
testable
manifest-bound
```

Patch limits:

```yaml
opung_patch_limits:
  max_files_changed: 3
  max_lines_added: 180
  max_lines_removed: 80
  max_patch_bytes: 60000
```

Opung must stop if task needs:

```text
dependency change
architecture change
denied path
.env change
secret
shell command
broad refactor
production data
security-sensitive change
DevOps change
```

---

# 20. Ranking Referensi untuk Opung

| Priority | Reference | Value for Opung | Status |
|---:|---|---|---|
| 1 | Python official docs | Core language reference | Core knowledge |
| 2 | Python standard library docs | Built-in API usage | Core knowledge |
| 3 | pytest docs and unittest integration | Unit testing patterns | Core knowledge |
| 4 | Python exceptions docs | Error understanding | Core knowledge |
| 5 | CPython | Official source and stdlib reference | Core reference |
| 6 | CodeSearchNetRetrieval | Code retrieval benchmark | Core retrieval benchmark |
| 7 | RepoCoder | Repo-level context design | Design pattern |
| 8 | GHPR Dataset | Bug-fix pattern dataset | Offline evaluation |
| 9 | FixEval | Execution-based repair evaluation | Offline evaluation |
| 10 | Code Review Assistant | Review style and patch note | Supporting reference |
| 11 | RosaliaTufano code_review | Code review research package | Supporting reference |
| 12 | clean-code-python | Small refactor guidance | Supporting knowledge |
| 13 | TheAlgorithms Python | Algorithm examples | Educational only |
| 14 | BugsJS | JS bug benchmark | Conditional JS only |
| 15 | InferredBugs | Cross-language bug dataset | Research and evaluation |
| 16 | StackOverflow datasets | Error/Q&A context | Secondary, noisy |
| 17 | Software defect prediction datasets | Defect prediction evaluation | Offline only |
| 18 | repo-level-codegen-papers | Research roadmap | Research only |

---

# 21. Final Policy

Opung uses these links as **coding knowledge**, not as execution authority.

```text
Opung reads.
Opung plans.
Opung writes small draft patches.
Opung writes small tests if allowed.
Opung writes patch notes.
Opung does not execute.
Opung does not commit.
```

Hard boundary:

```text
No shell.
No apply patch.
No test execution.
No dependency install.
No commit.
No push.
No .env modification.
No secret access.
No broad refactor.
No invented API behavior.
No direct patch generation from dataset.
```
