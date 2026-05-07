# Senior Reviewer Knowledge Base Links

**Agent:** Senior Reviewer  
**Role:** final code reviewer, merge-readiness evaluator, maintainability auditor, static-analysis result interpreter, test-readiness reviewer, commit-request approver  
**Purpose:** selected knowledge base, tools, datasets, and references for senior-level code review in a local multi-agent workflow  
**Created:** 2026-05-07 14:25:11  
**Filename:** `SENIOR_REVIEWER_KNOWLEDGE_BASE_LINKS.md`

---

# 0. Status Dokumen

Dokumen ini adalah daftar knowledge base untuk **Senior Reviewer**.

Senior Reviewer berbeda dari Opung.

```text
Opung = membuat draft patch kecil
Senior Reviewer = memeriksa patch, risiko, kualitas, maintainability, test, static-analysis result, dan readiness sebelum Runner atau Commit Gate
```

Dokumen ini juga memilah referensi user menjadi:

```text
Core knowledge base
Optional knowledge base
Request-only tools
Dataset and benchmark
Conditional references
Rejected or low-priority references
```

Prinsip utama:

```text
Knowledge base = boleh dibaca
Static analysis = boleh diminta, tidak dijalankan langsung
Review decision = boleh dibuat
Execution = Runner
Validation = Verification Engine
Commit lokal = Commit Gate
Push / merge / release = Human Owner
```

---

# 1. Fungsi Knowledge Base Senior Reviewer

Senior Reviewer memakai knowledge base ini untuk:

```text
membaca standar code review
membuat review final
mengecek logic bug
mengecek error handling
mengecek logging
mengecek maintainability
mengecek test adequacy
membaca hasil static analysis
membaca hasil linter
membaca hasil coverage
membaca hasil security review Asep
membaca hasil DevOps review Doni
membaca patch Opung
membuat merge-readiness decision
membuat commit request untuk Commit Gate
```

Senior Reviewer tidak boleh memakai knowledge base ini sebagai izin untuk:

```text
apply patch sendiri
run shell
run CodeQL sendiri
run Semgrep sendiri
run Sonar sendiri
run tests sendiri
git commit sendiri
git push
git merge
bypass Safety Gate
bypass Verification Engine
bypass Human Owner
```

---

# 2. Core Base Knowledge untuk Senior Reviewer

| Domain | Isi yang perlu dipahami | Fungsi Senior Reviewer |
|---|---|---|
| Code review standard | Correctness, code health, readability, maintainability, tests | Menentukan apakah patch layak lanjut |
| PR checklist | Scope, risk, test, docs, backward compatibility, migration | Review final sebelum apply atau commit |
| Secure code review | Input validation, auth, authorization, secrets, crypto | Review awal, lalu eskalasi ke Asep jika perlu |
| Static analysis | CodeQL, Semgrep, SonarQube, Super-Linter, MegaLinter | Membaca hasil dan meminta validasi |
| Maintainability | Code smell, long method, large class, duplicate code, SOLID | Mendeteksi patch yang menambah technical debt |
| Refactoring | Extract method, reduce duplication, simplify condition | Menilai apakah refactor kecil layak |
| Test review | Unit test, coverage, regression test, edge case | Menentukan apakah test cukup |
| Merge readiness | Safety, verification, docs, risk, reviewer approval | Membuat keputusan commit request |
| SARIF/result parsing | Static analysis result format, severity, confidence | Membaca output tools secara terstruktur |
| Dataset and benchmarks | PR comments, defect prediction, code quality datasets | Offline evaluation only |

---

# 3. Optimistic Analysis

Jika referensi dipakai dengan benar, Senior Reviewer bisa menjadi agent yang sangat penting karena:

```text
1. Opung membuat patch kecil.
2. Senior Reviewer menguji kelayakan patch secara konseptual.
3. Asep menangani security yang lebih dalam.
4. Doni menangani DevOps dan deployment risk.
5. Verification Engine membuktikan hasil melalui check deterministik.
6. Commit Gate hanya berjalan jika Senior Reviewer dan Verification Engine setuju.
```

Skenario optimis:

```text
Patch kecil dari Opung
  ↓
Senior Reviewer membaca diff
  ↓
Senior Reviewer cocokkan dengan checklist
  ↓
Senior Reviewer baca hasil Asep/Doni jika ada
  ↓
Senior Reviewer minta static-analysis jika perlu
  ↓
Senior Reviewer approve final patch
  ↓
Runner apply patch
  ↓
Verification Engine PASS
  ↓
Commit Gate local commit
```

Value utama:

```text
mengurangi bug logic
mencegah over-refactor
mencegah patch yang terlalu luas
menjaga code health
mengurangi false confidence dari model kecil
membuat commit request lebih ketat
```

---

# 4. Failure-First Analysis

Risiko terbesar Senior Reviewer adalah terlalu percaya diri.

Failure modes:

| Failure | Contoh | Dampak | Mitigasi |
|---|---|---|---|
| Rubber stamp | Semua patch dianggap OK | Bug masuk | Checklist wajib |
| Overrule specialist | Mengabaikan Asep/Doni | Security atau deployment risk | Specialist review precedence |
| Tool worship | Menganggap Semgrep PASS berarti aman | False negative | Tool result bukan bukti mutlak |
| Over-refactor | Meminta refactor besar | Scope creep | Patch scope limit |
| Style nitpicking | Blokir patch karena preferensi minor | Workflow lambat | Separate blocking vs non-blocking |
| Dataset overtrust | Menganggap dataset PR comments sebagai truth | Review generik | Dataset offline only |
| Static analysis false positive | Alert minor dianggap blocker | Delay | Severity and evidence gate |
| Static analysis false negative | Tidak ada alert dianggap aman | Bug lolos | Manual review tetap wajib |
| Merge without test | Approve tanpa verification | Runtime failure | Verification Engine mandatory |
| Commit bypass | Commit tanpa Safety Gate | Risk | Commit Gate strict requirements |

Final failure-first rule:

```text
Senior Reviewer may approve.
Senior Reviewer may request revision.
Senior Reviewer may request validation.
Senior Reviewer may request commit.
Senior Reviewer must not execute, commit, push, or merge.
```

---

# 5. Code Review Checklist Knowledge Base

## 5.1 Core Selected References

| No | Source | Link | Status | Use |
|---:|---|---|---|---|
| 1 | Michaela Greiler Code Review Checklist | https://github.com/mgreiler/code-review-checklist | Core | Logic, error handling, logging, dependencies, security, performance, usability, maintainability |
| 2 | Awesome Code Review Checklists | https://github.com/mgreiler/awesome-code-review-checklists | Core index | Curated code review checklists |
| 3 | Google Engineering Practices Code Review Standard | https://google.github.io/eng-practices/review/reviewer/standard.html | Core | Review philosophy and code health |
| 4 | Google Code Review Guide | https://google.github.io/eng-practices/review/reviewer/ | Core | How to review code |
| 5 | Software Engineering at Google, Code Review chapter | https://abseil.io/resources/swe-book/html/ch09.html | Core | Code review role separation |
| 6 | Secure Code Review Checklist | https://github.com/softwaresecured/secure-code-review-checklist | Core with Asep route | Security-focused review prompts |
| 7 | Code Review Checklist website | https://www.codereviewchecklist.com/ | Optional core | Human-readable checklist |
| 8 | Pull Request Checklist GitHub | https://www.pullchecklist.com/posts/pull-request-checklist-github | Optional | PR checklist pattern |

Use for Senior Reviewer:

```text
Review implementation correctness.
Review error handling.
Review logging.
Review dependencies.
Review test sufficiency.
Review maintainability.
Review performance impact.
Review security trigger before escalating to Asep.
```

---

## 5.2 Conditional Checklist References

| No | Source | Link | Status | Use |
|---:|---|---|---|---|
| 1 | Solidity Labs Code Review Checklist | https://github.com/solidity-labs-io/code-review-checklist | Conditional | Solidity / smart contract only |
| 2 | UiPath Code Review Checklist | https://github.com/seymenbahtiyar/UiPath_Code_Review_Checklist | Conditional | UiPath only |
| 3 | C++ Code Review Checklist | https://github.com/swomack/cpp-code-review-checklist | Conditional | C++ only |
| 4 | Frontend PR Checklist | https://github.com/sapegin/frontend-pull-request-checklist | Conditional | Frontend only |
| 5 | W3C ARIA PR Review Checklist | https://github.com/w3c/aria-practices/wiki/Pull-Request-Review-Checklist | Conditional | Accessibility docs / ARIA only |
| 6 | Vue code review checklist topic | https://github.com/topics/code-review-checklist?l=vue | Discovery only | Vue-specific discovery |
| 7 | Code review gist | https://gist.github.com/katyhuff/845e06656f18784210190e4f46a4aa95 | Secondary | Checklist example |
| 8 | ParadiseSS13 discussion | https://github.com/ParadiseSS13/Paradise/discussions/21968 | Low priority | Community discussion only |

Rule:

```text
Conditional references are loaded only when file type or task domain matches.
```

---

## 5.3 Excluded or Low-Priority Checklist References

| Source | Reason |
|---|---|
| Broken link `knonm/code-review-checklis thttps...` | URL malformed |
| Medium PR checklist articles | Useful for ideas, not core authority |
| dev.to guide | Secondary article |
| ResearchGate figure with sample comments | Visual sample only, not base policy |
| Medium example code review | Example only |

---

# 6. Static Analysis and Rule-Based Review

## 6.1 Core Selected Tools and References

| No | Tool / Source | Link | Status | Use |
|---:|---|---|---|---|
| 1 | CodeQL official | https://codeql.github.com/ | Core request-only | Semantic code analysis |
| 2 | CodeQL GitHub | https://github.com/github/codeql | Core request-only | CodeQL libraries and queries |
| 3 | CodeQL action | https://github.com/github/codeql-action | Core request-only | CI integration |
| 4 | Semgrep | https://github.com/semgrep/semgrep | Core request-only | Static analysis, bug and secure guardrail rules |
| 5 | Semgrep Rules | https://github.com/semgrep/semgrep-rules | Core request-only | Community rules |
| 6 | Semgrep docs overview | https://semgrep.dev/docs/semgrep-code/overview | Core request-only | Semgrep capabilities and config |
| 7 | Sonar custom rules examples | https://github.com/SonarSource/sonar-custom-rules-examples | Optional request-only | Custom quality rules |
| 8 | SonarQube Quality Gate Action | https://github.com/SonarSource/sonarqube-quality-gate-action | Optional request-only | Quality gate result |
| 9 | Super-Linter | https://github.com/super-linter/super-linter | Optional request-only | Multi-language linting |
| 10 | MegaLinter | https://github.com/oxsecurity/megalinter | Optional request-only | Multi-language linting and code quality |
| 11 | MegaLinter docs / action | https://github.com/marketplace/actions/megalinter | Optional request-only | CI linting reference |
| 12 | github/semantic | https://github.com/github/semantic | Research / future | Parse, analyze, compare source code |

Senior Reviewer use:

```text
Request static analysis.
Read static analysis report.
Classify findings as blocker or non-blocker.
Route security findings to Asep.
Route DevOps findings to Doni.
Never run the tool directly.
```

---

## 6.2 Static Analysis Index and Discovery References

| No | Source | Link | Status | Use |
|---:|---|---|---|---|
| 1 | awesome-static-analysis | https://github.com/satishpatnayak/awesome-static-analysis | Discovery | Static analysis tool catalog |
| 2 | analysis-tools-dev/static-analysis | https://github.com/analysis-tools-dev/static-analysis | Discovery | Static analysis catalog |
| 3 | awesome-security static analysis | https://github.com/awesome-security/awesome-static-analysis | Discovery | Security-focused static analysis tools |
| 4 | lukehutch awesome static analysis | https://github.com/lukehutch/awesome-static-analysis | Discovery | Tool discovery |
| 5 | GitHub static-analyzer topic | https://github.com/topics/static-analyzer | Discovery | Tool discovery |
| 6 | GitHub semantic-analysis topic | https://github.com/topics/semantic-analysis?o=asc&s=updated | Discovery | Research discovery |
| 7 | glob-linters | https://github.com/bowentan/glob-linters | Optional | Linter collection |
| 8 | mega-linter legacy | https://github.com/jlongman/mega-linter | Low priority | Prefer oxsecurity/megalinter |

Rule:

```text
Discovery lists are not runtime dependencies.
Only selected tools enter request-only tool policy.
```

---

## 6.3 Static Analysis Request Policy

Senior Reviewer can request:

```yaml
senior_static_analysis_requests:
  allow:
    - request_codeql_analysis
    - request_semgrep_scan
    - request_sonarqube_quality_gate
    - request_super_linter
    - request_megalinter
    - request_sarif_parse
    - request_duplicate_code_check
    - request_complexity_check
```

Senior Reviewer cannot run:

```yaml
senior_static_analysis_execution:
  deny:
    - codeql_database_create
    - codeql_analyze_direct
    - semgrep_run_direct
    - sonar_scanner_direct
    - super_linter_direct
    - megalinter_direct
    - arbitrary_linter_direct
```

---

# 7. Maintainability, Refactoring, Code Smell, and Technical Debt

## 7.1 Core Selected References

| No | Source | Link | Status | Use |
|---:|---|---|---|---|
| 1 | Martin Fowler Code Smell | https://martinfowler.com/bliki/CodeSmell.html | Core | Definition of code smell |
| 2 | Refactoring Guru Code Smells | https://refactoring.guru/refactoring/smells | Core | Code smell catalog |
| 3 | Refactoring Guru Long Method | https://refactoring.guru/smells/long-method | Core | Long method smell |
| 4 | Refactoring Guru Large Class | https://refactoring.guru/smells/large-class | Core | Large class smell |
| 5 | Refactoring Guru Duplicate Code | https://refactoring.guru/smells/duplicate-code | Core | Duplicate code smell |
| 6 | Refactoring Guru Refactoring Catalog | https://refactoring.guru/refactoring/catalog | Core | Refactoring techniques |
| 7 | CodelyTV refactoring code smells design patterns | https://github.com/CodelyTV/refactoring-code_smells-design_patterns | Optional | Learning reference |
| 8 | Awesome Refactoring | https://github.com/faradaj/awesome-refactoring | Discovery | Refactoring resources |
| 9 | DigitalOcean SOLID article | https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design | Supporting | SOLID explanation |
| 10 | GeeksForGeeks SOLID | https://www.geeksforgeeks.org/system-design/solid-principle-in-programming-understand-with-real-life-examples/ | Supporting | SOLID examples |
| 11 | PhpMetrics metrics | https://github.com/phpmetrics/PhpMetrics/blob/master/doc/metrics.md | Conditional | PHP metrics reference |

Use:

```text
Identify maintainability blockers.
Separate refactor suggestion from patch blocker.
Reject broad refactor request unless manifest allows.
Use duplicate code and long method as review signals, not absolute blockers.
```

---

## 7.2 Technical Debt References

| No | Source | Link | Status | Use |
|---:|---|---|---|---|
| 1 | GitHub technical-debt topic | https://github.com/topics/technical-debt | Discovery | Tool discovery |
| 2 | TechnicalDebtRecords | https://github.com/ms1963/TechnicalDebtRecords | Optional | Technical debt records |
| 3 | Tech Debt Skill | https://github.com/fastruby/tech-debt-skill | Optional | Technical debt tracking concept |
| 4 | TechDebt Tracker | https://github.com/Forward-Lang/TechDebt-Tracker | Optional | Tracker concept |
| 5 | Technical Debt Management Toolbox | https://github.com/AngelikiTsintzira/Technical-Debt-Management-Toolbox | Optional | Management toolbox |
| 6 | Security debt topic | https://github.com/topics/security-debt | Discovery | Security debt discovery |
| 7 | SWQD maintainability prediction | https://github.com/simonzachau/SWQD-predict-software-maintainability | Research | Maintainability prediction |
| 8 | Maintenance prediction | https://github.com/rishabhjainps/Maintenance-prediction | Research | Maintenance prediction |

Rule:

```text
Technical debt references support review notes.
They do not justify broad refactor in a small patch.
```

---

## 7.3 Duplicate Code Detection References

| No | Source | Link | Status | Use |
|---:|---|---|---|---|
| 1 | duplicate-code-detection-tool | https://github.com/platisd/duplicate-code-detection-tool | Optional request-only | Duplicate code detection |
| 2 | IBM duplicate code concepts PDF | https://www.ibm.com/docs/SSQ2R2_14.2.0/dupcodedetect/pdf/dupcodedetect_concepts.pdf | Supporting | Concepts |
| 3 | Duplicate Code Detection Using Anti-Unification | https://www.researchgate.net/publication/228376674_Duplicate_Code_Detection_Using_Anti-Unification | Research | Duplicate detection theory |
| 4 | GitHub code-duplication topic | https://github.com/topics/code-duplication | Discovery | Tool discovery |

Rule:

```text
Duplicate detection is request-only.
Do not block patch only because duplicate exists unless it worsens maintainability materially.
```

---

## 7.4 Low-Priority Maintainability References

| Source | Reason |
|---|---|
| Medium long method / large class articles | Secondary commentary only |
| ResearchGate figure distributions | Dataset or illustration only |
| Lecturer PDF for large/god class | Educational only |
| CDC stack reference | Not directly relevant to local reviewer |
| Generic GitHub topic pages | Discovery only |

---

# 8. Security Review Boundary

Senior Reviewer can detect security triggers, but Asep owns deep security review.

Senior Reviewer may identify:

```text
hardcoded secrets
unsafe deserialization
injection risk
path traversal risk
missing authorization check
weak error handling
sensitive data logging
insecure dependency change
dangerous file operation
```

If found:

```text
route_to = Asep
decision = needs_security_review
```

Senior Reviewer must not replace Asep.

Core security references used by Senior Reviewer:

| Source | Link | Use |
|---|---|---|
| Secure Code Review Checklist | https://github.com/softwaresecured/secure-code-review-checklist | Security prompts |
| CodeQL | https://codeql.github.com/ | Semantic security analysis request |
| Semgrep Rules | https://github.com/semgrep/semgrep-rules | Rule-based security analysis request |
| OWASP Cheat Sheet Series | https://github.com/OWASP/CheatSheetSeries | Secure coding reference, routed through Asep |

---

# 9. Tool Selection for Senior Reviewer

## 9.1 Agent-Facing Tools

Senior Reviewer may directly use:

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
    - retrieve_code_review_reference
    - retrieve_maintainability_reference
    - retrieve_static_analysis_reference
    - write_senior_review
    - write_revision_request
    - write_final_patch_decision
    - write_apply_approval
    - write_commit_request
```

## 9.2 Denied Tools

```yaml
senior_reviewer_tools:
  deny:
    - run_shell
    - apply_patch
    - run_tests
    - install_dependency
    - codeql_run_direct
    - semgrep_run_direct
    - sonar_run_direct
    - linter_run_direct
    - modify_env
    - read_secret
    - git_commit
    - git_push
    - git_merge
    - git_rebase
    - delete_file
    - deploy
```

## 9.3 Request-Only Tools

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

# 10. Dataset and Benchmark References

These references are **offline evaluation only**.

| No | Dataset / Source | Link | Status | Use |
|---:|---|---|---|---|
| 1 | GitHub Public Pull Request Comments | https://www.kaggle.com/datasets/pelmers/github-public-pull-request-comments | Optional | Review comment style benchmark |
| 2 | Software Defect Prediction | https://www.kaggle.com/datasets/semustafacevik/software-defect-prediction | Offline | Bug-risk evaluation |
| 3 | Software Engineering and Code Quality Dataset 2024 | https://www.kaggle.com/datasets/imaadmahmood/software-engineering-and-code-quality-dataset-2024 | Offline | Code quality evaluation |
| 4 | Code Review Data v2 | https://www.kaggle.com/datasets/bulivington/code-review-data-v2 | Offline | Review comment benchmark |
| 5 | NAIST Code Review Dataset Index | https://naist-se.github.io/code-review/dataset/ | Research index | Dataset discovery |
| 6 | ResearchGate code review comments example | https://www.researchgate.net/figure/Examples-of-code-review-comments-included-in-our-survey_fig2_375831008 | Secondary | Example only |

Rules:

```text
Dataset cannot approve or reject patch.
Dataset cannot replace human-style review rubric.
Dataset cannot become production truth source.
Dataset is for offline evaluation and prompt calibration only.
```

---

# 11. Knowledge Routing

Suggested file:

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

# 12. Suggested Chroma Collection

Collection:

```text
senior_reviewer_knowledge
```

Metadata for core review guidance:

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

Metadata for static analysis tools:

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

Metadata for maintainability references:

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

Metadata for datasets:

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

# 13. Suggested Local Files

```text
config/senior_reviewer_knowledge_routing.yaml
config/senior_reviewer_guardrails.yaml
data/agent_workspace/reviews/
data/agent_workspace/reviews/senior/
data/agent_workspace/revision_requests/
data/agent_workspace/approvals/
data/agent_workspace/requests/
data/agent_workspace/errors/
data/agent_workspace/performance/
knowledge-base/reviewer-senior-programmer/
  checklists/
  rules/
  templates/
  datasets/
  policies/
```

---

# 14. Ranking Referensi untuk Senior Reviewer

| Priority | Reference | Value | Status |
|---:|---|---|---|
| 1 | Google Code Review Standard | Review philosophy and code health | Core |
| 2 | mgreiler Code Review Checklist | Practical checklist | Core |
| 3 | Google Code Review Guide | Reviewer process | Core |
| 4 | CodeQL | Semantic static analysis | Request-only core |
| 5 | Semgrep and Semgrep Rules | Rule-based review and security guardrails | Request-only core |
| 6 | SonarQube Quality Gate | Quality gate result | Optional request-only |
| 7 | Super-Linter / MegaLinter | Multi-language lint | Optional request-only |
| 8 | Martin Fowler Code Smell | Code smell concept | Core |
| 9 | Refactoring Guru Code Smells | Maintainability catalog | Core |
| 10 | Refactoring Guru Refactoring Catalog | Refactor guidance | Core |
| 11 | Secure Code Review Checklist | Security trigger checklist | Core with Asep route |
| 12 | Duplicate Code Detection Tool | Duplicate code support | Optional request-only |
| 13 | SOLID references | Maintainability principle | Supporting |
| 14 | Technical debt trackers | Debt documentation pattern | Optional |
| 15 | Code review datasets | Offline evaluation | Offline only |
| 16 | Medium/dev.to articles | Secondary ideas | Low priority |
| 17 | Domain-specific checklists | Conditional only | Conditional |
| 18 | GitHub topic pages | Discovery only | Discovery |

---

# 15. Final Policy

Senior Reviewer uses these links as **review knowledge**, not as execution authority.

```text
Senior Reviewer reads.
Senior Reviewer evaluates.
Senior Reviewer requests validation.
Senior Reviewer writes final review.
Senior Reviewer can approve apply request.
Senior Reviewer can write commit request.
Senior Reviewer does not execute.
```

Hard boundary:

```text
No shell.
No apply patch.
No test execution.
No direct static-analysis execution.
No dependency install.
No commit.
No push.
No merge.
No .env access.
No secret access.
No deployment.
```
