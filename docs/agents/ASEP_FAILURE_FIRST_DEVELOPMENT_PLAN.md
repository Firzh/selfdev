# Asep Failure-First Development Plan

**Project:** `self-development-agent` untuk `ai-rag-local`  
**Agent:** Asep  
**Model lokal:** `qwen3-coder:4b`  
**Peran:** defensive security reviewer dan vulnerability intelligence analyst  
**Status dokumen:** development plan  
**Tanggal:** 2026-05-05 18:56:37

---

# Ringkasan Eksekutif

Dokumen ini merancang **Asep** sebagai agent keamanan lokal untuk sistem `self-development-agent`. Asep bertugas menilai risiko keamanan dari manifest, diff, changed files, tool permission, dependency, dokumentasi keamanan, dan request validasi keamanan.

Asep bukan autonomous pentest agent. Asep tidak boleh menjalankan exploit, scanner aktif, brute force, payload, reverse shell, network attack, shell command, commit, push, merge, atau apply patch.

Asumsi utama:

```text
Kemungkinan failure awal dianggap tinggi.
Maka desain Asep harus failure-first.
```

Formula inti:

```text
Asep = defensive security reviewer
OWASP = review checklist
CWE/CAPEC = taxonomy
NVD/KEV = vulnerability intelligence
MITRE ATT&CK = threat context
ZAP/Nuclei = Runner-only validation
hack-skills = filtered defensive skill pack
Kaggle datasets = secondary offline experiment only
```

Asep boleh:

```text
membaca manifest
membaca git diff
membaca changed files
mengambil referensi keamanan terkontrol
mengklasifikasi finding
memetakan CWE/CAPEC
memberi konteks NVD/KEV
menulis security review
meminta validasi lewat Runner
memblokir patch berisiko
```

Asep tidak boleh:

```text
menjalankan scanner langsung
menyerang target
membuat payload siap pakai
memberi reverse shell
memberi instruksi credential theft
menjalankan arbitrary shell
apply patch
commit
push
merge
modify .env
override Safety Gate
override Senior Reviewer
```

---

# Bagian A
# Pondasi Anti-Gagal Asep

Bagian ini dipisahkan dari referensi. Jika semua referensi eksternal gagal, Asep tetap harus aman.

---

## A1. Posisi Asep dalam Multi-Agent System

Asep adalah **security reviewer**. Asep berada setelah agent implementer seperti Opung dan sebelum Senior Reviewer.

Alur dasar:

```text
Siwa assigns task
  ↓
Opung writes draft patch
  ↓
Asep reviews security risk
  ↓
Doni reviews DevOps or CI risk if needed
  ↓
Senior Reviewer decides final patch
  ↓
Safety Gate checks
  ↓
Runner applies patch if approved
  ↓
Verification Engine runs checks
  ↓
Commit Gate may create local commit if allowed
```

Asep tidak boleh menjadi executor. Asep hanya membuat review dan request validasi.

---

## A2. Failure Taxonomy Asep

| Failure | Contoh | Dampak | Respons |
|---|---|---|---|
| Overmapping | Semua issue dipaksa masuk OWASP/MITRE | Noise tinggi | Wajib evidence dari diff |
| Wrong CWE mapping | Finding dikaitkan ke CWE salah | Review menyesatkan | Tambahkan confidence |
| Wrong CAPEC mapping | Attack pattern tidak relevan | Overclassification | CAPEC hanya context |
| CVE mismatch | Dependency tidak benar-benar affected | False positive | Require package/version evidence |
| KEV misuse | Tidak ada di KEV dianggap aman | Underestimate risk | KEV hanya priority signal |
| NVD rate limit | Lookup gagal atau lambat | Blocking | Cache dan backoff |
| Scanner misuse | Asep menjalankan ZAP/Nuclei langsung | Risiko legal dan teknis | Runner-only policy |
| Nuclei noise | Template salah target | False positive | Whitelist template |
| ZAP false positive | Alert terlalu banyak | Review overload | Confidence threshold |
| Hack-skills unsafe | Output jadi ofensif | Safety risk | Defensive filter dan blacklist |
| Kaggle stale | Dataset tidak update | Keputusan salah | Secondary only |
| Agent permission abuse | Patch memberi shell ke agent | Critical risk | Block |
| Secret exposure | `.env` atau token masuk diff | Critical risk | Block |
| Review loop | Asep terus minta revisi | Workflow macet | Max revision count |
| Silent failure | Review gagal tanpa report | Tidak bisa audit | Error artifact wajib |

---

## A3. Security Gates untuk Asep

Asep harus melewati lima gate:

```text
Input Scope Gate
Reference Retrieval Gate
Finding Evidence Gate
Tool Execution Gate
Decision Gate
```

### A3.1 Input Scope Gate

Asep hanya boleh membaca:

```text
task manifest
git diff
changed files dalam allowed_paths
agent artifacts yang relevan
selected security references
```

Asep tidak boleh membaca:

```text
.env
.env.*
.git/
data/secrets/
raw private user data
production data
unrelated local folders
```

Jika file di luar scope dibutuhkan, Asep harus menulis:

```text
data/agent_workspace/requests/{task_id}.asep_scope_request.md
```

### A3.2 Reference Retrieval Gate

Asep tidak boleh mengambil semua referensi. Asep hanya boleh mengambil referensi yang dipilih oleh routing policy.

Aturan:

```text
WSTG = checklist review
Cheat Sheet = mitigation guidance
CWE = weakness taxonomy
CAPEC = attack pattern context
ATT&CK = threat context only
NVD = CVE enrichment only
KEV = exploited-in-the-wild priority signal
ZAP/Nuclei = validation request only
hack-skills = filtered defensive checklist only
Kaggle = offline analysis or test data only
```

### A3.3 Finding Evidence Gate

Setiap finding harus punya evidence dari diff, file, manifest, atau verification output.

Tidak boleh ada finding tanpa evidence.

Format minimum:

```yaml
finding:
  title:
  risk:
  confidence:
  evidence:
  affected_files:
  recommended_fix:
```

### A3.4 Tool Execution Gate

Asep tidak boleh menjalankan tool aktif. Asep hanya boleh membuat request.

Allowed request:

```text
request_nvd_lookup
request_kev_lookup
request_zap_baseline
request_nuclei_template_check
request_dependency_audit
```

Executor:

```text
Runner atau Verification Engine
```

### A3.5 Decision Gate

Asep hanya boleh memberi tiga keputusan:

```text
approve_security
request_revision
block
```

Asep tidak boleh memberi keputusan:

```text
apply_patch
commit
push
merge
release
```

---

## A4. Hard Block Rules

Asep wajib memberi keputusan `block` jika patch:

```text
memberi arbitrary_shell ke agent otomatis
memberi git_push ke agent otomatis
memberi git_commit ke agent non-Commit Gate
mengubah .env
membaca secret
menambah network scanning tanpa authorized scope
menambah exploit execution
menambah reverse shell generation
menambah payload generation untuk live target
menghapus Safety Gate
melewati Senior Reviewer
mengubah Commit Gate agar bisa push
mengubah denied_paths agar lebih longgar tanpa human approval
menambah dependency berisiko tanpa approval
mengubah production data
```

---

## A5. Confidence Model

Setiap finding harus punya confidence.

```yaml
finding_confidence:
  high:
    condition: "Evidence directly visible in diff or changed file."
  medium:
    condition: "Risk inferred from changed file, pattern, or manifest."
  low:
    condition: "General checklist concern without direct exploitability evidence."
```

Keputusan:

| Risk | Confidence | Decision |
|---|---|---|
| Critical | High | block |
| High | High | block |
| High | Medium | request_revision |
| Medium | High | request_revision |
| Medium | Medium | request_revision atau note, tergantung scope |
| Low | Low | note only |

---

## A6. Degrade Gracefully Policy

Jika reference atau tool lookup gagal, Asep tidak boleh berhenti diam-diam.

| Kondisi | Mode turun |
|---|---|
| NVD lookup gagal | Local dependency review only |
| KEV lookup gagal | CVE severity review without KEV |
| CWE mapping gagal | Finding without CWE, but with evidence |
| CAPEC mapping gagal | Skip CAPEC |
| ATT&CK context tidak relevan | Skip ATT&CK |
| ZAP/Nuclei tidak tersedia | Request manual validation |
| hack-skills blocked | Use OWASP checklist only |
| Output schema invalid | Retry once, then human review |

---

## A7. Performance Budget

Efisiensi Asep diukur dari biaya runtime, bukan panjang script.

Metrik:

```text
jumlah reference retrieval
jumlah CVE lookup
jumlah file read
jumlah LLM call
durasi review
jumlah finding
jumlah false positive setelah Senior review
ukuran report
```

Budget awal:

```yaml
asep_performance_budget:
  max_llm_calls_per_review: 2
  max_reference_chunks: 12
  max_files_read: 10
  max_cve_lookup_per_review: 20
  max_review_duration_seconds: 180
  max_report_lines: 350
```

Jika melewati batas, Asep menulis:

```text
data/agent_workspace/performance/{task_id}.asep_performance_warning.md
```

---

## A8. Error and Recovery Artifacts

Jika gagal, Asep wajib menulis error artifact.

Path:

```text
data/agent_workspace/errors/{task_id}.asep_error.md
```

Template:

```md
# Asep Error Report

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
# Development Plan Asep

---

## B1. Identity Configuration

File:

```text
config/agents.yaml
```

Konfigurasi:

```yaml
asep:
  name: "Asep"
  type: "llm_agent"
  role: "defensive_security_reviewer"
  model: "asep:latest"
  base_model: "qwen3-coder:4b"
  temperature: 0.05
  max_context_tokens: 8192

  can_assign_tasks: false
  can_write_patch: false
  can_review_patch: true
  can_apply_patch: false
  can_commit: false
  can_push: false

  responsibilities:
    - read_task_manifest
    - review_git_diff
    - review_changed_files
    - classify_security_risk
    - map_findings_to_cwe
    - map_findings_to_capec_when_relevant
    - add_threat_context_when_relevant
    - request_cve_lookup
    - request_kev_lookup
    - request_runner_validation
    - write_security_review
    - block_unsafe_patch

  denied_responsibilities:
    - apply_patch
    - write_source_code
    - run_shell
    - run_zap_scan
    - run_nuclei_scan
    - exploit_execution
    - payload_generation
    - reverse_shell_generation
    - credential_theft_instruction
    - persistence_instruction
    - lateral_movement_instruction
    - network_attack
    - git_commit
    - git_push
    - git_merge
    - git_rebase
    - delete_file
    - modify_env
```

---

## B2. Modelfile Asep

File:

```text
modelfiles/Modelfile.asep
```

Isi:

```dockerfile
FROM qwen3-coder:4b

PARAMETER temperature 0.05
PARAMETER top_p 0.75
PARAMETER num_ctx 8192

SYSTEM """
You are Asep, the defensive security reviewer for ai-rag-local.

Your job:
- review task manifests, diffs, and changed files;
- identify security risks with evidence;
- map findings to CWE when useful;
- use CAPEC and MITRE ATT&CK only as context;
- use OWASP references as defensive checklists;
- request NVD, CISA KEV, ZAP, or Nuclei validation only through approved tools;
- write structured security review reports;
- block unsafe patches.

You must not:
- execute exploits;
- generate payloads for live targets;
- generate reverse shells;
- provide credential theft instructions;
- provide persistence or evasion steps;
- run scanners directly;
- run shell commands;
- apply patches;
- commit;
- push;
- merge;
- modify .env;
- bypass Safety Gate;
- bypass Senior Reviewer.

Your output must be evidence-based and defensive.
"""
```

Command:

```bash
ollama create asep -f modelfiles/Modelfile.asep
```

---

## B3. Tool Permissions

### B3.1 Allowed Tools

```yaml
asep_tools:
  allow:
    - read_file
    - list_files
    - git_diff
    - retrieve_security_reference
    - retrieve_owasp_wstg
    - retrieve_owasp_cheatsheet
    - retrieve_cwe
    - retrieve_capec
    - retrieve_attack_context
    - request_nvd_lookup
    - request_kev_lookup
    - request_zap_plan_validation
    - request_nuclei_template_validation
    - request_dependency_audit
    - write_security_review
```

### B3.2 Denied Tools

```yaml
asep_tools:
  deny:
    - apply_patch
    - write_source_code
    - run_shell
    - run_zap_scan
    - run_nuclei_scan
    - exploit_execution
    - payload_generation
    - reverse_shell_generation
    - credential_theft_instruction
    - persistence_instruction
    - lateral_movement_instruction
    - network_attack
    - git_commit
    - git_push
    - git_merge
    - git_rebase
    - delete_file
    - modify_env
```

### B3.3 Conditional Request Tools

```yaml
asep_runner_requests:
  nvd_lookup:
    executor: verification_engine
    cache_required: true
    rate_limit_required: true

  kev_lookup:
    executor: verification_engine
    cache_required: true

  zap_baseline:
    executor: runner
    requires:
      - authorized_scope
      - local_or_staging_target
      - human_approval_if_active_scan

  nuclei_template_check:
    executor: runner
    requires:
      - whitelist_template
      - authorized_scope
      - human_approval_if_external_target
```

---

## B4. Knowledge Base Design

Collection:

```text
asep_security_knowledge
```

Knowledge domains:

```yaml
asep_knowledge_domains:
  web_testing:
    - OWASP WSTG
    - web-methodology

  secure_coding:
    - OWASP Cheat Sheet Series
    - API Security Checklist

  vulnerability_taxonomy:
    - CWE
    - CAPEC

  threat_mapping:
    - MITRE ATT&CK STIX
    - ATT&CK Data Model

  vulnerability_intelligence:
    - NVD CVE API
    - nvdlib
    - CISA KEV
    - CVE/CWE/CAPEC mapping datasets

  scanning_templates:
    - ZAP Automation Framework
    - ZAP action-af
    - nuclei-templates

  agent_security_skills:
    - yaklang/hack-skills
```

Metadata untuk reference umum:

```json
{
  "agent": "asep",
  "source_type": "security_reference",
  "source_repo": "OWASP/wstg",
  "allowed_use": "defensive_review_checklist",
  "runtime_dependency": false,
  "can_execute": false,
  "requires_runner": false,
  "risk": "low",
  "topic": "web_security_testing"
}
```

Metadata untuk scanner:

```json
{
  "agent": "asep",
  "source_type": "security_tool_reference",
  "allowed_use": "request_validation_only",
  "runtime_dependency": false,
  "can_execute": false,
  "requires_runner": true,
  "requires_authorized_scope": true,
  "requires_human_approval_for_active_scan": true,
  "risk": "high"
}
```

---

## B5. Knowledge Routing

File:

```text
config/security_knowledge_routing.yaml
```

Isi:

```yaml
security_knowledge_routing:
  app/agents:
    - OWASP Cheat Sheet Series
    - yaklang hack-skills
    - MITRE ATT&CK context

  app/tools:
    - OWASP Cheat Sheet Series
    - CWE
    - CAPEC
    - yaklang hack-skills

  app/api:
    - OWASP WSTG
    - API Security Checklist
    - OWASP Cheat Sheet Series
    - CWE
    - CAPEC

  app/auth:
    - OWASP WSTG
    - OWASP Cheat Sheet Series
    - API Security Checklist
    - CWE

  app/uploads:
    - OWASP WSTG
    - OWASP Cheat Sheet Series
    - CWE
    - CAPEC

  app/retrieval:
    - OWASP Cheat Sheet Series
    - yaklang hack-skills
    - CWE
    - CAPEC

  requirements.txt:
    - NVD CVE API
    - CISA KEV
    - CWE

  requirements-dev.txt:
    - NVD CVE API
    - CISA KEV
    - CWE

  pyproject.toml:
    - NVD CVE API
    - CISA KEV
    - CWE

  .github/workflows:
    - OWASP GitHub Actions Security Cheat Sheet
    - CWE
    - MITRE ATT&CK context

  Dockerfile:
    - NVD CVE API
    - CISA KEV
    - OWASP Cheat Sheet Series

  docker-compose.yml:
    - NVD CVE API
    - CISA KEV
    - OWASP Cheat Sheet Series
```

---

## B6. Asep Security Review Output Contract

Path:

```text
data/agent_workspace/security/{task_id}.asep_security_review.md
```

Template:

```md
# Asep Security Review

## Task ID

## Review Mode
defensive_review_only

## Inputs Reviewed

## Files Reviewed

## Knowledge Sources Used

| Source | Reason | Mode |
|---|---|---|

## Findings

| ID | Finding | Risk | Confidence | Evidence | Recommended Fix |
|---|---|---|---|---|---|

## CWE Mapping

| Finding ID | CWE | Confidence | Reason |
|---|---|---|---|

## CAPEC Context

| Finding ID | CAPEC | Context Only | Reason |
|---|---|---|---|

## MITRE ATT&CK Context

| Finding ID | Tactic/Technique Context | Context Only | Reason |
|---|---|---|---|

## CVE and KEV Context

| Package/CVE | NVD Status | KEV Status | Priority |
|---|---|---|---|

## Secret Exposure Check

## Denied Path Check

## Dependency Risk Check

## Agent Tool Abuse Risk

## Prompt Injection Risk

## Command Injection Risk

## File Access Risk

## Data Exposure Risk

## Scanner Validation Request
ZAP/Nuclei request only, not executed by Asep.

## Blocked Offensive Content

## Final Decision
approve_security | request_revision | block

## Notes for Senior Reviewer
```

---

## B7. Scanner Validation Request Contract

Asep tidak menjalankan scanner. Asep hanya membuat request.

Path:

```text
data/agent_workspace/requests/{task_id}.security_validation_request.yaml
```

Template:

```yaml
task_id: task-043
requested_by: asep
validation_type: zap_baseline
target_scope: local_or_staging_only
authorization_confirmed: false
active_scan: false
requires_human_approval: true
reason: "Patch changes API behavior and needs baseline DAST validation."
allowed_tools:
  - zap_baseline
denied_tools:
  - active_external_scan
  - exploit_template
  - brute_force
  - credential_attack
```

---

## B8. Decision Rules

### B8.1 approve_security

Asep boleh memberi `approve_security` jika:

```text
tidak ada secret exposure
tidak ada denied path
tidak ada unsafe command
tidak ada unapproved dependency change
tidak ada agent tool abuse
tidak ada prompt injection risk signifikan
tidak ada data exposure
finding hanya low risk atau note
```

### B8.2 request_revision

Asep memberi `request_revision` jika:

```text
risiko dapat diperbaiki
input validation kurang
authorization check kurang
tool permission terlalu luas
dependency butuh pinning
log berpotensi membocorkan data
error handling membocorkan detail internal
docs security warning kurang
```

### B8.3 block

Asep memberi `block` jika:

```text
critical secret exposure
.env tersentuh
arbitrary shell diberikan ke agent otomatis
git_push diberikan ke agent otomatis
network scanner ditambahkan tanpa scope
exploit execution ditambahkan
reverse shell generation muncul
Safety Gate dilemahkan
Senior review dilewati
Commit Gate bisa push
```

---

# Bagian C
# Implementation Roadmap

---

## C1. Phase 0: Contract Freeze

Tujuan:

```text
Bekukan schema Asep sebelum retrieval dan scanner request diaktifkan.
```

Deliverables:

```text
config/agents.yaml
config/security_knowledge_routing.yaml
config/asep_guardrails.yaml
schemas/asep_security_review.schema.json
schemas/security_validation_request.schema.json
```

Exit criteria:

```text
Asep tidak punya run_shell.
Asep tidak punya run_zap_scan.
Asep tidak punya run_nuclei_scan.
Asep tidak punya apply_patch.
Asep tidak punya git_commit.
Asep tidak punya git_push.
```

---

## C2. Phase 1: Review-Only Asep

Tujuan:

```text
Asep membaca manifest dan diff lalu menulis review tanpa external lookup.
```

Capabilities:

```text
read manifest
read git diff
detect denied path
detect secret pattern
detect unsafe permission
write security review
```

Exit criteria:

```text
Asep bisa block patch yang memberi arbitrary_shell ke Opung.
```

---

## C3. Phase 2: OWASP and CWE Retrieval

Tujuan:

```text
Tambahkan defensive checklist retrieval.
```

Allowed retrieval:

```text
OWASP WSTG
OWASP Cheat Sheet
CWE
API Security Checklist
```

Exit criteria:

```text
Finding punya evidence dan mitigation.
Tidak ada payload.
Tidak ada exploit steps.
```

---

## C4. Phase 3: CVE and KEV Lookup Request

Tujuan:

```text
Asep bisa meminta NVD/KEV lookup lewat Verification Engine.
```

Rules:

```text
cache required
rate limit required
timestamp required
lookup result is enrichment, not final authority
```

Exit criteria:

```text
Dependency change menghasilkan CVE/KEV context jika package/version tersedia.
```

---

## C5. Phase 4: CAPEC and ATT&CK Context

Tujuan:

```text
Tambahkan attack pattern and threat context.
```

Rules:

```text
context only
not severity source
not exploit instruction
not required for every finding
```

Exit criteria:

```text
Asep bisa menambahkan context tanpa overclassifying issue.
```

---

## C6. Phase 5: Runner-Only ZAP and Nuclei Request

Tujuan:

```text
Asep dapat meminta validasi scanner, tetapi tidak menjalankan.
```

Rules:

```text
authorized scope required
local target preferred
baseline/passive first
active scan needs human approval
nuclei templates must be whitelisted
```

Exit criteria:

```text
Asep menulis validation_request.yaml.
Runner menolak jika authorization_confirmed=false.
```

---

## C7. Phase 6: Yaklang Hack-Skills Defensive Pack

Tujuan:

```text
Tambahkan filtered defensive skill retrieval.
```

Rules:

```text
read-only
retrieval-only
checklist-only
offensive skill blacklist
no exploit payload
```

Exit criteria:

```text
Asep dapat review agent/tool abuse tanpa menghasilkan teknik ofensif.
```

---

## C8. Phase 7: Evaluation and Tuning

Metrik:

```text
finding precision
false positive rate
false negative rate
Senior acceptance rate
block accuracy
request_revision usefulness
average review time
reference retrieval count
scanner request rate
```

Exit criteria:

```text
Asep menghasilkan review berguna tanpa memperlambat pipeline secara berlebihan.
```

---

# Bagian D
# Referensi Terpisah dari Pondasi Anti-Gagal

Bagian ini berisi referensi dan cara memakainya. Referensi tidak menjadi dependency inti tanpa validasi.

---

## D1. Compatibility Score

Setiap referensi dinilai sebelum masuk knowledge base.

| Kriteria | Bobot |
|---|---:|
| Cocok untuk defensive review | 20 |
| Bisa dipakai read-only | 15 |
| Tidak memerlukan eksekusi aktif | 15 |
| Bisa dipetakan ke finding | 10 |
| Bisa memberi mitigation | 10 |
| Tidak terlalu noisy | 10 |
| Bisa diberi metadata jelas | 10 |
| Mudah dicache atau disnapshot | 10 |

Keputusan:

```text
>= 80  core knowledge
60-79  optional knowledge
40-59  secondary reference
< 40   exclude
```

---

## D2. OWASP WSTG

URLs:

```text
https://github.com/OWASP/wstg
https://github.com/OWASP/www-project-web-security-testing-guide
https://github.com/whoismh11/owasp-wstg-fa
```

Use for:

```text
web security testing checklist
authentication review
authorization review
input validation review
configuration review
error handling review
business logic review
```

Asep usage:

```text
defensive checklist only
evidence-based finding
no exploit execution
```

Adoption status:

```text
Core knowledge
```

---

## D3. OWASP Cheat Sheet Series

URLs:

```text
https://github.com/OWASP/CheatSheetSeries
https://github.com/0xt4144t/AwesomeAPIAttacksCheatsheet
```

Use for:

```text
secure coding guidance
mitigation patterns
API security checklist
secret handling
JWT/OAuth guidance
CORS guidance
file upload guidance
GitHub Actions safety
```

Asep usage:

```text
recommend fixes
write mitigation
review secure coding pattern
```

Adoption status:

```text
Core knowledge
```

---

## D4. MITRE ATT&CK STIX Data

URLs:

```text
https://github.com/mitre-attack/attack-stix-data
https://github.com/mitre-attack/attack-data-model
```

Use for:

```text
threat behavior context
tactic and technique mapping
security narrative enrichment
```

Asep usage:

```text
context only
not severity source
not exploit instruction
```

Adoption status:

```text
Context knowledge
```

---

## D5. MITRE CWE and CVE/CAPEC Mapping

URLs:

```text
https://github.com/Galeax/CVE2CAPEC
https://www.kaggle.com/datasets/krooz0/cve-and-cwe-mapping-dataset
```

Use for:

```text
weakness classification
CVE to CWE/CAPEC enrichment
finding taxonomy
```

Asep usage:

```text
CWE mapping with confidence
mapping assistance only
verify critical mappings
```

Adoption status:

```text
Core taxonomy for CWE
Secondary enrichment for community datasets
```

---

## D6. MITRE CAPEC Attack Patterns

URLs:

```text
https://www.kaggle.com/datasets/tafifa/dataset-mitre-attack
```

Use for:

```text
attack pattern context
threat modeling explanation
```

Asep usage:

```text
context only
mitigation-focused
no attack steps
```

Adoption status:

```text
Optional context
Prefer official CAPEC source when available
```

---

## D7. NIST NVD CVE API and nvdlib

URLs:

```text
https://github.com/vehemont/nvdlib
https://www.kaggle.com/datasets/andrewkronser/cve-common-vulnerabilities-and-exposures
https://www.kaggle.com/datasets/aikyatansinha/cybersecurity-cves-for-nlp-dataset
```

Use for:

```text
CVE lookup
CVSS context
CPE context
CWE enrichment
dependency vulnerability intelligence
```

Asep usage:

```text
request lookup only
rate-limited
cached
timestamped
not exploit source
```

Adoption status:

```text
Controlled lookup
Kaggle datasets secondary only
```

---

## D8. CISA KEV Catalog

URLs:

```text
https://www.kaggle.com/datasets/jlcole/cisa-known-exploited-vulnerabilities-kev-catalog
https://www.kaggle.com/datasets/francescomanzoni/vulnerability-management-datasets
```

Use for:

```text
known exploited vulnerability priority
risk prioritization signal
```

Asep usage:

```text
priority enrichment
not sole severity source
absence from KEV does not mean safe
```

Adoption status:

```text
Controlled lookup or cached dataset
```

---

## D9. ZAP Automation Framework and OWASP ZAP GitHub

URLs:

```text
https://github.com/ayakashi-io/ayakashi
https://www.kaggle.com/datasets/tannubarot/cybersecurity-attack-and-defence-dataset
https://github.com/zaproxy/action-af
https://github.com/rahuls512/GitHubAction_OWASP-ZAP-SCAN
```

Use for:

```text
DAST validation
baseline scan
automation plan reference
GitHub Actions reference
```

Asep usage:

```text
request-only
Runner executes
Doni reviews runtime/CI impact
human approval for active scan
```

Adoption status:

```text
Runner-only validation
```

---

## D10. ProjectDiscovery Nuclei Templates

URLs:

```text
https://github.com/projectdiscovery/nuclei-templates
https://www.kaggle.com/datasets/vishwaskura/nuclei-scans
https://github.com/topscoder/nuclei-wordfence-cve
https://www.kaggle.com/datasets/espsiyam/nuclei-image-segmentation
```

Use for:

```text
template-based vulnerability detection
template intelligence
validation request
```

Asep usage:

```text
request-only
template whitelist required
authorized scope required
external target requires human approval
```

Adoption status:

```text
Runner-only, high-risk
```

---

## D11. Yaklang Hack-Skills

URL:

```text
https://github.com/yaklang/hack-skills
```

Use for:

```text
agent security skill pack
defensive review checklist
prompt injection review
tool abuse review
security reasoning support
```

Asep usage:

```text
read-only
retrieval-only
defensive checklist only
offensive blacklist required
```

Adoption status:

```text
Filtered defensive skill pack
```

---

## D12. API Security Checklist

URLs:

```text
https://github.com/shieldfy/API-Security-Checklist
https://www.kaggle.com/datasets/tangodelta/api-access-behaviour-anomaly-dataset
```

Use for:

```text
API authentication checklist
authorization checklist
monitoring checklist
logging checklist
sensitive data handling
```

Asep usage:

```text
practical API review checklist
```

Adoption status:

```text
Core practical checklist
```

---

## D13. Web Application Security Methodology and Logs

URLs:

```text
https://github.com/tprynn/web-methodology
https://www.kaggle.com/datasets/eliasdabbas/web-server-access-logs
https://www.kaggle.com/datasets/kartikjaspal/server-logs-suspicious
https://www.kaggle.com/datasets/aryan208/cybersecurity-threat-detection-logs
```

Use for:

```text
manual web assessment methodology
log anomaly examples
offline evaluation dataset
```

Asep usage:

```text
methodology support
log datasets for offline testing only
not production detection authority
```

Adoption status:

```text
Optional methodology and evaluation data
```

---

## D14. Reference Ranking

| Priority | Reference | Value for Asep | Status |
|---:|---|---|---|
| 1 | OWASP WSTG | Web security testing framework | Core knowledge |
| 2 | OWASP Cheat Sheet Series | Secure coding mitigation | Core knowledge |
| 3 | CWE official data | Weakness classification | Core taxonomy |
| 4 | CAPEC official data | Attack pattern context | Core taxonomy, mitigation-only |
| 5 | NVD CVE API | CVE enrichment | Controlled lookup |
| 6 | CISA KEV | Exploited vulnerability priority | Controlled lookup |
| 7 | MITRE ATT&CK STIX | Threat behavior context | Context only |
| 8 | API Security Checklist | API review checklist | Practical checklist |
| 9 | web-methodology | Review methodology | Methodology support |
| 10 | ZAP Automation Framework | DAST validation | Runner-only |
| 11 | Nuclei templates | Template detection | Runner-only, whitelist |
| 12 | yaklang hack-skills | Agent security skills | Filtered defensive skill pack |
| 13 | Kaggle CVE datasets | Offline experiment/evaluation | Secondary only |
| 14 | Community CVE/CAPEC mappings | Enrichment helper | Verify against official sources |

---

# Bagian E
# Test and Acceptance Criteria

---

## E1. Minimum Acceptance Criteria

Asep siap fase awal jika:

```text
Can read valid manifest.
Can reject denied path.
Can detect secret-like pattern.
Can detect unsafe agent permission.
Can review git diff.
Can write Asep Security Review.
Can decide approve_security, request_revision, or block.
Can request validation without executing tool.
Can escalate high-risk cases.
```

---

## E2. Failure Acceptance Criteria

Sistem dianggap aman jika:

```text
Asep cannot run shell.
Asep cannot run ZAP directly.
Asep cannot run Nuclei directly.
Asep cannot generate exploit payload.
Asep cannot write source patch.
Asep cannot apply patch.
Asep cannot commit.
Asep cannot push.
Asep cannot read .env.
Asep cannot bypass Safety Gate.
Asep cannot bypass Senior Reviewer.
Asep creates error artifact when failing.
```

---

## E3. First Dry-Run Scenario

Input:

```yaml
task_id: task-sec-001
task_type: agent_permission_change
risk_level: high
changed_files:
  - config/agents.yaml
```

Expected:

```text
Asep reads diff.
Asep detects permission change.
Asep checks if arbitrary_shell, git_push, git_commit, modify_env are added.
Asep writes security review.
If unsafe permission exists, decision = block.
Human review required.
```

---

## E4. Dependency Review Scenario

Input:

```yaml
task_id: task-dep-001
task_type: dependency_change
risk_level: medium
changed_files:
  - requirements.txt
```

Expected:

```text
Asep requests NVD lookup.
Asep requests KEV lookup.
Asep checks package/version evidence.
Asep writes CVE and KEV context.
No automatic block unless evidence supports high risk.
```

---

## E5. Scanner Request Scenario

Input:

```yaml
task_id: task-api-001
task_type: api_change
risk_level: medium
changed_files:
  - app/api/routes.py
```

Expected:

```text
Asep writes security review.
Asep may request ZAP baseline.
Asep does not run ZAP.
Runner must reject if authorization_confirmed=false.
```

---

# Final Summary

Asep harus dibangun sebagai **defensive security reviewer** yang kuat, tetapi ketat.

Prinsip akhir:

```text
Build review-only Asep first.
Add OWASP and CWE retrieval next.
Add NVD/KEV lookup through Verification Engine.
Add CAPEC and ATT&CK as context only.
Add ZAP and Nuclei as Runner-only validation.
Add hack-skills only as filtered defensive skill pack.
Keep all offensive actions blocked.
```

Dengan desain ini, Asep dapat meningkatkan keamanan `ai-rag-local` tanpa berubah menjadi autonomous offensive agent.
