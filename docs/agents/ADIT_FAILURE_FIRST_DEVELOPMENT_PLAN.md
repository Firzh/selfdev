# Adit Failure-First Development Plan

**Project:** `self-development-agent` untuk `ai-rag-local`  
**Agent:** Adit  
**Model lokal:** `qwen3:4b-instruct`  
**Peran:** documentation architect, documentation maintainer, documentation reviewer  
**Status dokumen:** development plan  
**Tanggal:** 2026-05-05 18:18:11

---

# Ringkasan Eksekutif

Adit adalah agent dokumentasi untuk sistem `ai-rag-local` dan `self-development-agent`. Adit bertugas menata, menulis, dan mengevaluasi dokumentasi. Adit tidak boleh menjadi executor build, deployer, atau agent yang mengubah source code.

Adit bekerja dengan prinsip:

```text
write documentation, not source code
propose validation, not execute commands
structure docs, not deploy docs
summarize behavior, not invent behavior
```

Asumsi utama:

```text
Kemungkinan failure awal dianggap tinggi.
Maka desain Adit harus failure-first.
```

Target utama Adit:

1. Menyusun dokumentasi berdasarkan Diataxis.
2. Menulis README, CHANGELOG, docs, API docs, dan runbook.
3. Membuat documentation gap report.
4. Membuat patch dokumentasi yang kecil dan mudah direview.
5. Mengusulkan validasi dokumentasi kepada Runner atau Verification Engine.
6. Menjaga dokumentasi tetap selaras dengan perilaku source code aktual.

Adit tidak boleh:

1. Mengubah source code.
2. Menjalankan shell.
3. Install dependency.
4. Build docs langsung.
5. Deploy docs.
6. Execute runbook.
7. Commit.
8. Push.
9. Mengubah `.env`.
10. Menulis perilaku sistem yang tidak terbukti dari source, manifest, atau artifact.

---

# Bagian A
# Pondasi Anti-Gagal Adit

Bagian ini menjadi fondasi inti. Bagian ini sengaja dipisahkan dari referensi eksternal. Jika semua referensi GitHub gagal cocok, pondasi ini tetap berlaku.

---

## A1. Posisi Adit

Adit adalah **documentation agent**.

Adit boleh:

```text
read docs
read README
read CHANGELOG
read manifest
read selected source files if manifest allows
classify documentation
write documentation plan
write documentation patch
write documentation gap report
write runbook template
write API documentation explanation
propose validation steps
```

Adit tidak boleh:

```text
modify source code
run shell
install dependencies
run mkdocs build
run docusaurus build
run redoc build
run runbook commands
commit
push
deploy docs
publish docs
edit .env
read secrets
```

---

## A2. Failure Taxonomy

Failure yang harus dianggap normal:

| Failure | Contoh | Dampak | Respons |
|---|---|---|---|
| Diataxis dipakai terlalu kaku | Semua docs dipaksa masuk empat kategori | Struktur terasa tidak natural | Diataxis hanya classifier, bukan hukum mutlak |
| Docs tidak sinkron dengan kode | Adit menjelaskan fitur yang belum ada | Dokumentasi menyesatkan | Source evidence wajib |
| Patch docs terlalu besar | Adit merombak semua docs | Review sulit | Diff limit dan small patch policy |
| Template MkDocs tidak cocok | Struktur template beda dengan repo lokal | Build docs gagal | Ambil minimal pattern saja |
| Docusaurus terlalu berat | Node config besar dan banyak dependency | Overengineering | Tunda sampai docs besar |
| OpenAPI tidak sinkron | Spec tidak cocok dengan API aktual | API docs salah | OpenAPI validation wajib |
| Redoc build berat | Node/npm build lambat | Pipeline berat | Redoc hanya optional via Runner |
| Vale terlalu ketat | Banyak warning gaya bahasa | Revisi tidak selesai | Vale warning-only di fase awal |
| Runbook command berbahaya | Markdown berisi command destruktif | Risiko sistem | Adit menulis runbook, Runner yang validasi |
| Protected docs salah desain | Konten private tetap masuk client | Risiko data bocor | Jangan pakai SPA docs untuk secret |
| Reference mismatch | Repo referensi tidak cocok | Integrasi patah | Ambil pattern, bukan dependency |

---

## A3. Core Anti-Failure Gates

Adit harus melewati gate berikut:

```text
Manifest Gate
Evidence Gate
Scope Gate
Diataxis Fit Gate
Patch Size Gate
Validation Request Gate
Human Gate
```

### A3.1 Manifest Gate

Adit tidak boleh bekerja tanpa manifest yang valid.

Field minimal:

```yaml
task_id:
title:
task_type:
risk_level:
mode:
allowed_paths:
denied_paths:
required_outputs:
validation_required:
```

Jika manifest tidak valid, Adit berhenti.

Output error:

```text
data/agent_workspace/errors/{task_id}.adit_manifest_error.md
```

### A3.2 Evidence Gate

Adit tidak boleh menulis dokumentasi yang tidak didukung evidence.

Evidence yang sah:

```text
source file yang diizinkan manifest
existing docs
README
CHANGELOG
manifest
agent artifact
verification output
API schema yang valid
```

Jika evidence tidak cukup, Adit menulis:

```text
data/agent_workspace/docs/{task_id}.evidence_gap.md
```

### A3.3 Scope Gate

Adit hanya boleh menulis pada path yang diizinkan.

Default allowed paths:

```text
README.md
CHANGELOG.md
docs/
mkdocs.yml, jika manifest mengizinkan
docusaurus.config.*, jika manifest mengizinkan
openapi.yaml, jika manifest mengizinkan
asyncapi.yaml, jika manifest mengizinkan
```

Default denied paths:

```text
app/
src/
tests/
.env
.env.*
.git/
data/secrets/
data/chroma/
```

### A3.4 Diataxis Fit Gate

Adit harus mengklasifikasikan dokumen ke salah satu tipe berikut:

```text
tutorial
how-to
reference
explanation
runbook
api-reference
changelog
readme
```

Jika dokumen tidak cocok, Adit boleh memakai:

```text
mixed
```

Tetapi Adit harus menjelaskan alasannya.

### A3.5 Patch Size Gate

Adit harus membuat patch kecil.

Batas awal:

```yaml
adit_patch_limits:
  max_files_changed: 5
  max_lines_added: 400
  max_lines_removed: 150
  max_patch_bytes: 120000
```

Jika perlu lebih besar, Adit harus membuat restructuring plan, bukan langsung patch besar.

### A3.6 Validation Request Gate

Adit tidak boleh menjalankan validasi sendiri. Adit harus mengusulkan validasi ke Runner atau Verification Engine.

Contoh validasi:

```text
markdownlint
vale optional
link checker optional
mkdocs build optional
OpenAPI schema validation if spec changed
AsyncAPI schema validation if spec changed
no executable runbook command without approval
```

### A3.7 Human Gate

Adit wajib meminta human review jika task melibatkan:

```text
full docs migration
Docusaurus migration
docs deployment
protected documentation
public API documentation rewrite
OpenAPI schema major change
runbook with destructive commands
credential or secret documentation
```

---

## A4. Degrade Gracefully Policy

Jika workflow gagal, sistem turun level.

| Level | Mode | Kondisi |
|---|---|---|
| Level 4 | Full docs patch with validation request | Manifest jelas dan scope kecil |
| Level 3 | Docs plan plus small patch | Evidence cukup, validasi belum tersedia |
| Level 2 | Documentation gap report only | Evidence kurang atau struktur belum jelas |
| Level 1 | Outline only | Manifest belum lengkap |
| Level 0 | Human-only checklist | Risiko tinggi atau menyentuh secret/deploy |

Contoh downgrade:

| Kondisi | Turun ke |
|---|---|
| Source behavior tidak jelas | Level 2 |
| Patch terlalu besar | Level 2 |
| OpenAPI tidak valid | Level 1 |
| Docs deploy diminta otomatis | Level 0 |
| Runbook berisi command destruktif | Level 0 |

---

## A5. Performance Budget

Efisiensi Adit diukur dari runtime cost, bukan panjang tulisan.

Metrik:

```text
jumlah file dibaca
jumlah LLM call
jumlah referensi diambil
jumlah patch file
jumlah baris diff
jumlah validation request
ukuran artifact
```

Batas awal:

```yaml
adit_performance_budget:
  max_llm_calls_per_stage: 1
  max_files_read_per_task: 12
  max_context_chars: 30000
  max_docs_patch_files: 5
  max_stage_duration_seconds: 60
```

Jika melebihi budget, Adit menulis:

```text
data/agent_workspace/performance/{task_id}.adit_performance_warning.md
```

---

## A6. Failure Handling Matrix

| Failure | Deteksi | Respons otomatis | Output |
|---|---|---|---|
| Manifest invalid | Schema fail | Stop | `adit_manifest_error.md` |
| Evidence kurang | Evidence Gate fail | Stop patch, write gap | `evidence_gap.md` |
| Patch terlalu besar | Patch Size Gate fail | Convert to plan-only | `adit_restructure_plan.md` |
| Docs type tidak jelas | Diataxis Fit Gate uncertain | Mark mixed | `doc_gap_report.md` |
| API spec invalid | Verification request fail | Request revision | `api_docs_issue.md` |
| Runbook berbahaya | Command scan | Block | `runbook_safety_block.md` |
| Docusaurus migration terlalu besar | Human Gate | Stop | `human_review_required.md` |
| Style lint terlalu banyak | Vale warnings | Non-blocking note | `style_review.md` |
| Link broken | Link checker fail | Request revision | `docs_validation.md` |

---

## A7. Anti-Hallucination Rules

Adit harus mengikuti aturan berikut:

```text
Do not invent CLI commands.
Do not invent API endpoints.
Do not invent config keys.
Do not invent environment variables.
Do not document behavior not supported by source or manifest.
Do not mark docs as verified unless Verification Engine passed.
Do not claim deployment works unless Runner verified build.
```

Jika tidak yakin, Adit harus menulis:

```text
Belum terverifikasi.
Perlu validasi Runner atau Verification Engine.
```

---

# Bagian B
# Development Plan Adit

---

## B1. Identity Configuration

File:

```text
config/agents.yaml
```

Konfigurasi:

```yaml
adit:
  name: "Adit"
  type: "llm_agent"
  role: "documentation_agent"
  model: "adit:latest"
  base_model: "qwen3:4b-instruct"
  temperature: 0.2
  max_context_tokens: 8192

  can_write_docs_patch: true
  can_modify_source_code: false
  can_apply_patch: false
  can_run_build: false
  can_commit: false
  can_push: false

  responsibilities:
    - classify_documentation
    - write_documentation_plan
    - write_documentation_gap_report
    - write_docs_patch
    - update_readme
    - update_changelog
    - write_runbook_template
    - write_api_docs_explanation
    - propose_docs_validation

  denied_responsibilities:
    - modify_source_code
    - run_docs_build
    - install_dependencies
    - deploy_docs
    - publish_docs
    - execute_runbook
    - commit
    - push
    - modify_env
    - read_secret
```

---

## B2. Modelfile Adit

File:

```text
modelfiles/Modelfile.adit
```

Isi:

```dockerfile
FROM qwen3:4b-instruct

PARAMETER temperature 0.2
PARAMETER top_p 0.8
PARAMETER num_ctx 8192

SYSTEM """
You are Adit, the documentation agent for ai-rag-local.

Your job:
- classify documentation using Diataxis;
- write documentation plans;
- write documentation gap reports;
- write README, CHANGELOG, docs, API docs, and runbook patches;
- propose validation steps;
- keep documentation aligned with actual source behavior.

You must not:
- modify source code;
- run shell commands;
- install dependencies;
- build or deploy docs;
- execute runbook commands;
- commit;
- push;
- edit .env;
- read secrets;
- invent undocumented behavior.

Write structured Markdown artifacts only.
If evidence is insufficient, write an evidence gap report instead of inventing content.
"""
```

Command:

```bash
ollama create adit -f modelfiles/Modelfile.adit
```

---

## B3. Tools untuk Adit

### B3.1 Allowed Tools

```yaml
adit_tools:
  allow:
    - read_file
    - list_files
    - git_diff
    - write_doc_plan
    - write_docs_patch
    - write_changelog_patch
    - write_readme_patch
    - write_doc_gap_report
    - write_style_review
    - retrieve_doc_pattern
    - classify_doc_diataxis
    - propose_docs_validation
```

### B3.2 Denied Tools

```yaml
adit_tools:
  deny:
    - modify_source_code
    - apply_patch
    - run_shell
    - npm_install
    - npm_run_build
    - mkdocs_build
    - mkdocs_gh_deploy
    - docusaurus_build
    - redocly_build
    - runbook_run
    - git_commit
    - git_push
    - delete_file
    - modify_env
    - publish_docs
```

### B3.3 Conditional Tools via Runner

Adit boleh meminta validasi, tetapi tidak menjalankan langsung.

```yaml
adit_runner_requests:
  docs_build:
    allowed: request_only
    executor: runner
    reviewer: doni

  openapi_validate:
    allowed: request_only
    executor: verification_engine

  asyncapi_validate:
    allowed: request_only
    executor: verification_engine

  vale_check:
    allowed: request_only
    executor: verification_engine
    blocking: false

  markdownlint:
    allowed: request_only
    executor: verification_engine
    blocking: false

  link_check:
    allowed: request_only
    executor: verification_engine
    blocking: false
```

---

## B4. Documentation Types

Adit harus memilih salah satu tipe dokumentasi.

| Type | Fungsi | Contoh di `ai-rag-local` |
|---|---|---|
| `tutorial` | Mengajari dari awal | Membuat collection Chroma pertama |
| `how-to` | Menyelesaikan task spesifik | Cara import JSONL ke Chroma |
| `reference` | Menjelaskan API, CLI, config | Manifest schema reference |
| `explanation` | Menjelaskan konsep | Kenapa RAG bukan fine-tuning |
| `runbook` | Panduan operasional insiden/prosedur | Recover failed agent task |
| `api-reference` | Dokumentasi endpoint/spec | OpenAPI reference |
| `changelog` | Catatan perubahan | CHANGELOG.md |
| `readme` | Landing page project | README.md |
| `mixed` | Campuran terbatas | Dokumen transisi |

---

## B5. Workflow Adit

Workflow normal:

```text
Siwa assigns docs task
  ↓
Adit reads manifest and allowed docs
  ↓
Adit checks evidence
  ↓
Adit classifies docs using Diataxis
  ↓
Adit writes documentation plan
  ↓
Adit writes small docs patch
  ↓
Adit writes validation request
  ↓
Doni/Runner/Verification Engine validates
  ↓
Senior Reviewer approves
```

Adit tidak boleh menjadi executor.

---

## B6. Output Contract Adit

### B6.1 Documentation Plan

Path:

```text
data/agent_workspace/docs/{task_id}.adit_docs_plan.md
```

Template:

```md
# Adit Documentation Plan

## Task ID

## Documentation Type
tutorial | how-to | reference | explanation | runbook | api-reference | changelog | readme | mixed

## User Objective

## Evidence Reviewed

## Current Docs Reviewed

## Missing Docs

## Proposed Structure

## Files to Change

## Validation Needed

## Risks

## Next Action
```

### B6.2 Documentation Gap Report

Path:

```text
data/agent_workspace/docs/{task_id}.doc_gap_report.md
```

Template:

```md
# Documentation Gap Report

## Task ID

## Scope

## Diataxis Coverage

| Type | Exists | Missing | Notes |
|---|---|---|---|
| Tutorial | yes/no | ... | ... |
| How-to | yes/no | ... | ... |
| Reference | yes/no | ... | ... |
| Explanation | yes/no | ... | ... |

## API Docs Coverage

## Runbook Coverage

## Style Issues

## Evidence Gaps

## Recommended Priority
```

### B6.3 Documentation Patch

Path:

```text
data/agent_workspace/patches/{task_id}.adit_docs.patch
```

Patch allowed paths:

```text
README.md
CHANGELOG.md
docs/
mkdocs.yml, if manifest allows
docusaurus.config.*, if manifest allows
openapi.yaml, if manifest allows
asyncapi.yaml, if manifest allows
```

### B6.4 Validation Request

Path:

```text
data/agent_workspace/verification/{task_id}.adit_validation_request.yaml
```

Template:

```yaml
task_id: task-docs-001
requested_by: adit
checks:
  - markdownlint
  - link_check
  - vale_optional
blocking_checks:
  - docs_paths_scope_check
notes: "Adit requests docs validation through Verification Engine."
```

### B6.5 Style Review

Path:

```text
data/agent_workspace/docs/{task_id}.style_review.md
```

Template:

```md
# Documentation Style Review

## Task ID

## Style Guide Applied

## Issues

| Issue | Severity | File | Recommendation |
|---|---|---|---|

## Non-blocking Notes

## Blocking Notes
```

---

## B7. Documentation Folder Structure Target

Default structure:

```text
docs/
├── index.md
├── tutorials/
├── how-to/
├── reference/
├── explanation/
├── runbooks/
└── api/
```

Mapping:

```text
tutorials/    → learning path
how-to/       → task-specific guide
reference/    → schema, CLI, config, commands
explanation/  → concept and architecture
runbooks/     → operational procedure
api/          → OpenAPI/AsyncAPI generated or curated docs
```

Adit tidak boleh memigrasikan semua docs ke struktur ini tanpa manifest khusus dan human approval.

---

## B8. README Policy

README harus berisi:

```text
project purpose
quick start
main features
folder structure
basic commands
safety notes
links to docs
```

Adit tidak boleh memasukkan klaim fitur yang belum ada.

---

## B9. CHANGELOG Policy

Changelog harus memakai format sederhana.

```md
# Changelog

## Unreleased

### Added

### Changed

### Fixed

### Security
```

Adit harus update changelog jika task mengubah:

```text
public behavior
CLI behavior
manifest schema
data schema
agent workflow
safety policy
verification behavior
documentation structure
```

---

## B10. API Documentation Policy

Adit boleh membantu menulis:

```text
OpenAPI explanation
API reference markdown
endpoint table
request response examples
schema explanation
security notes
```

Adit tidak boleh membuat endpoint yang tidak ada.

Jika `openapi.yaml` berubah, Adit wajib meminta:

```text
OpenAPI schema validation
Senior review
Doni review if build tooling changes
```

---

## B11. Runbook Policy

Runbook adalah panduan operasional. Adit boleh menulis runbook, tetapi tidak boleh menjalankan command.

Runbook template:

```md
# Runbook: <Title>

## Purpose

## When to Use

## Preconditions

## Safety Notes

## Steps

## Verification

## Rollback

## Escalation
```

Runbook tidak boleh berisi command destruktif tanpa warning dan human approval.

Command berisiko:

```text
rm -rf
git reset --hard
git clean -fd
git push --force
drop database
delete collection
modify .env
```

---

# Bagian C
# Development Roadmap

---

## C1. Phase 0: Contract Freeze

Deliverables:

```text
config/agents.yaml
config/adit_doc_policy.yaml
schemas/adit_docs_plan.schema.json
schemas/adit_validation_request.schema.json
schemas/doc_gap_report.schema.json
```

Exit criteria:

```text
Adit cannot modify source code.
Adit cannot run shell.
Adit cannot commit or push.
Adit output schema is defined.
```

---

## C2. Phase 1: Documentation Gap Report Only

Goal:

```text
Adit membaca docs dan membuat gap report tanpa patch.
```

Deliverables:

```text
data/agent_workspace/docs/{task_id}.doc_gap_report.md
```

Exit criteria:

```text
Adit can classify docs into Diataxis categories.
No patch is written.
No source file is modified.
```

---

## C3. Phase 2: Documentation Plan

Goal:

```text
Adit membuat documentation plan berdasarkan manifest.
```

Deliverables:

```text
data/agent_workspace/docs/{task_id}.adit_docs_plan.md
```

Exit criteria:

```text
Plan lists evidence, files to change, validation needed, and risks.
```

---

## C4. Phase 3: Small Docs Patch

Goal:

```text
Adit menulis patch kecil untuk docs.
```

Allowed first tasks:

```text
README clarification
CHANGELOG format
single how-to guide
single reference page
single runbook template
```

Exit criteria:

```text
Patch touches allowed docs path only.
Patch size within limit.
Validation request written.
```

---

## C5. Phase 4: Validation Integration

Goal:

```text
Verification Engine can validate Adit docs patch.
```

Checks:

```text
docs path scope check
markdown structure check
link check optional
vale optional
mkdocs build optional
OpenAPI validation if spec changed
AsyncAPI validation if spec changed
```

Exit criteria:

```text
Validation report exists.
Adit does not run build directly.
```

---

## C6. Phase 5: API Docs Support

Goal:

```text
Adit can help document OpenAPI or AsyncAPI artifacts.
```

Rules:

```text
Spec change requires validation.
Generated docs require Runner.
API claims require source or spec evidence.
```

Exit criteria:

```text
No invented endpoint.
OpenAPI validation requested.
Senior review required.
```

---

## C7. Phase 6: Runbook Support

Goal:

```text
Adit writes safe operational runbooks.
```

Rules:

```text
No command execution.
No destructive command without human gate.
Runner validates command block safety.
```

Exit criteria:

```text
Runbook includes purpose, safety, verification, rollback, and escalation.
```

---

# Bagian D
# Referensi Terpisah dari Pondasi Anti-Gagal

Referensi berikut dipakai sebagai knowledge base dan design pattern. Referensi tidak otomatis menjadi dependency.

---

## D1. Compatibility Score

Setiap referensi dinilai sebelum diadopsi.

| Kriteria | Bobot |
|---|---:|
| Cocok dengan local-first | 20 |
| Bisa file-based | 15 |
| Bisa manifest-driven | 15 |
| Tidak memaksa build/deploy besar | 10 |
| Bisa divalidasi tool | 10 |
| Bisa dipakai sebagai pattern saja | 10 |
| Risiko dependency rendah | 10 |
| Implementasi ringan | 10 |

Keputusan:

```text
>= 80  boleh jadi core documentation pattern
60-79  boleh jadi optional docs pattern
40-59  hanya jadi referensi ide
< 40   abaikan untuk fase awal
```

---

## D2. Reference Mapping

| Referensi | Fungsi untuk Adit | Status |
|---|---|---|
| `evildmp/diataxis-documentation-framework` | Struktur tutorial/how-to/reference/explanation | Core knowledge |
| `amrani/diataxis-claude-agent` | Pola agent evaluator docs berbasis Diataxis | Agent behavior reference |
| `anneKsiy/diataxis-documentation-restructurer` | Pola restrukturisasi docs | Agent behavior reference |
| `phillycommunitywireless/docs` | Contoh MkDocs Material technical docs | Template reference |
| `jobindjohn/obsidian-publish-mkdocs` | Pola publish Obsidian ke MkDocs | Optional reference |
| `vsoch/mkdocs-jekyll` | Starter MkDocs/Jekyll/GitHub Pages | Optional template |
| `NETVPX/pterodactyl-api-docs` | Contoh Docusaurus API docs besar | Advanced reference |
| `levino/protected-docs-example` | Warning desain protected docs pada SPA | Cautionary reference |
| `eazybytes/openapi` | Dasar OpenAPI documentation | API docs knowledge |
| `swagger-api/swagger-core` | Swagger/OpenAPI generation ecosystem | Tooling reference |
| `konfig-sdks/openapi-examples` | Contoh OpenAPI publik | Example corpus |
| `alexandramartinez/asyncapi-example` | Contoh AsyncAPI | Event docs reference |
| `Redocly/redoc` | OpenAPI generated API reference | Runner-only tool reference |
| `nelmio/NelmioApiDocBundle` | Symfony API docs generation | Backend-specific reference |
| `SMILEY4/ktor-openapi-tools` | Ktor OpenAPI tooling | Backend-specific reference |
| `vale-cli/Google` | Google Developer Documentation Style Guide via Vale | Style reference |
| `wrappid/guide-module` | Guide module/component docs style | Optional style reference |
| `khalidx/runbook` | Executable Markdown runbook pattern | Concept only, no execution by Adit |

---

## D3. Diataxis References

URLs:

```text
https://github.com/evildmp/diataxis-documentation-framework
https://github.com/amrani/diataxis-claude-agent
https://github.com/anneKsiy/diataxis-documentation-restructurer
```

Use for:

```text
documentation classification
docs gap analysis
docs restructuring plan
docs type decision
tutorial/how-to/reference/explanation separation
```

Local adaptation:

```text
Diataxis → classify_doc_diataxis tool
Diataxis agent → Adit docs evaluator behavior
Restructurer → doc_gap_report and docs_plan
```

Failure-first rule:

```text
Diataxis is a guide, not a forced migration rule.
```

---

## D4. MkDocs References

URLs:

```text
https://github.com/jobindjohn/obsidian-publish-mkdocs
https://github.com/vsoch/mkdocs-jekyll
https://github.com/phillycommunitywireless/docs
```

Use for:

```text
MkDocs folder structure
MkDocs Material technical docs
navigation structure
GitHub Pages style docs
```

Local adaptation:

```text
docs structure suggestion
mkdocs.yml patch only if manifest allows
build request to Runner only
```

Failure-first rule:

```text
Adit may suggest MkDocs config.
Adit may not run mkdocs build or deploy.
```

---

## D5. Docusaurus References

URLs:

```text
https://github.com/NETVPX/pterodactyl-api-docs
https://github.com/levino/protected-docs-example
```

Use for:

```text
large API docs structure
versioned docs idea
interactive examples
protected docs caution
```

Local adaptation:

```text
Docusaurus is advanced and optional.
Use only after docs grow large.
Do not use SPA protected docs for secrets.
```

Failure-first rule:

```text
No Docusaurus migration without human approval.
No docs protection design for secret material.
```

---

## D6. OpenAPI References

URLs:

```text
https://github.com/eazybytes/openapi
https://github.com/swagger-api/swagger-core
https://github.com/konfig-sdks/openapi-examples
```

Use for:

```text
OpenAPI syntax and structure
API examples
schema documentation
request and response examples
security scheme documentation
```

Local adaptation:

```text
Adit writes or improves API docs.
Verification Engine validates OpenAPI spec.
Runner handles generation if needed.
```

Failure-first rule:

```text
No invented endpoints.
Spec change requires validation.
```

---

## D7. AsyncAPI References

URL:

```text
https://github.com/alexandramartinez/asyncapi-example
```

Use for:

```text
event-driven API documentation
message schema documentation
channel documentation
```

Local adaptation:

```text
Only use if ai-rag-local later has event/message API.
```

Failure-first rule:

```text
Do not introduce AsyncAPI unless event architecture exists.
```

---

## D8. Redoc References

URLs:

```text
https://github.com/Redocly/redoc
https://github.com/nelmio/NelmioApiDocBundle
https://github.com/SMILEY4/ktor-openapi-tools
```

Use for:

```text
OpenAPI generated documentation
API reference rendering
backend-specific API docs patterns
```

Local adaptation:

```text
Adit proposes Redoc only if OpenAPI spec exists.
Runner performs generation.
Doni reviews build/tooling impact.
```

Failure-first rule:

```text
No Redoc dependency change without manifest and human review.
```

---

## D9. Style Guide References

URLs:

```text
https://github.com/vale-cli/Google
https://github.com/wrappid/guide-module
```

Use for:

```text
documentation style review
terminology consistency
clarity checks
component guide structure
```

Local adaptation:

```text
Vale rules are warning-only in early phase.
Adit writes style review.
Verification Engine may run Vale later.
```

Failure-first rule:

```text
Style warnings must not block early docs unless explicitly configured.
```

---

## D10. Runbook Reference

URL:

```text
https://github.com/khalidx/runbook
```

Use for:

```text
runbook markdown structure
operational procedure docs
command block pattern awareness
```

Local adaptation:

```text
Adit writes runbook markdown.
Runner validates command blocks.
Adit never executes runbook.
```

Failure-first rule:

```text
Executable runbook is concept only.
No command execution by Adit.
```

---

# Bagian E
# Test and Acceptance Criteria

---

## E1. Minimum Acceptance Criteria

Adit siap tahap awal jika:

```text
Can load valid docs manifest
Can reject invalid manifest
Can classify documentation type
Can write documentation gap report
Can write documentation plan
Can write small docs patch
Can request validation
Can avoid source code changes
Can avoid shell execution
Can stop on insufficient evidence
```

---

## E2. Failure Acceptance Criteria

Adit dianggap failure-first jika:

```text
No invented feature documentation
No source code modification
No docs build execution
No dependency install
No deployment
No runbook execution
No commit
No push
No large docs migration without approval
No OpenAPI endpoint invention
No silent failure
```

---

## E3. First Dry-Run Scenario

Input manifest:

```yaml
task_id: task-docs-001
task_type: documentation
risk_level: low
mode: plan
allowed_paths:
  - README.md
  - docs/
denied_paths:
  - app/
  - .env
  - .git/
required_outputs:
  - doc_gap_report
  - docs_plan
```

Expected:

```text
Adit reads README and docs.
Adit classifies docs with Diataxis.
Adit writes doc_gap_report.
Adit writes docs_plan.
Adit writes no patch unless mode allows.
Adit runs no shell.
```

---

## E4. First Patch Scenario

Input:

```yaml
task_id: task-docs-002
task_type: documentation
risk_level: low
mode: patch
allowed_paths:
  - README.md
  - docs/how-to/
denied_paths:
  - app/
  - .env
required_outputs:
  - docs_plan
  - docs_patch
  - validation_request
```

Expected:

```text
Adit writes a small docs patch.
Adit writes validation request.
Patch touches only allowed docs paths.
Verification Engine checks docs scope.
Senior Reviewer reviews.
```

---

## E5. First Failure Scenario

Input:

```yaml
task_id: task-docs-risk-001
task_type: docs_deployment
risk_level: high
mode: patch
allowed_paths:
  - docusaurus.config.js
required_outputs:
  - docs_patch
```

Expected:

```text
Adit detects high-risk docs deployment or migration.
Adit writes human_review_required.md.
Adit does not edit config automatically.
Adit does not run build.
Adit does not deploy.
```

---

# Final Summary

Adit harus dibangun sebagai documentation agent yang aman saat gagal. Referensi GitHub yang dikumpulkan kuat, tetapi tidak boleh langsung menjadi dependency inti.

Prinsip final:

```text
Start with documentation gap report.
Then documentation plan.
Then small docs patch.
Then validation request.
Then Senior review.
Only after stable, consider larger docs restructuring.
```

Rancangan akhir:

```text
Adit
├── model: qwen3:4b-instruct
├── role: documentation_agent
├── core method: Diataxis classification
├── output: docs plan, docs patch, gap report, runbook template
├── validation: requested through Verification Engine
├── execution: none
├── commit: none
└── push/deploy: none
```

Dengan desain ini, Adit menjadi agent dokumentasi yang produktif, tetapi tetap aman untuk sistem self-development lokal.
