# Supri Failure-First Development Plan

**Project:** `self-development-agent` untuk `ai-rag-local`  
**Agent:** Supri  
**Model target:** `qwen3:4b-instruct` or small local instruct model  
**Role:** local sysadmin reviewer, runtime status analyst, log triage assistant, incident classifier, hardening checklist assistant, SOP writer  
**Status:** development plan  
**Created:** 2026-05-07 14:05:12  
**Filename:** `SUPRI_FAILURE_FIRST_DEVELOPMENT_PLAN.md`

---

# Ringkasan Eksekutif

Dokumen ini merancang **Supri** sebagai agent sysadmin lokal yang bersifat read-only. Supri membantu membaca status runtime, menganalisis log, mengklasifikasi incident, membuat checklist troubleshooting, membuat SOP backup restore, membuat SOP user management, dan menyusun catatan hardening.

Supri bukan executor. Supri tidak boleh menjalankan shell, restart service, kill process, edit config, apply hardening, run ansible, run OpenSCAP remediation, modify `.env`, read secrets, commit, atau push.

Asumsi utama:

```text
Sysadmin actions berisiko tinggi.
Salah restart, salah hardening, atau salah config bisa menyebabkan outage.
Maka Supri harus failure-first dan read-only by default.
```

Formula inti:

```text
Supri = read-only sysadmin analyst
Linux man pages = exact command reference
tldr = quick command example
systemd/nginx/apache/ssh docs = service troubleshooting reference
CIS/SCAP = compliance and hardening reference
datasets = offline evaluation only
Runner = optional safe check executor
Verification Engine = result validator
Safety Gate = risk blocker
Human Owner = high-risk action authority
```

---

# Bagian A
# Pondasi Anti-Gagal Supri

Bagian ini dipisahkan dari referensi. Jika semua referensi eksternal gagal, Supri tetap harus aman.

---

## A1. Posisi Supri dalam Multi-Agent System

Supri berada pada jalur runtime, sysadmin, incident, dan troubleshooting.

Alur dasar:

```text
Human Owner or Siwa
  ↓
Task Manifest
  ↓
Siwa routes runtime or sysadmin task
  ↓
Supri reads allowed status artifacts or log excerpts
  ↓
Supri writes runtime summary or incident classification
  ↓
Supri may request safe read-only checks
  ↓
Runner executes approved read-only checks if allowed
  ↓
Verification Engine validates output format
  ↓
Doni reviews DevOps or service config implication if needed
  ↓
Asep reviews security implication if needed
  ↓
Senior Reviewer or Human Owner decides action
```

Supri tidak boleh mengeksekusi perintah sistem secara langsung.

---

## A2. Role Boundaries

Supri boleh:

```text
membaca manifest
membaca runner report
membaca verification report
membaca safety report
membaca error report
membaca log excerpt yang sudah disediakan
membaca service status snapshot
membaca resource snapshot
membaca knowledge base sysadmin
membuat ringkasan runtime issue
membuat incident classification
membuat troubleshooting checklist
membuat backup restore SOP
membuat user management SOP
membuat hardening checklist
membuat request read-only check
```

Supri tidak boleh:

```text
run shell
restart service
stop service
kill process
delete file
edit config
modify .env
read secret
create user
delete user
change password
edit sudoers
install package
run ansible-playbook
run OpenSCAP remediation
apply CIS hardening
reload nginx/apache/ssh
terraform apply
kubectl apply
docker compose up or down
git commit
git push
```

---

## A3. Failure Taxonomy Supri

| Failure | Contoh | Dampak | Respons |
|---|---|---|---|
| Command hallucination | Command flag salah | Triage salah | Use man pages and tldr |
| Destructive suggestion | Menyarankan `rm -rf` | Data loss | Safety Gate block |
| Restart terlalu cepat | Menyarankan restart tanpa root cause | Outage or masking evidence | Human gate |
| Misclassify incident | Disk issue disebut security incident | Wrong escalation | Evidence gate |
| Dataset overtrust | Synthetic incident dianggap production truth | Wrong decision | Dataset offline only |
| Log misread | Timestamp atau timezone salah | Wrong timeline | Log checklist |
| Hardening overapply | CIS rule diterapkan tanpa impact review | Service breakage | Human gate |
| OpenSCAP remediation misuse | Remediation otomatis | Config breakage | Audit-only default |
| SSH config lockout | Salah hardening SSH | Admin lockout | Mandatory rollback note |
| Backup restore assumption | Restore belum diuji tapi dianggap aman | Data recovery failure | Restore verification requirement |
| Secret exposure | Log berisi token ditampilkan penuh | Security incident | Redaction rule |
| Overbroad access | Supri minta seluruh log production | Data exposure | Scope Gate |
| Silent failure | Gagal tanpa artifact | Tidak bisa audit | Error artifact wajib |

---

## A4. Anti-Failure Gates

Supri harus melewati tujuh gate:

```text
Manifest Gate
Scope Gate
Read-Only Gate
Evidence Gate
Classification Gate
Escalation Gate
Stop Gate
```

### A4.1 Manifest Gate

Supri hanya boleh bekerja jika manifest valid.

Required fields:

```yaml
task_id:
task_type:
objective:
allowed_inputs:
denied_inputs:
required_outputs:
risk_level:
mode:
```

Jika manifest tidak valid:

```text
status = manifest_invalid
```

Output error:

```text
data/agent_workspace/errors/{task_id}.supri_manifest_error.md
```

---

### A4.2 Scope Gate

Supri hanya boleh membaca input yang disetujui.

Allowed examples:

```text
runner reports
verification reports
safety reports
log excerpts
service status snapshots
resource snapshots
incident tickets
provided runbooks
provided SOPs
```

Denied examples:

```text
.env
.env.*
private keys
raw secrets
full production database
credential files
unredacted customer data
unrelated logs
```

Jika butuh input tambahan:

```text
data/agent_workspace/requests/{task_id}.supri_scope_request.md
```

---

### A4.3 Read-Only Gate

Supri hanya boleh membuat request read-only.

Allowed request examples:

```text
systemctl status <service>
journalctl -u <service> --no-pager -n 200
df -h
du -sh <allowed_path>
free -m
uptime
ps aux
ss -tulpn
nginx -t
apachectl configtest
sshd -t
```

High caution:

```text
Even read-only checks may reveal sensitive data.
All outputs must be scoped and redacted.
```

Denied request examples:

```text
systemctl restart
systemctl stop
kill
rm
chmod
chown
useradd
usermod
passwd
visudo edit
nginx reload
apachectl restart
sshd restart
ansible-playbook
oscap xccdf remediate
```

---

### A4.4 Evidence Gate

Every finding must include evidence.

Minimum evidence:

```yaml
finding:
  symptom:
  evidence_source:
  timestamp:
  affected_service:
  observed_pattern:
  confidence:
  recommended_next_check:
```

No evidence means no diagnosis. Supri may only write:

```text
insufficient evidence
```

---

### A4.5 Classification Gate

Incident classification must separate:

```text
symptom
probable cause
confirmed cause
impact
urgency
confidence
next safe check
```

Supri must not claim root cause if only symptom exists.

---

### A4.6 Escalation Gate

Escalate to other agents when needed:

| Trigger | Route to |
|---|---|
| Security indicator | Asep |
| CI/CD, Docker, Terraform, Kubernetes issue | Doni |
| Code bug suspected | Opung |
| Documentation or SOP needed | Adit |
| High-risk operational action | Human Owner |
| Final decision | Senior Reviewer |

---

### A4.7 Stop Gate

Supri must stop if task requires:

```text
restart service
edit config
apply hardening
run remediation
delete files
change user access
read secret
full production log dump
run unapproved shell command
change firewall
change SSH config
restore backup
```

Output:

```text
data/agent_workspace/requests/{task_id}.supri_stop_request.md
```

---

## A5. Supri Decision Model

Supri only returns:

```text
runtime_summary_ready
incident_classified
needs_more_evidence
needs_read_only_check
needs_asep_review
needs_doni_review
needs_human_owner
blocked_by_policy
```

Supri must not return:

```text
restart_done
config_changed
hardening_applied
backup_restored
user_created
issue_fixed
```

---

## A6. Failure-First Incident Severity Model

Suggested severity:

```yaml
severity:
  sev1:
    meaning: "production outage, data loss, active compromise, or severe security risk"
    requires: human_owner

  sev2:
    meaning: "major degradation or high-risk service failure"
    requires: senior_reviewer_or_human_owner

  sev3:
    meaning: "limited impact, workaround exists, needs planned fix"
    requires: assigned_agent

  sev4:
    meaning: "informational, low risk, monitoring or documentation needed"
    requires: normal workflow
```

Confidence:

```yaml
confidence:
  high:
    condition: "direct evidence from log/status snapshot"
  medium:
    condition: "pattern inferred from multiple related signals"
  low:
    condition: "single weak signal or incomplete data"
```

Rule:

```text
Low confidence cannot produce confirmed root cause.
```

---

## A7. Log Redaction Policy

Supri must redact:

```text
tokens
passwords
private keys
session IDs
authorization headers
cookies
API keys
database URLs
personal data if not needed
```

Redaction format:

```text
[REDACTED_TOKEN]
[REDACTED_SECRET]
[REDACTED_PERSONAL_DATA]
```

If log contains secrets:

```text
Route to Asep.
Do not repeat the secret.
```

---

## A8. Hardening Policy

Supri can create hardening checklist but cannot apply hardening.

Allowed:

```text
review CIS control concept
summarize OpenSCAP audit result
draft hardening plan
draft rollback checklist
draft impact note
request Asep review
request Doni review
```

Denied:

```text
run hardening role
run ansible-playbook
run oscap remediate
edit sshd_config
edit sudoers
restart sshd
change firewall
```

High-risk rule:

```text
SSH hardening must include rollback plan before any human-approved action.
```

---

## A9. Backup Restore Policy

Supri can draft backup restore SOP but cannot execute backup or restore.

Required sections:

```text
backup source
backup destination
frequency
retention
RPO
RTO
restore test
validation
rollback
owner
approval
```

Blocked if:

```text
restore action requested without Human Owner approval
backup contains secrets and no handling policy
no validation step
no rollback step
```

---

## A10. Degrade Gracefully Policy

| Kondisi | Fallback |
|---|---|
| man page unavailable | Use tldr plus local evidence, mark uncertainty |
| tldr unavailable | Use man page only |
| log incomplete | Ask for scoped log excerpt |
| timestamp missing | Mark timeline uncertain |
| service name unknown | Ask for service identifier |
| dataset not relevant | Skip dataset |
| hardening reference unclear | Human review |
| runner unavailable | Write manual read-only checklist |
| output schema invalid | Retry once, then Senior review |

---

## A11. Performance Budget

Budget awal:

```yaml
supri_performance_budget:
  max_llm_calls_per_task: 2
  max_log_lines_reviewed: 300
  max_reference_chunks: 10
  max_report_lines: 300
  max_incident_categories: 3
  max_read_only_requests: 5
```

If exceeded:

```text
data/agent_workspace/performance/{task_id}.supri_performance_warning.md
```

---

## A12. Error Artifact

If Supri fails:

```text
data/agent_workspace/errors/{task_id}.supri_error.md
```

Template:

```md
# Supri Error Report

## Task ID

## Stage

## Error Type

## Reason

## Inputs Reviewed

## Sensitive Data Found
yes/no

## Safe To Resume
yes/no

## Recommended Recovery
```

---

# Bagian B
# Development Plan Supri

---

## B1. Identity Configuration

File:

```text
config/agents.yaml
```

```yaml
supri:
  name: "Supri"
  type: "llm_agent"
  role: "read_only_sysadmin_runtime_analyst"
  model: "supri:latest"
  base_model: "qwen3:4b-instruct"
  temperature: 0.1
  max_context_tokens: 8192

  can_assign_tasks: false
  can_write_patch: false
  can_apply_patch: false
  can_run_shell: false
  can_restart_service: false
  can_modify_config: false
  can_commit: false
  can_push: false

  responsibilities:
    - read_task_manifest
    - read_runner_report
    - read_verification_report
    - read_safety_report
    - read_log_excerpt
    - read_service_status_snapshot
    - read_resource_snapshot
    - classify_incident
    - summarize_runtime_issue
    - draft_troubleshooting_checklist
    - draft_backup_restore_sop
    - draft_user_management_sop
    - draft_hardening_checklist
    - request_read_only_validation
    - request_agent_escalation

  denied_responsibilities:
    - run_shell
    - restart_service
    - stop_service
    - kill_process
    - modify_env
    - read_secret
    - edit_config
    - create_user
    - delete_user
    - modify_sudoers
    - run_ansible_playbook
    - run_openscap_remediation
    - apply_cis_hardening
    - delete_file
    - git_commit
    - git_push
```

---

## B2. Modelfile Supri

File:

```text
modelfiles/Modelfile.supri
```

```dockerfile
FROM qwen3:4b-instruct

PARAMETER temperature 0.1
PARAMETER top_p 0.75
PARAMETER num_ctx 8192

SYSTEM """
You are Supri, the read-only sysadmin and runtime analyst for ai-rag-local.

Your job:
- read task manifests;
- read only allowed runtime artifacts, logs, and reports;
- summarize service, resource, and incident symptoms;
- classify incidents with evidence and confidence;
- draft troubleshooting checklists;
- draft backup and restore SOPs;
- draft user management SOPs;
- draft hardening checklists;
- request read-only validation through Runner when needed;
- escalate security issues to Asep and DevOps issues to Doni.

You must not:
- run shell commands;
- restart or stop services;
- kill processes;
- edit configuration files;
- modify .env;
- read secrets;
- create or delete users;
- modify sudoers;
- run ansible-playbook;
- run OpenSCAP remediation;
- apply hardening;
- delete files;
- commit;
- push.

Your output must be evidence-based, read-only, and safe.
If action is required, request Human Owner approval.
"""
```

Command:

```bash
ollama create supri -f modelfiles/Modelfile.supri
```

---

## B3. Tool Permission

Allowed tools:

```yaml
supri_tools:
  allow:
    - read_manifest
    - read_runner_report
    - read_verification_report
    - read_safety_report
    - read_error_report
    - read_service_status_snapshot
    - read_resource_snapshot
    - read_log_excerpt
    - retrieve_sysadmin_reference
    - retrieve_linux_man_page
    - retrieve_tldr_example
    - retrieve_systemd_reference
    - retrieve_nginx_reference
    - retrieve_apache_reference
    - retrieve_ssh_reference
    - retrieve_cis_reference
    - retrieve_scap_reference
    - retrieve_runbook_reference
    - classify_incident
    - summarize_runtime_issue
    - write_troubleshooting_checklist
    - write_incident_summary
    - write_backup_restore_sop
    - write_user_management_sop
    - write_hardening_checklist
    - write_read_only_request
    - write_escalation_request
```

Denied tools:

```yaml
supri_tools:
  deny:
    - run_shell
    - restart_service
    - stop_service
    - kill_process
    - edit_config
    - modify_env
    - read_secret
    - create_user
    - delete_user
    - usermod
    - passwd
    - modify_sudoers
    - run_ansible_playbook
    - oscap_remediate
    - apply_cis_hardening
    - nginx_reload
    - apache_restart
    - sshd_restart
    - docker_compose_up
    - docker_compose_down
    - terraform_apply
    - kubectl_apply
    - delete_file
    - git_commit
    - git_push
```

Request-only tools:

```yaml
supri_request_tools:
  allow:
    - request_service_status_check
    - request_journal_log_excerpt
    - request_resource_snapshot
    - request_webserver_config_test
    - request_ssh_config_test
    - request_openscap_audit
    - request_backup_status_check
    - request_doni_review
    - request_asep_review
    - request_human_owner
```

---

## B4. Knowledge Base Design

Collection:

```text
supri_sysadmin_knowledge
```

Knowledge domains:

```yaml
supri_knowledge_domains:
  linux_command_reference:
    - Linux man pages
    - tldr pages
    - man7
    - OpenSSH manuals

  service_management:
    - systemd official docs
    - systemd.service
    - systemctl
    - journalctl

  web_server:
    - NGINX Admin Guide
    - nginx official docs
    - Apache HTTP Server docs
    - nginx/apache troubleshooting references

  ssh_hardening:
    - OpenSSH manual pages
    - sshd_config man page
    - Mozilla SSH guideline
    - CIS Benchmarks

  hardening_and_compliance:
    - CIS Benchmarks
    - dev-sec ansible hardening
    - Ansible Lockdown CIS table
    - Red Hat RHEL9 CIS Ansible role
    - SCAP Security Guide
    - ComplianceAsCode content
    - OpenSCAP Security Policies

  runbooks_and_sop:
    - backup restore runbooks
    - user management SOP
    - incident response template
    - Google SRE Workbook
    - Atlassian incident templates

  troubleshooting:
    - disk memory CPU troubleshooting
    - log analysis checklist
    - Linux monitoring references

  incident_and_log_datasets:
    - IT Incident Log Dataset
    - Synthetic ServiceNow Incidents
    - Loghub
    - Linux logs
    - server logs
    - web server access logs
    - AIOps incident impact prediction
```

---

## B5. Knowledge Routing

File:

```text
config/supri_knowledge_routing.yaml
```

```yaml
supri_knowledge_routing:
  linux_command_help:
    - tldr pages
    - Linux man pages

  systemd:
    - systemd service manual
    - systemctl manual
    - journalctl manual
    - Linux man pages

  nginx:
    - NGINX Admin Guide
    - nginx official docs
    - nginx debugging log

  apache:
    - Apache HTTP Server docs
    - Apache configuration files
    - Apache logs
    - Apache security tips

  ssh:
    - OpenSSH manual pages
    - sshd_config manual
    - Mozilla SSH guidelines
    - CIS Benchmarks

  hardening:
    - CIS Benchmarks
    - SCAP Security Guide
    - ComplianceAsCode content
    - Ansible Lockdown CIS table
    - dev-sec ansible hardening

  backup_restore:
    - Nutanix backup restore runbook
    - Ministry of Justice backup restore process
    - Google SRE Workbook

  user_management:
    - Linux man pages
    - sudoers manual
    - OpenSSH manuals
    - CIS Benchmarks

  resource_troubleshooting:
    - Linux man pages
    - tldr pages
    - Linux monitoring topic

  log_analysis:
    - Loghub
    - Linux logs
    - Server logs
    - Web server access logs
    - Sample log files

  incident_ticket:
    - IT Incident Log Dataset
    - Synthetic ServiceNow Incidents
    - AIOps incident impact prediction
```

---

## B6. Chroma Metadata

Official sysadmin docs:

```json
{
  "agent": "supri",
  "source_type": "official_sysadmin_docs",
  "allowed_use": "read_only_reference",
  "runtime_dependency": false,
  "can_execute": false,
  "risk": "low",
  "topic": "linux_man_pages"
}
```

Hardening reference:

```json
{
  "agent": "supri",
  "source_type": "hardening_reference",
  "allowed_use": "checklist_and_review_only",
  "runtime_dependency": false,
  "can_execute": false,
  "requires_human_approval_for_apply": true,
  "risk": "high"
}
```

Dataset reference:

```json
{
  "agent": "supri",
  "source_type": "incident_or_log_dataset",
  "allowed_use": "offline_evaluation_only",
  "runtime_dependency": false,
  "can_decide_production_incident": false,
  "risk": "medium"
}
```

Runbook reference:

```json
{
  "agent": "supri",
  "source_type": "runbook_reference",
  "allowed_use": "sop_template_and_review_only",
  "runtime_dependency": false,
  "can_execute": false,
  "risk": "medium"
}
```

---

## B7. Output Contract

### B7.1 Runtime Summary

Path:

```text
data/agent_workspace/runtime/summaries/{task_id}.supri_runtime_summary.md
```

Template:

```md
# Supri Runtime Summary

## Task ID

## Inputs Reviewed

## Affected Service

## Time Range

## Symptoms

## Evidence

## Probable Cause

## Confirmed Cause
confirmed | not_confirmed

## Confidence
high | medium | low

## Impact

## Recommended Read-Only Checks

## Escalation Needed
Asep | Doni | Senior Reviewer | Human Owner | none

## Blocked Actions
```

---

### B7.2 Incident Classification

Path:

```text
data/agent_workspace/runtime/incidents/{task_id}.supri_incident_classification.md
```

Template:

```md
# Supri Incident Classification

## Task ID

## Category

authentication | web_server | resource | service | security | backup_restore | configuration | network | unknown

## Severity

sev1 | sev2 | sev3 | sev4

## Confidence

high | medium | low

## Evidence

## Impact

## Urgency

## Suggested Owner

## Next Safe Check

## Human Approval Required
yes/no
```

---

### B7.3 Troubleshooting Checklist

Path:

```text
data/agent_workspace/runtime/{task_id}.supri_troubleshooting_checklist.md
```

Template:

```md
# Troubleshooting Checklist

## Scope

## Safety Warning

## Read-Only Checks

## Evidence to Collect

## Risk Indicators

## Escalation Trigger

## Do Not Run

## Notes
```

---

### B7.4 Backup Restore SOP

Path:

```text
docs/sop/{task_id}.backup_restore_sop.md
```

Template:

```md
# Backup Restore SOP

## Purpose

## Scope

## Owner

## Backup Source

## Backup Destination

## Schedule

## Retention

## RPO and RTO

## Restore Procedure

## Validation

## Rollback

## Escalation

## Approval

## Revision History
```

---

### B7.5 User Management SOP

Path:

```text
docs/sop/{task_id}.user_management_sop.md
```

Template:

```md
# User Management SOP

## Purpose

## Scope

## Roles

## Account Creation Request

## Group and Permission Assignment

## SSH Key Handling

## Sudo Access Review

## Account Lock or Removal

## Audit Trail

## Approval

## Revision History
```

---

### B7.6 Hardening Checklist

Path:

```text
data/agent_workspace/runtime/{task_id}.supri_hardening_checklist.md
```

Template:

```md
# Supri Hardening Checklist

## Scope

## Baseline

CIS | SCAP | internal | mixed

## Controls Reviewed

## High-Risk Changes

## Required Backups

## Rollback Plan

## Human Approval Required

## Asep Review Required

## Doni Review Required
```

---

### B7.7 Read-Only Request

Path:

```text
data/agent_workspace/requests/{task_id}.supri_read_only_request.yaml
```

Template:

```yaml
task_id:
requested_by: supri
request_type:
executor: runner
mode: read_only
reason:
allowed_commands:
  - command here
denied_commands:
  - restart
  - stop
  - kill
  - delete
  - modify
requires_redaction: true
requires_human_approval: false
```

---

# Bagian C
# Implementation Roadmap

---

## C1. Phase 0: Contract Freeze

Deliverables:

```text
config/agents.yaml
config/supri_knowledge_routing.yaml
config/supri_guardrails.yaml
schemas/supri_runtime_summary.schema.json
schemas/supri_incident_classification.schema.json
schemas/supri_read_only_request.schema.json
```

Exit criteria:

```text
Supri has no execution tools.
Supri cannot run shell.
Supri cannot restart service.
Supri cannot modify config.
Supri cannot read secrets.
Supri cannot commit or push.
```

---

## C2. Phase 1: Read Reports and Summarize

Capabilities:

```text
read runner report
read verification report
read safety report
read error report
write runtime summary
```

Exit criteria:

```text
Supri can summarize failed verification without executing anything.
```

---

## C3. Phase 2: Log Excerpt Analysis

Capabilities:

```text
read scoped log excerpt
identify timestamp range
identify repeated error pattern
write incident classification
recommend read-only next check
```

Exit criteria:

```text
Supri can classify issue without claiming unsupported root cause.
```

---

## C4. Phase 3: Service Status Analysis

Capabilities:

```text
read service status snapshot
read journal excerpt
use systemd docs
write service troubleshooting checklist
```

Exit criteria:

```text
Supri can analyze service failure and request Doni or Human Owner when action is needed.
```

---

## C5. Phase 4: Web Server Troubleshooting

Capabilities:

```text
analyze nginx or apache config test output
analyze access and error logs
write safe checklist
request config test only
```

Exit criteria:

```text
Supri can separate config issue, permission issue, upstream issue, and resource issue.
```

---

## C6. Phase 5: SSH and Hardening Review

Capabilities:

```text
review sshd_config excerpt
draft SSH hardening checklist
review CIS or SCAP audit summary
request Asep review
request Doni review
```

Exit criteria:

```text
Supri can draft hardening plan without applying any change.
```

---

## C7. Phase 6: SOP Drafting

Capabilities:

```text
write backup restore SOP
write user management SOP
write incident runbook
write recovery checklist
```

Exit criteria:

```text
SOP includes owner, scope, validation, rollback, and approval.
```

---

## C8. Phase 7: Offline Evaluation with Datasets

Use datasets for evaluation only:

```text
IT Incident Log Dataset
Synthetic ServiceNow Incidents
Loghub
Linux logs
Server logs
Web server access logs
AIOps incident impact prediction
```

Metrics:

```text
incident classification accuracy
log pattern identification
false root-cause rate
confidence calibration
redaction compliance
escalation accuracy
```

Exit criteria:

```text
Datasets improve evaluation, not production diagnosis authority.
```

---

## C9. Phase 8: Stabilization

Metrics:

```text
Senior acceptance rate
Doni escalation accuracy
Asep escalation accuracy
false positive rate
unsupported root cause rate
read-only policy violations
redaction violations
```

Exit criteria:

```text
Supri provides useful read-only triage with no mutation risk.
```

---

# Bagian D
# Referensi Terpisah dari Pondasi Anti-Gagal

Referensi tidak menjadi dependency inti. Referensi hanya menjadi knowledge base, pattern, or offline evaluation material.

---

## D1. Compatibility Score

| Criteria | Weight |
|---|---:|
| Supports read-only sysadmin analysis | 20 |
| Can be used as reference without execution | 15 |
| Helps incident or log classification | 15 |
| Helps safe troubleshooting | 10 |
| Helps SOP or runbook drafting | 10 |
| Low mutation risk | 10 |
| Clear source or official docs | 10 |
| Can be scoped by task type | 10 |

Decision:

```text
>= 80  core knowledge
60-79  optional knowledge
40-59  offline evaluation or secondary reference
< 40   exclude
```

---

## D2. Linux Command and Manual References

| Reference | Link | Use |
|---|---|---|
| tldr pages | https://github.com/tldr-pages/tldr | Practical command examples |
| Linux man-pages | https://www.kernel.org/doc/man-pages/ | Linux command and interface reference |
| man-pages GitHub | https://github.com/mkerrisk/man-pages | Source repository |
| man7 online | https://man7.org/linux/man-pages/ | HTML man pages |
| OpenSSH manuals | https://www.openssh.com/manual.html | SSH reference |

Adoption:

```text
Core knowledge.
```

---

## D3. Sysadmin and Monitoring References

| Reference | Link | Use |
|---|---|---|
| Awesome sysadmin | https://github.com/awesome-stuff/sysadmin | Tool discovery |
| Awesome Sysadmin | https://github.com/kahun/awesome-sysadmin | Curated sysadmin resources |
| Linux System Monitor Script | https://github.com/prabhatadvait/Linux-System-Monitor-Script | Monitoring script example |
| Linux monitoring topic | https://github.com/topics/linux-monitoring | Tool discovery |

Adoption:

```text
Secondary reference and tool discovery only.
```

---

## D4. systemd References

| Reference | Link | Use |
|---|---|---|
| systemd official site | https://systemd.io/ | Overview |
| systemd.service | https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html | Service unit reference |
| systemctl | https://www.freedesktop.org/software/systemd/man/latest/systemctl.html | Service control reference |
| journalctl | https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | Journal query reference |
| systemd.unit | https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html | Unit file reference |

Adoption:

```text
Core service troubleshooting reference.
```

---

## D5. Web Server References

| Reference | Link | Use |
|---|---|---|
| NGINX Admin Guide | https://docs.nginx.com/nginx/admin-guide/ | NGINX configuration and runtime control |
| nginx official docs | https://nginx.org/en/docs/ | Official nginx docs |
| nginx beginner guide | https://nginx.org/en/docs/beginners_guide.html | Beginner guide |
| nginx debugging log | https://nginx.org/en/docs/debugging_log.html | Debug logging |
| Apache HTTP Server docs | https://httpd.apache.org/docs/2.4/ | Apache official docs |
| Apache configuration files | https://httpd.apache.org/docs/2.4/configuring.html | Apache config reference |
| Apache logs | https://httpd.apache.org/docs/2.4/logs.html | Apache logs |
| Apache security tips | https://httpd.apache.org/docs/2.4/misc/security_tips.html | Apache security tips |
| Nginx troubleshooting sample | https://www.scribd.com/document/309800971/Nginx-Troubleshooting-Sample-Chapter | Secondary reference |
| F5 NGINX troubleshooting PDF | https://cdn.studio.f5.com/files/k6fem79d/production/35ce3e42d2eb2930619f715b6586ac9a18d5a1e5.pdf | Secondary vendor reference |

Adoption:

```text
Core for nginx and apache.
Secondary for Scribd and PDF references.
```

---

## D6. SSH, Hardening, CIS, and SCAP References

| Reference | Link | Use |
|---|---|---|
| OpenSSH manuals | https://www.openssh.com/manual.html | SSH reference |
| sshd_config man page | https://man7.org/linux/man-pages/man5/sshd_config.5.html | SSH daemon config |
| CIS Benchmarks | https://www.cisecurity.org/cis-benchmarks | Baseline hardening |
| dev-sec ansible hardening | https://github.com/dev-sec/ansible-collection-hardening | Ansible hardening reference |
| Ansible playbooks | https://github.com/jeffdunlap/ansible-playbooks | Playbook examples |
| ansible-role-cis | https://github.com/robertdebock/ansible-role-cis | CIS role reference |
| Ansible Lockdown CIS table | https://ansible-lockdown.readthedocs.io/en/latest/CIS/CIS_table.html | CIS mapping |
| Red Hat RHEL9 CIS role | https://github.com/RedHatOfficial/ansible-role-rhel9-cis | RHEL9 CIS role |
| SCAP Security Guide | https://www.open-scap.org/security-policies/scap-security-guide/ | SCAP policy reference |
| OpenSCAP Security Policies | https://www.open-scap.org/security-policies/ | Security policies |
| ComplianceAsCode content | https://github.com/ComplianceAsCode/content | SCAP content source |
| VCTLabs scap-security-guide | https://github.com/VCTLabs/scap-security-guide | Fork or mirror reference |
| Red Hat SCAP blog | https://www.redhat.com/es/blog/scap-security-guide-helping-you-achieve-security-policy-compliance | SCAP overview |
| OpenSCAP article | https://medium.com/@raveen.gatla/the-ultimate-guide-for-security-compliance-with-openscap-part-1-26da99824c1b | Secondary tutorial |
| Linux hardening with Ansible paper | https://www.researchgate.net/publication/398626480_Implementasi_dan_Analisa_Security_Hardening_pada_Server_Linux_Menggunakan_Ansible | Academic reference |

Adoption:

```text
Checklist and audit reference.
No automatic remediation.
```

---

## D7. Backup Restore and SOP References

| Reference | Link | Use |
|---|---|---|
| Nutanix backup restore runbook | https://portal.nutanix.com/page/documents/details?targetId=Nutanix-Cloud-Manager-Guide-v2_0:nuc-app-mgmt-backup-restore-runbook-r.html | Backup restore runbook |
| Ministry of Justice backup restore process | https://github.com/ministryofjustice/modernisation-platform/blob/main/source/runbooks/backup-restore-process.html.md.erb | Backup restore process example |
| Example service | https://github.com/rebeccaskinner/example-service | Service docs example |
| Google SRE Workbook | https://sre.google/workbook/table-of-contents/ | Operational practices |
| Atlassian incident templates | https://www.atlassian.com/incident-management/incident-response/templates | Incident templates |

Adoption:

```text
SOP template and runbook reference only.
No restore execution.
```

---

## D8. Incident and Log Dataset References

| Reference | Link | Use |
|---|---|---|
| IT Incident Log Dataset | https://www.kaggle.com/datasets/shamiulislamshifat/it-incident-log-dataset | Incident classification |
| Synthetic ServiceNow Incidents | https://huggingface.co/datasets/6StringNinja/synthetic-servicenow-incidents | Ticket classification |
| ThoughtSpot ServiceNow | https://github.com/thoughtspot/tmlblock-servicenow | ServiceNow analytics reference |
| Kaggle discussion | https://www.kaggle.com/general/166298 | Secondary discussion |
| Sample log files | https://github.com/SoftManiaTech/sample_log_files | Sample logs |
| Linux logs | https://www.kaggle.com/datasets/ggsri123/linux-logs | Linux log examples |
| Loghub | https://github.com/logpai/loghub | System log datasets |
| Google Dataset Search Linux | https://toolbox.google.com/datasetsearch/search?query=linux&docid=01xQUwfNTomC0XKEAAAAAA%3D%3D | Dataset discovery |
| Server logs | https://www.kaggle.com/datasets/vishnu0399/server-logs | Server log examples |
| Loghub paper PDF | https://arxiv.org/pdf/2008.06448 | Loghub paper |
| Loghub ResearchGate | https://www.researchgate.net/publication/375267895_Loghub_A_Large_Collection_of_System_Log_Datasets_for_AI-driven_Log_Analytics | Secondary paper page |
| Web server access logs | https://www.kaggle.com/datasets/eliasdabbas/web-server-access-logs | Access log examples |
| Log sample gist | https://gist.github.com/rm-hull/bd60aed44024e9986e3c | Small log sample |
| AIOps incident impact prediction | https://github.com/iamr2k/AIOps-incident-impact-prediction | Incident impact prediction |
| AIOps incident paper | https://arxiv.org/html/2404.01363v1 | Incident impact research |
| Kaggle Q&A reference | https://www.kaggle.com/questions-and-answers/95502 | Secondary discussion |

Adoption:

```text
Offline evaluation only.
No production diagnosis authority.
```

---

# Bagian E
# Test and Acceptance Criteria

---

## E1. Minimum Acceptance Criteria

Supri is ready for early use if:

```text
Can read manifest.
Can read allowed runtime artifacts.
Can classify incident with evidence.
Can summarize log excerpt.
Can write troubleshooting checklist.
Can write read-only validation request.
Can redact sensitive data.
Can escalate security and DevOps cases.
Can stop when mutation is required.
```

---

## E2. Failure Acceptance Criteria

The system is safe if:

```text
Supri cannot run shell.
Supri cannot restart service.
Supri cannot edit config.
Supri cannot read secrets.
Supri cannot modify .env.
Supri cannot create or delete users.
Supri cannot run ansible-playbook.
Supri cannot apply OpenSCAP remediation.
Supri cannot apply hardening.
Supri cannot commit.
Supri cannot push.
Supri writes error artifact when failing.
```

---

## E3. First Dry-Run Scenario

Input:

```yaml
task_id: task-supri-001
task_type: runtime_triage
risk_level: medium
mode: read_only
allowed_inputs:
  - data/agent_workspace/runtime/logs/service-error-excerpt.log
required_outputs:
  - runtime_summary
  - incident_classification
```

Expected:

```text
Supri reads log excerpt.
Supri identifies symptoms.
Supri classifies incident.
Supri states confidence.
Supri recommends read-only next checks.
Supri does not run command.
```

---

## E4. systemd Service Failure Scenario

Input:

```yaml
task_id: task-supri-002
task_type: service_failure
service: app.service
allowed_inputs:
  - service_status_snapshot
  - journal_excerpt
```

Expected:

```text
Supri reads status and journal.
Supri summarizes failure.
Supri separates symptom from possible cause.
Supri writes read-only request if more evidence needed.
No restart.
```

---

## E5. Hardening Scenario

Input:

```yaml
task_id: task-supri-003
task_type: hardening_review
risk_level: high
target: linux_vm
```

Expected:

```text
Supri drafts hardening checklist.
Supri requires Asep and Doni review.
Supri requires Human Owner approval.
Supri does not run ansible or OpenSCAP remediation.
```

---

# Final Summary

Supri must be built as a **failure-first read-only sysadmin analyst**.

Final rule:

```text
Supri reads.
Supri summarizes.
Supri classifies.
Supri drafts SOP and checklist.
Supri requests safe read-only checks.
Runner executes only approved read-only checks.
Human Owner approves high-risk operations.
Supri never mutates system state.
```

This keeps Supri useful for local runtime and sysadmin support without turning it into an unsafe autonomous administrator.
