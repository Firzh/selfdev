# Asep Knowledge Base Links

**Agent:** Asep  
**Role:** Defensive security reviewer, vulnerability intelligence analyst, and security validation requester  
**Purpose:** daftar rujukan knowledge base untuk OWASP WSTG, OWASP ASVS, OWASP API Security Top 10, MITRE ATT&CK Enterprise, MITRE CWE Top 25, MITRE CAPEC, NVD CVE, CISA KEV, security test case template, vulnerability report template, CVSS scoring guide, dan pentest rules of engagement template  
**Created:** 2026-05-05 19:43:09

---

# 1. Fungsi Knowledge Base Asep

Knowledge base ini dipakai untuk memperkuat Asep sebagai **defensive security reviewer**.

Asep memakai rujukan ini untuk:

```text
web security review
application security verification
API security review
weakness classification
attack pattern context
threat behavior context
CVE enrichment
exploited vulnerability prioritization
CVSS scoring support
security test case drafting
vulnerability report drafting
rules of engagement review
```

Asep tidak boleh memakai rujukan ini sebagai izin untuk:

```text
menjalankan exploit
menjalankan scanner aktif tanpa scope
melakukan pentest live target
membuat payload siap pakai
membuat reverse shell
credential theft
persistence
lateral movement
brute force
network attack
run shell
apply patch
commit
push
merge
modify .env
bypass Safety Gate
bypass Senior Reviewer
```

Prinsip:

```text
Knowledge base = boleh dibaca
Security review = boleh ditulis
Validation request = boleh dibuat
Execution = hanya Runner atau Verification Engine
High-risk action = wajib Human Owner approval
```

---

# 2. Core Base Knowledge untuk Asep

| Domain | Isi yang perlu dipahami | Fungsi Asep |
|---|---|---|
| OWASP WSTG | Web security testing framework, testing categories, reporting | Membuat checklist web security review |
| OWASP ASVS | Verification requirement, security control levels | Membuat security test case dan requirement mapping |
| OWASP API Security Top 10 | API risk category dan mitigation awareness | Review endpoint API dan auth flow |
| MITRE ATT&CK Enterprise | Tactics, techniques, mitigations | Memberi threat context, bukan exploit instruction |
| MITRE CWE Top 25 | Software weakness priority | Mengklasifikasi kelemahan source/config |
| MITRE CAPEC | Attack pattern taxonomy | Memberi attack pattern context secara defensif |
| NVD CVE | CVE, CVSS, CPE, CWE enrichment | Memperkaya dependency or component risk |
| CISA KEV | Known exploited vulnerabilities | Prioritas risiko yang sudah exploited |
| Security test case template | Requirement, precondition, steps, expected result | Membuat test case defensif |
| Vulnerability report template | Finding, impact, evidence, mitigation | Membuat laporan security review |
| CVSS scoring guide | Base, temporal, environmental metric | Membantu severity scoring |
| Pentest ROE template | Scope, authorization, allowed/disallowed actions | Memastikan aktivitas sesuai izin |

---

# 3. OWASP WSTG Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | OWASP WSTG official project | https://owasp.org/www-project-web-security-testing-guide/ | Project page untuk Web Security Testing Guide |
| 2 | OWASP WSTG latest | https://owasp.org/www-project-web-security-testing-guide/latest/ | Versi latest WSTG |
| 3 | OWASP WSTG GitHub | https://github.com/OWASP/wstg | Source repository WSTG |
| 4 | OWASP WSTG Reporting | https://owasp.org/www-project-web-security-testing-guide/latest/5-Reporting/01-Reporting_Structure | Struktur reporting keamanan |
| 5 | OWASP WSTG v4.2 archive | https://owasp.org/www-project-web-security-testing-guide/v42/ | Versi stabil archive untuk rujukan lama |

Use for Asep:

```text
Build web security review checklist.
Map findings to testing categories.
Write vulnerability report structure.
Support defensive test planning.
```

Restrictions:

```text
Asep may not execute attacks.
Asep may not generate payloads.
Asep may only use WSTG as defensive checklist and reporting guide.
```

Suggested local routing:

```yaml
security_knowledge_routing:
  "app/api":
    - OWASP WSTG
  "app/auth":
    - OWASP WSTG
  "app/uploads":
    - OWASP WSTG
  "app/web":
    - OWASP WSTG
```

---

# 4. OWASP ASVS Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | OWASP ASVS official project | https://owasp.org/www-project-application-security-verification-standard/ | Project page ASVS |
| 2 | OWASP ASVS GitHub | https://github.com/OWASP/ASVS | Source repository ASVS |
| 3 | OWASP ASVS Security Evaluation Templates with Nuclei | https://owasp.org/www-project-asvs-security-evaluation-templates-with-nuclei/ | ASVS evaluation template idea, request-only |
| 4 | ASVS template example | https://www.reqview.com/doc/asvs-template/ | Security requirement template example |
| 5 | OWASP Cheat Sheet Series | https://github.com/OWASP/CheatSheetSeries | Supporting secure coding guidance |

Use for Asep:

```text
Create verification requirement mapping.
Draft security test cases.
Review technical security controls.
Classify security verification level.
```

Restrictions:

```text
Asep may not run Nuclei directly.
Asep may request ASVS-based validation through Runner only.
Asep must not treat ASVS checklist as proof of exploitability.
```

Suggested ASVS mapping fields:

```yaml
asvs_mapping:
  requirement_id:
  requirement_title:
  verification_level:
  affected_file:
  evidence:
  status: pass | fail | not_applicable | needs_manual_review
```

---

# 5. OWASP API Security Top 10 Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | OWASP API Security Project | https://owasp.org/www-project-api-security/ | API Security project page |
| 2 | OWASP API Security Top 10 | https://owasp.org/API-Security/ | Main API Security Top 10 portal |
| 3 | OWASP API Security Top 10 2023 | https://owasp.org/API-Security/editions/2023/en/0x11-t10/ | API Top 10 2023 list |
| 4 | OWASP API Security Introduction | https://owasp.org/API-Security/editions/2023/en/0x03-introduction/ | API security purpose and context |
| 5 | API Security Checklist | https://github.com/shieldfy/API-Security-Checklist | Practical API security checklist |

Use for Asep:

```text
Review object-level authorization.
Review authentication.
Review authorization boundaries.
Review unrestricted resource consumption.
Review sensitive business flows.
Review logging and monitoring gaps.
```

Restrictions:

```text
Asep may write review findings.
Asep may not run API fuzzing or brute force.
Asep must request active API testing through Runner with authorized scope.
```

---

# 6. MITRE ATT&CK Enterprise Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | MITRE ATT&CK Enterprise Matrix | https://attack.mitre.org/matrices/enterprise/ | Enterprise tactics and techniques matrix |
| 2 | MITRE ATT&CK Enterprise Techniques | https://attack.mitre.org/techniques/enterprise/ | Enterprise techniques list |
| 3 | MITRE ATT&CK Enterprise Tactics | https://attack.mitre.org/tactics/enterprise/ | Enterprise tactics |
| 4 | MITRE ATT&CK Enterprise Mitigations | https://attack.mitre.org/mitigations/enterprise/ | Mitigation context |
| 5 | ATT&CK STIX Data GitHub | https://github.com/mitre-attack/attack-stix-data | STIX data source |
| 6 | ATT&CK Data Model | https://github.com/mitre-attack/attack-data-model | Data model reference |
| 7 | ATT&CK updates | https://attack.mitre.org/resources/updates/ | Release updates |

Use for Asep:

```text
Add threat behavior context.
Map risky behavior to defensive context.
Explain why a risky permission or execution path matters.
Recommend mitigations.
```

Restrictions:

```text
ATT&CK is context only.
ATT&CK must not be used as exploit guide.
ATT&CK must not be used as sole severity source.
```

Suggested field:

```yaml
attack_context:
  tactic:
  technique:
  context_only: true
  defensive_relevance:
  mitigation:
```

---

# 7. MITRE CWE Top 25 and CWE Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | CWE official website | https://cwe.mitre.org/ | Common Weakness Enumeration homepage |
| 2 | CWE Top 25 | https://cwe.mitre.org/top25/ | Current CWE Top 25 index |
| 3 | CWE Top 25 archive | https://cwe.mitre.org/top25/archive/ | Historical CWE Top 25 archive |
| 4 | CWE data downloads | https://cwe.mitre.org/data/downloads.html | XML, CSV, and structured data |
| 5 | CWE list | https://cwe.mitre.org/data/index.html | CWE list and views |

Use for Asep:

```text
Classify weakness type.
Map findings to CWE when evidence supports it.
Use Top 25 as priority awareness.
Improve vulnerability report consistency.
```

Restrictions:

```text
CWE mapping must include confidence.
Do not force CWE mapping if evidence is weak.
Do not treat CWE Top 25 rank as final severity.
```

Suggested field:

```yaml
cwe_mapping:
  cwe_id:
  cwe_name:
  confidence: high | medium | low
  evidence:
  reason:
```

---

# 8. MITRE CAPEC Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | CAPEC official website | https://capec.mitre.org/ | CAPEC homepage |
| 2 | CAPEC list and downloads | https://capec.mitre.org/data/index.html | CAPEC list and structured data |
| 3 | CAPEC documents | https://capec.mitre.org/about/documents.html | Schema and documentation |
| 4 | CAPEC and ATT&CK comparison | https://capec.mitre.org/about/attack_comparison.html | Difference between CAPEC and ATT&CK |
| 5 | CAPEC search | https://capec.mitre.org/data/definitions/ | CAPEC definitions entry point |

Use for Asep:

```text
Add attack pattern context.
Support threat modeling.
Explain likely abuse pattern defensively.
Link weakness to mitigation thinking.
```

Restrictions:

```text
CAPEC is context only.
Asep must not output attack steps.
Asep must not generate exploit chains.
```

Suggested field:

```yaml
capec_context:
  capec_id:
  attack_pattern:
  context_only: true
  mitigation_focus:
```

---

# 9. NVD CVE Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | NVD official website | https://nvd.nist.gov/ | National Vulnerability Database |
| 2 | NVD developers | https://nvd.nist.gov/developers | NVD developer documentation |
| 3 | NVD CVE API documentation | https://nvd.nist.gov/developers/vulnerabilities | CVE API |
| 4 | NVD data feeds | https://nvd.nist.gov/vuln/data-feeds | CVE and CPE data feed references |
| 5 | NVD CVSS calculator | https://nvd.nist.gov/vuln-metrics/cvss/v4-calculator | CVSS v4 calculator |
| 6 | nvdlib Python wrapper | https://github.com/vehemont/nvdlib | Python wrapper for NVD API |

Use for Asep:

```text
CVE lookup.
Dependency vulnerability enrichment.
CPE and version context.
CVSS context.
CWE enrichment.
```

Restrictions:

```text
Asep can request NVD lookup only.
Verification Engine performs lookup.
Cache and rate limit are required.
NVD CVE data is enrichment, not proof of exploitability in local code.
```

Suggested lookup request:

```yaml
task_id:
requested_by: asep
lookup_type: nvd_cve
package:
version:
cve_id:
cache_required: true
rate_limit_required: true
```

---

# 10. CISA KEV Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | CISA KEV Catalog | https://www.cisa.gov/known-exploited-vulnerabilities-catalog | Official KEV catalog |
| 2 | CISA KEV JSON | https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json | JSON feed |
| 3 | CISA KEV CSV | https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.csv | CSV feed |
| 4 | CISA KEV JSON Schema | https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities_schema.json | JSON schema |
| 5 | CISA KEV GitHub mirror | https://github.com/cisagov/kev-data | GitHub mirror for easier consumption |

Use for Asep:

```text
Prioritize known exploited vulnerabilities.
Raise risk priority when CVE exists in KEV.
Support remediation urgency.
```

Restrictions:

```text
KEV is a prioritization signal.
Absence from KEV does not mean safe.
Asep can request KEV lookup only.
```

Suggested KEV field:

```yaml
kev_context:
  cve_id:
  in_kev: true | false | unknown
  due_date:
  known_ransomware_use:
  priority_note:
```

---

# 11. CVSS Scoring Guide

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | FIRST CVSS official page | https://www.first.org/cvss/ | CVSS overview and versions |
| 2 | FIRST CVSS v4.0 specification | https://www.first.org/cvss/v4.0/specification-document | CVSS v4.0 specification |
| 3 | FIRST CVSS v4.0 user guide | https://www.first.org/cvss/v4.0/user-guide | CVSS scoring guide |
| 4 | FIRST CVSS calculator | https://www.first.org/cvss/calculator/4.0 | CVSS calculator |
| 5 | NVD CVSS v4 calculator | https://nvd.nist.gov/vuln-metrics/cvss/v4-calculator | NVD CVSS calculator |

Use for Asep:

```text
Support severity reasoning.
Draft CVSS score suggestion.
Separate risk from priority.
Document scoring assumptions.
```

Restrictions:

```text
Asep may suggest CVSS.
Senior Reviewer or Human Owner should confirm high-severity scores.
CVSS score must include assumptions.
```

Suggested CVSS field:

```yaml
cvss:
  version: "4.0"
  vector:
  base_score:
  assumptions:
  reviewer_note:
```

---

# 12. Security Test Case Template

## 12.1 References

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | OWASP ASVS | https://owasp.org/www-project-application-security-verification-standard/ | Security verification requirements |
| 2 | OWASP WSTG | https://owasp.org/www-project-web-security-testing-guide/latest/ | Web security testing guide |
| 3 | OWASP API Security Top 10 | https://owasp.org/API-Security/ | API security test themes |
| 4 | OWASP ASVS Security Evaluation Templates with Nuclei | https://owasp.org/www-project-asvs-security-evaluation-templates-with-nuclei/ | ASVS test template concept, request-only |
| 5 | ReqView ASVS Template | https://www.reqview.com/doc/asvs-template/ | ASVS requirement/test template example |

## 12.2 Suggested Security Test Case Template

```md
# Security Test Case: {test_case_title}

## Test Case ID

## Related Requirement

ASVS / WSTG / API Top 10 / CWE:

## Objective

## Scope

## Preconditions

## Test Data

## Steps

1. Step one.
2. Step two.
3. Step three.

## Expected Result

## Actual Result

## Evidence

## Risk if Failed

## Status

pass | fail | blocked | not_applicable | needs_manual_review

## Notes
```

Use for Asep:

```text
Draft defensive security test cases.
Map tests to ASVS/WSTG/API Top 10.
Avoid offensive payload generation.
Request Runner validation only if authorized.
```

---

# 13. Vulnerability Report Template

## 13.1 References

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | OWASP WSTG Reporting Structure | https://owasp.org/www-project-web-security-testing-guide/latest/5-Reporting/01-Reporting_Structure | Security report structure |
| 2 | OWASP Risk Rating Methodology | https://owasp.org/www-community/OWASP_Risk_Rating_Methodology | Risk rating model |
| 3 | CVSS v4.0 User Guide | https://www.first.org/cvss/v4.0/user-guide | Severity scoring support |
| 4 | CISA KEV Catalog | https://www.cisa.gov/known-exploited-vulnerabilities-catalog | Exploited vulnerability priority |
| 5 | CWE | https://cwe.mitre.org/ | Weakness classification |

## 13.2 Suggested Vulnerability Report Template

```md
# Vulnerability Report

## Finding ID

## Title

## Executive Summary

## Affected Asset

## Affected File or Component

## Severity

Critical | High | Medium | Low | Informational

## Confidence

High | Medium | Low

## Evidence

## Technical Details

## CWE Mapping

## CAPEC Context

## MITRE ATT&CK Context

## CVE and KEV Context

## Impact

## Likelihood

## Recommended Fix

## Validation Steps

## Status

open | fixed | accepted_risk | false_positive | needs_review

## Notes for Senior Reviewer
```

Use for Asep:

```text
Write structured security review findings.
Separate evidence, severity, confidence, and priority.
Avoid unsupported claims.
```

---

# 14. Pentest Rules of Engagement Template

## 14.1 References

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | PTES Pre-engagement Interactions | https://pentest-standard.readthedocs.io/en/latest/pre-engagement_interactions.html | Scoping, timing, third-party, support, and authorization planning |
| 2 | PTES Technical Guidelines | https://www.pentest-standard.org/index.php/PTES_Technical_Guidelines | Technical procedure reference |
| 3 | SANS Pen Test Rules of Engagement Worksheet | https://www.sans.org/posters/pen-test-rules-of-engagement-worksheet | ROE worksheet |
| 4 | Microsoft Security Testing Rules of Engagement | https://www.microsoft.com/en-us/msrc/pentest-rules-of-engagement | Example ROE for security testing against defined assets |
| 5 | FedRAMP Penetration Test Guidance | https://www.fedramp.gov/resources/documents/ | Search for penetration test guidance and ROE template in FedRAMP documents |

## 14.2 Suggested ROE Template

```md
# Penetration Test Rules of Engagement

## Document Control

| Field | Value |
|---|---|
| Client / Owner | |
| Testing Team | |
| Version | |
| Approval Date | |
| Testing Window | |

## Authorization

## Scope

### In-Scope Assets

### Out-of-Scope Assets

## Objectives

## Allowed Testing Activities

## Prohibited Activities

## Testing Window

## Rate Limits

## Credential Handling

## Data Handling

## Third-Party Systems

## Communication Channel

## Emergency Stop Procedure

## Escalation Contacts

## Evidence Handling

## Reporting Requirements

## Sign-Off
```

Use for Asep:

```text
Check whether security validation has authorized scope.
Check whether active scan or pentest request has ROE.
Block testing requests without authorization.
```

Restrictions:

```text
Asep does not perform pentest.
Asep does not approve ROE.
Human Owner approves ROE.
Runner executes only approved validation.
```

---

# 15. Suggested Knowledge Routing

Suggested file:

```text
config/asep_knowledge_routing.yaml
```

```yaml
asep_knowledge_routing:
  "app/web":
    - OWASP WSTG
    - OWASP ASVS
    - CWE
    - CAPEC

  "app/api":
    - OWASP API Security Top 10
    - OWASP ASVS
    - OWASP WSTG
    - CWE

  "app/auth":
    - OWASP ASVS
    - OWASP WSTG
    - OWASP API Security Top 10
    - CWE

  "app/uploads":
    - OWASP WSTG
    - OWASP ASVS
    - CWE
    - CAPEC

  "requirements.txt":
    - NVD CVE
    - CISA KEV
    - CWE Top 25
    - CVSS scoring guide

  "pyproject.toml":
    - NVD CVE
    - CISA KEV
    - CWE Top 25
    - CVSS scoring guide

  "security/reports":
    - vulnerability report template
    - CVSS scoring guide
    - CWE
    - CISA KEV

  "security/test-cases":
    - security test case template
    - OWASP ASVS
    - OWASP WSTG
    - OWASP API Security Top 10

  "security/roe":
    - pentest rules of engagement template
    - PTES
    - SANS ROE worksheet
```

---

# 16. Suggested Chroma Collection

Collection:

```text
asep_security_knowledge
```

Metadata for defensive references:

```json
{
  "agent": "asep",
  "source_type": "security_reference",
  "allowed_use": "defensive_review",
  "runtime_dependency": false,
  "can_execute": false,
  "risk": "low",
  "topic": "owasp_asvs"
}
```

Metadata for active testing references:

```json
{
  "agent": "asep",
  "source_type": "active_testing_reference",
  "allowed_use": "scope_and_request_only",
  "runtime_dependency": false,
  "can_execute": false,
  "requires_runner": true,
  "requires_human_approval": true,
  "risk": "high"
}
```

Metadata for vulnerability intelligence:

```json
{
  "agent": "asep",
  "source_type": "vulnerability_intelligence",
  "allowed_use": "enrichment_only",
  "runtime_dependency": false,
  "can_execute": false,
  "cache_required": true,
  "risk": "medium"
}
```

---

# 17. Suggested Local Files

```text
config/asep_knowledge_routing.yaml
config/asep_guardrails.yaml
config/asep_reference_policy.yaml
data/agent_workspace/security/
data/agent_workspace/security/test_cases/
data/agent_workspace/security/reports/
data/agent_workspace/security/roe/
data/agent_workspace/requests/
data/agent_workspace/errors/
data/agent_workspace/performance/
```

---

# 18. Ranking Referensi untuk Asep

| Priority | Reference | Value for Asep | Status |
|---:|---|---|---|
| 1 | OWASP ASVS | Security verification requirement baseline | Core knowledge |
| 2 | OWASP WSTG | Web security testing and reporting | Core knowledge |
| 3 | OWASP API Security Top 10 | API risk categories | Core knowledge |
| 4 | MITRE CWE Top 25 / CWE | Weakness classification | Core taxonomy |
| 5 | NVD CVE | Vulnerability intelligence | Controlled lookup |
| 6 | CISA KEV | Exploited vulnerability prioritization | Controlled lookup |
| 7 | FIRST CVSS | Severity scoring support | Core scoring reference |
| 8 | MITRE CAPEC | Attack pattern context | Context only |
| 9 | MITRE ATT&CK Enterprise | Threat behavior context | Context only |
| 10 | OWASP Risk Rating | Risk rating support | Supporting reference |
| 11 | PTES / SANS ROE | Rules of engagement | Authorization and scope reference |
| 12 | Security test case templates | Test case writing | Template reference |
| 13 | Vulnerability report templates | Finding report writing | Template reference |

---

# 19. Final Policy

Asep uses these links as **defensive security knowledge**, not as automatic authority to test live systems.

```text
Asep reviews.
Asep classifies.
Asep maps findings.
Asep writes reports.
Asep requests validation.
Asep blocks unsafe changes.
Asep does not execute attacks.
```

Hard boundary:

```text
No exploit.
No payload.
No scanner execution.
No brute force.
No live target testing without ROE.
No shell.
No patch.
No commit.
No push.
No .env modification.
No Safety Gate bypass.
No Senior Reviewer bypass.
```
