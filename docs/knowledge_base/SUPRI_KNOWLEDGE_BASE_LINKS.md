# Supri Knowledge Base Links

**Agent:** Supri  
**Role:** local sysadmin reviewer, runtime status analyst, log triage assistant, hardening checklist assistant, runbook drafter  
**Purpose:** knowledge base links untuk Linux command help, man pages, systemd, web server config, SSH hardening, CIS/SCAP hardening, backup restore SOP, user management SOP, disk memory CPU troubleshooting, log analysis, dan incident ticket classification  
**Created:** 2026-05-07 14:05:12  
**Filename:** `SUPRI_KNOWLEDGE_BASE_LINKS.md`

---

# 0. Status Dokumen

Dokumen ini adalah daftar rujukan knowledge base untuk **Supri**.

Supri memakai dokumen ini untuk:

```text
membaca referensi command Linux
membaca manual Linux
menganalisis log
membuat ringkasan incident
membuat checklist troubleshooting
membuat SOP backup restore
membuat SOP user management
membuat catatan hardening Linux
membuat rekomendasi read-only untuk admin
mengusulkan validasi lewat Runner atau Verification Engine
```

Supri tidak boleh memakai rujukan ini sebagai izin untuk:

```text
menjalankan shell langsung
restart service
kill process
modify system config
mengubah user atau permission
membaca secret
mengubah .env
menjalankan ansible-playbook
menerapkan CIS hardening
menjalankan OpenSCAP remediation
menghapus file
deploy service
commit
push
```

Prinsip:

```text
Knowledge base = boleh dibaca
Runtime summary = boleh dibuat
SOP and checklist = boleh dibuat
Execution = Runner atau Human Owner
Validation = Verification Engine
High-risk sysadmin action = Human Owner approval
```

---

# 1. Core Base Knowledge untuk Supri

| Domain | Isi yang perlu dipahami | Fungsi Supri |
|---|---|---|
| Linux man pages | Command, syscall, config manual, file format | Referensi command dan perilaku Linux |
| tldr command examples | Contoh penggunaan command ringkas | Membantu memahami command secara cepat |
| systemd service guide | Unit file, service status, journal, enable/disable concept | Menganalisis service issue secara read-only |
| nginx and Apache config guide | Config file, logs, server blocks, virtual host, reload concept | Menganalisis web server issue |
| SSH hardening guide | `sshd_config`, authentication, key, root login, port, allow users | Membuat checklist hardening, bukan apply |
| CIS Benchmarks | Security baseline per OS | Checklist hardening dan compliance awareness |
| SCAP Security Guide | Automated audit policy, remediation scripts, rules | Compliance reference, request-only |
| Backup restore SOP | Backup scope, schedule, restore test, RPO/RTO | Membuat SOP backup dan restore |
| User management SOP | Account lifecycle, sudo, group, SSH key, offboarding | Membuat SOP user management |
| Disk memory CPU troubleshooting | `df`, `du`, `free`, `top`, `ps`, `journalctl`, `iostat` | Triage resource issue |
| Log analysis checklist | log source, timestamp, severity, pattern, correlation | Membuat ringkasan log |
| Incident ticket classification | severity, category, impact, symptom, root cause candidate | Mengklasifikasi ticket dan incident |
| AIOps and log datasets | Log parsing, anomaly, incident prediction research | Offline evaluation only |

---

# 2. Linux Command and Man Page Knowledge Base

## 2.1 Man Pages and Linux Manual

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Linux man-pages project | https://www.kernel.org/doc/man-pages/ | Linux kernel and C library interface documentation |
| 2 | man-pages GitHub mirror | https://github.com/mkerrisk/man-pages | Source repository for Linux man-pages |
| 3 | man7 Linux man pages online | https://man7.org/linux/man-pages/ | HTML rendering of Linux man pages |
| 4 | OpenSSH manual pages | https://www.openssh.com/manual.html | OpenSSH command and config manuals |
| 5 | sshd_config manual | https://man7.org/linux/man-pages/man5/sshd_config.5.html | SSH daemon configuration reference |

Use for Supri:

```text
Explain command behavior.
Interpret config files.
Check meaning of system calls or file formats.
Support troubleshooting notes.
Avoid command hallucination.
```

Restrictions:

```text
Supri may read man pages.
Supri must not execute commands directly.
Supri must not suggest destructive command as direct action.
```

---

## 2.2 tldr Command Examples

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | tldr-pages GitHub | https://github.com/tldr-pages/tldr | Community-maintained command examples |
| 2 | tldr website | https://tldr.sh/ | Human-friendly command examples |
| 3 | tldr style guide | https://github.com/tldr-pages/tldr/blob/main/contributing-guides/style-guide.md | Command example formatting pattern |

Use for Supri:

```text
Explain common command usage.
Draft read-only command examples.
Produce short command help.
Avoid overlong man-page style output.
```

Restrictions:

```text
Use tldr as convenience reference only.
Prefer man pages for exact behavior.
Do not output destructive command without warning and human approval.
```

---

# 3. Linux Sysadmin Knowledge Base

## 3.1 Awesome Sysadmin and General References

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Awesome sysadmin | https://github.com/awesome-stuff/sysadmin | General sysadmin resources |
| 2 | Awesome Sysadmin | https://github.com/kahun/awesome-sysadmin | Curated sysadmin tools and resources |
| 3 | Linux monitoring topic | https://github.com/topics/linux-monitoring | Linux monitoring repositories and tool discovery |
| 4 | Linux System Monitor Script | https://github.com/prabhatadvait/Linux-System-Monitor-Script | Example Linux system monitoring script |

Use for Supri:

```text
Tool discovery.
Sysadmin topic mapping.
Monitoring checklist inspiration.
Do not use as production authority.
```

Restrictions:

```text
Community lists are not source of truth.
Do not install or run tools automatically.
```

---

## 3.2 Disk, Memory, CPU, and Service Troubleshooting Base Knowledge

Recommended knowledge items:

```text
df
du
free
top
htop
ps
uptime
vmstat
iostat
ss
lsof
journalctl
systemctl
dmesg
sar
tail
grep
awk
sed
find
```

Suggested references:

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Linux man pages | https://man7.org/linux/man-pages/ | Official manual reference |
| 2 | tldr pages | https://github.com/tldr-pages/tldr | Practical examples |
| 3 | systemd documentation | https://systemd.io/ | systemd overview |
| 4 | systemd service man page | https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html | Service unit reference |
| 5 | journalctl man page | https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | Journal log query reference |

Use for Supri:

```text
Create troubleshooting checklist.
Explain likely resource bottleneck.
Interpret log excerpts.
Recommend safe read-only checks.
```

Restrictions:

```text
Supri may not run these commands.
Supri may write a request for Runner or Human Owner.
```

---

# 4. systemd Service Guide

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | systemd official site | https://systemd.io/ | System and service manager overview |
| 2 | systemd service manual | https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html | Unit file reference |
| 3 | systemctl manual | https://www.freedesktop.org/software/systemd/man/latest/systemctl.html | Service control reference |
| 4 | journalctl manual | https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | Logs and journal reference |
| 5 | systemd unit manual | https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html | Unit configuration reference |

Use for Supri:

```text
Analyze service status output.
Explain unit file fields.
Identify service startup failure signals.
Draft service troubleshooting checklist.
```

Restrictions:

```text
No direct systemctl restart.
No direct systemctl enable/disable.
No direct daemon-reload.
Use request-only validation.
```

Suggested request type:

```yaml
supri_request_tools:
  request_service_status_check:
    executor: runner
    allowed_commands:
      - systemctl status <service>
      - journalctl -u <service> --no-pager -n 200
    denied_commands:
      - systemctl restart
      - systemctl stop
      - systemctl disable
```

---

# 5. Nginx and Apache Config Guide

## 5.1 Nginx

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | NGINX Admin Guide | https://docs.nginx.com/nginx/admin-guide/ | NGINX configuration and runtime control |
| 2 | nginx official docs | https://nginx.org/en/docs/ | Official nginx docs |
| 3 | nginx beginner guide | https://nginx.org/en/docs/beginners_guide.html | Basic nginx concepts |
| 4 | nginx debugging log | https://nginx.org/en/docs/debugging_log.html | Debug log reference |
| 5 | Nginx Troubleshooting sample chapter | https://www.scribd.com/document/309800971/Nginx-Troubleshooting-Sample-Chapter | Secondary troubleshooting reference |
| 6 | F5 NGINX troubleshooting PDF | https://cdn.studio.f5.com/files/k6fem79d/production/35ce3e42d2eb2930619f715b6586ac9a18d5a1e5.pdf | Secondary vendor troubleshooting reference |

Use for Supri:

```text
Review nginx config snippets.
Explain common 4xx and 5xx causes.
Check log analysis pattern.
Draft troubleshooting checklist.
```

Restrictions:

```text
No nginx reload.
No nginx restart.
No config write.
No production config change.
```

## 5.2 Apache HTTP Server

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Apache HTTP Server 2.4 docs | https://httpd.apache.org/docs/2.4/ | Official Apache documentation |
| 2 | Apache configuration files | https://httpd.apache.org/docs/2.4/configuring.html | Configuration file reference |
| 3 | Apache logs | https://httpd.apache.org/docs/2.4/logs.html | Log file reference |
| 4 | Apache security tips | https://httpd.apache.org/docs/2.4/misc/security_tips.html | Security configuration tips |
| 5 | Apache virtual hosts | https://httpd.apache.org/docs/2.4/vhosts/ | Virtual host reference |

Use for Supri:

```text
Analyze Apache config.
Explain log paths and error patterns.
Support web server incident summary.
```

Restrictions:

```text
No apachectl restart.
No config mutation.
No module enable/disable.
```

---

# 6. SSH Hardening Guide

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | OpenSSH manual pages | https://www.openssh.com/manual.html | Official OpenSSH manual index |
| 2 | sshd_config manual | https://man7.org/linux/man-pages/man5/sshd_config.5.html | SSH daemon config reference |
| 3 | sshd manual | https://man7.org/linux/man-pages/man8/sshd.8.html | SSH daemon reference |
| 4 | Mozilla SSH guidelines | https://infosec.mozilla.org/guidelines/openssh | SSH configuration guideline |
| 5 | CIS Benchmarks | https://www.cisecurity.org/cis-benchmarks | Security benchmark source |

Use for Supri:

```text
Draft SSH hardening checklist.
Explain config flags.
Review risk from root login, password auth, weak algorithms, users and groups.
Support user management SOP.
```

Restrictions:

```text
Supri may not edit sshd_config.
Supri may not restart sshd.
Human Owner must approve hardening changes.
```

Suggested SSH checklist fields:

```yaml
ssh_hardening_checklist:
  permit_root_login:
  password_authentication:
  pubkey_authentication:
  allow_users_or_groups:
  max_auth_tries:
  client_alive_interval:
  log_level:
  approved_by:
```

---

# 7. CIS Benchmarks, Ansible Hardening, and SCAP

## 7.1 CIS and Ansible Hardening References

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | CIS Benchmarks | https://www.cisecurity.org/cis-benchmarks | Official CIS benchmark source |
| 2 | dev-sec ansible collection hardening | https://github.com/dev-sec/ansible-collection-hardening | Ansible hardening reference |
| 3 | Ansible playbooks examples | https://github.com/jeffdunlap/ansible-playbooks | Playbook example reference |
| 4 | Ansible role CIS | https://github.com/robertdebock/ansible-role-cis | CIS role reference |
| 5 | Ansible Lockdown CIS table | https://ansible-lockdown.readthedocs.io/en/latest/CIS/CIS_table.html | CIS mapping reference |
| 6 | Red Hat RHEL9 CIS Ansible role | https://github.com/RedHatOfficial/ansible-role-rhel9-cis | RHEL9 CIS role reference |
| 7 | ResearchGate Linux hardening with Ansible | https://www.researchgate.net/publication/398626480_Implementasi_dan_Analisa_Security_Hardening_pada_Server_Linux_Menggunakan_Ansible | Academic hardening reference |

Use for Supri:

```text
Draft hardening checklist.
Classify control categories.
Identify hardening impact.
Suggest human-reviewed ansible validation.
```

Restrictions:

```text
No ansible-playbook execution.
No hardening apply.
No automatic CIS remediation.
No production mutation.
```

---

## 7.2 OpenSCAP and SCAP Security Guide

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | SCAP Security Guide | https://www.open-scap.org/security-policies/scap-security-guide/ | SCAP security policy reference |
| 2 | OpenSCAP Security Policies | https://www.open-scap.org/security-policies/ | Policy and rule overview |
| 3 | ComplianceAsCode content | https://github.com/ComplianceAsCode/content | SCAP content source |
| 4 | ComplianceAsCode discussion | https://github.com/ComplianceAsCode/content/discussions/12679 | Community discussion reference |
| 5 | VCTLabs scap-security-guide | https://github.com/VCTLabs/scap-security-guide | Mirror or fork reference |
| 6 | Red Hat blog SCAP Security Guide | https://www.redhat.com/es/blog/scap-security-guide-helping-you-achieve-security-policy-compliance | SCAP Security Guide overview |
| 7 | OpenSCAP compliance guide | https://medium.com/@raveen.gatla/the-ultimate-guide-for-security-compliance-with-openscap-part-1-26da99824c1b | Secondary tutorial reference |

Use for Supri:

```text
Explain compliance audit concepts.
Draft audit request.
Summarize SCAP output if provided.
Differentiate audit from remediation.
```

Restrictions:

```text
SCAP remediation is high risk.
Supri can request audit only.
Remediation requires Human Owner approval.
```

Suggested request:

```yaml
supri_request_tools:
  request_openscap_audit:
    executor: runner
    mode: audit_only
    remediation_allowed: false
    requires_human_approval: true
```

---

# 8. Backup Restore SOP Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Nutanix backup restore runbook | https://portal.nutanix.com/page/documents/details?targetId=Nutanix-Cloud-Manager-Guide-v2_0:nuc-app-mgmt-backup-restore-runbook-r.html | Backup restore runbook reference |
| 2 | Ministry of Justice backup restore process | https://github.com/ministryofjustice/modernisation-platform/blob/main/source/runbooks/backup-restore-process.html.md.erb | Runbook example |
| 3 | Example service | https://github.com/rebeccaskinner/example-service | Example service docs reference |
| 4 | Google SRE Workbook | https://sre.google/workbook/table-of-contents/ | Operational reliability reference |
| 5 | Atlassian incident templates | https://www.atlassian.com/incident-management/incident-response/templates | Incident and runbook templates |

Use for Supri:

```text
Draft backup restore SOP.
Define restore test.
Define RPO and RTO notes.
Define verification after restore.
Define escalation path.
```

Restrictions:

```text
Supri may not run backup or restore.
Restore operation must be Human Owner approved.
```

Suggested template:

```md
# Backup Restore SOP

## Purpose
## Scope
## Backup Source
## Backup Destination
## Schedule
## RPO and RTO
## Restore Procedure
## Validation
## Rollback
## Escalation
## Revision History
```

---

# 9. User Management SOP Knowledge Base

Recommended sources:

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Linux man pages | https://man7.org/linux/man-pages/ | useradd, usermod, groupadd, passwd, sudoers references |
| 2 | sudo manual | https://www.sudo.ws/docs/man/sudoers.man/ | sudoers reference |
| 3 | OpenSSH manuals | https://www.openssh.com/manual.html | SSH key and access reference |
| 4 | CIS Benchmarks | https://www.cisecurity.org/cis-benchmarks | Access control baseline |
| 5 | GitLab Handbook | https://handbook.gitlab.com/ | Procedure style reference |

Use for Supri:

```text
Draft account lifecycle SOP.
Draft onboarding and offboarding checklist.
Draft sudo review checklist.
Draft SSH key rotation checklist.
```

Restrictions:

```text
Supri may not create or remove users.
Supri may not modify sudoers.
Supri may not install SSH keys.
```

Suggested template:

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

# 10. Log Analysis and Incident Classification Dataset

Datasets in this section are for **offline evaluation**, **triage pattern learning**, and **ticket classification benchmark**. They are not production truth sources.

## 10.1 Incident and Ticket Datasets

| No | Dataset | Link | Intended Use |
|---:|---|---|---|
| 1 | IT Incident Log Dataset | https://www.kaggle.com/datasets/shamiulislamshifat/it-incident-log-dataset | Incident ticket classification |
| 2 | Synthetic ServiceNow Incidents | https://huggingface.co/datasets/6StringNinja/synthetic-servicenow-incidents | Synthetic ticket classification |
| 3 | ThoughtSpot ServiceNow TML Block | https://github.com/thoughtspot/tmlblock-servicenow | ServiceNow analytics reference |
| 4 | Kaggle Q&A reference | https://www.kaggle.com/general/166298 | Secondary dataset discussion |
| 5 | AIOps incident impact prediction | https://github.com/iamr2k/AIOps-incident-impact-prediction | Incident impact prediction reference |
| 6 | AIOps incident paper | https://arxiv.org/html/2404.01363v1 | Incident impact research reference |

Use for Supri:

```text
Incident category mapping.
Ticket severity classification.
Impact summary style.
Offline evaluation.
```

Restrictions:

```text
Synthetic data is not production truth.
Do not auto-close incidents.
Do not auto-escalate without human review.
```

---

## 10.2 Log Dataset References

| No | Dataset | Link | Intended Use |
|---:|---|---|---|
| 1 | Sample log files | https://github.com/SoftManiaTech/sample_log_files | Sample logs for parsing |
| 2 | Linux logs | https://www.kaggle.com/datasets/ggsri123/linux-logs | Linux log examples |
| 3 | Loghub | https://github.com/logpai/loghub | System log datasets |
| 4 | Google Dataset Search Linux logs | https://toolbox.google.com/datasetsearch/search?query=linux&docid=01xQUwfNTomC0XKEAAAAAA%3D%3D | Dataset discovery |
| 5 | Server logs | https://www.kaggle.com/datasets/vishnu0399/server-logs | Server log examples |
| 6 | Web server access logs | https://www.kaggle.com/datasets/eliasdabbas/web-server-access-logs | HTTP access logs |
| 7 | Example log gist | https://gist.github.com/rm-hull/bd60aed44024e9986e3c | Small log sample |
| 8 | Loghub paper PDF | https://arxiv.org/pdf/2008.06448 | Loghub paper |
| 9 | Loghub ResearchGate | https://www.researchgate.net/publication/375267895_Loghub_A_Large_Collection_of_System_Log_Datasets_for_AI-driven_Log_Analytics | Secondary paper page |

Use for Supri:

```text
Log parsing pattern.
Anomaly detection benchmark.
Triage example.
Incident summary style.
```

Restrictions:

```text
Offline only.
Do not use dataset as production diagnosis authority.
Actual incident diagnosis must use actual logs and human review.
```

---

# 11. Log Analysis Checklist

Suggested checklist:

```text
1. Identify log source.
2. Identify timestamp range.
3. Normalize timezone.
4. Identify service name.
5. Identify severity.
6. Count repeated errors.
7. Find first occurrence.
8. Find recent change before error.
9. Correlate with CPU, memory, disk, network.
10. Check auth failures.
11. Check permission errors.
12. Check config parse errors.
13. Check dependency or connection errors.
14. Separate symptom from root cause.
15. Draft incident summary.
16. Add confidence level.
17. Recommend safe next checks.
```

Output template:

```md
# Log Analysis Summary

## Time Range
## Sources
## Key Symptoms
## Repeated Patterns
## Error Samples
## Possible Causes
## Confidence
## Recommended Read-Only Checks
## Escalation Needed
```

---

# 12. Incident Ticket Classification

Suggested categories:

```yaml
incident_categories:
  authentication:
    examples:
      - failed login
      - SSH brute force signal
      - sudo denial

  web_server:
    examples:
      - 4xx spike
      - 5xx spike
      - nginx config error
      - apache virtual host issue

  resource:
    examples:
      - disk full
      - high CPU
      - memory pressure
      - inode exhaustion

  service:
    examples:
      - systemd service failed
      - dependency unavailable
      - port conflict

  security:
    examples:
      - suspicious binary
      - privilege escalation indicator
      - unauthorized user
      - policy deviation

  backup_restore:
    examples:
      - backup failed
      - restore failed
      - snapshot missing

  configuration:
    examples:
      - invalid config
      - permission mismatch
      - missing environment variable

  network:
    examples:
      - DNS failure
      - connection timeout
      - refused connection
```

Severity model:

```yaml
severity:
  sev1:
    condition: "production outage or data loss risk"
  sev2:
    condition: "major service degradation"
  sev3:
    condition: "limited impact or workaround exists"
  sev4:
    condition: "informational or minor issue"
```

---

# 13. Suggested Knowledge Routing

Suggested file:

```text
config/supri_knowledge_routing.yaml
```

```yaml
supri_knowledge_routing:
  "linux_command_help":
    - tldr pages
    - Linux man pages

  "systemd":
    - systemd service manual
    - systemctl manual
    - journalctl manual
    - Linux man pages

  "nginx":
    - NGINX Admin Guide
    - nginx official docs
    - nginx debugging log

  "apache":
    - Apache HTTP Server docs
    - Apache configuration files
    - Apache logs
    - Apache security tips

  "ssh":
    - OpenSSH manual pages
    - sshd_config manual
    - Mozilla SSH guidelines
    - CIS Benchmarks

  "hardening":
    - CIS Benchmarks
    - SCAP Security Guide
    - ComplianceAsCode content
    - Ansible Lockdown CIS table
    - dev-sec ansible hardening

  "backup_restore":
    - Nutanix backup restore runbook
    - Ministry of Justice backup restore process
    - Google SRE Workbook

  "user_management":
    - Linux man pages
    - sudoers manual
    - OpenSSH manuals
    - CIS Benchmarks

  "log_analysis":
    - Loghub
    - Linux logs
    - Web server access logs
    - Sample log files

  "incident_ticket":
    - IT Incident Log Dataset
    - Synthetic ServiceNow Incidents
    - AIOps incident impact prediction
```

---

# 14. Suggested Chroma Collection

Collection:

```text
supri_sysadmin_knowledge
```

Metadata for official documentation:

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

Metadata for hardening references:

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

Metadata for datasets:

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

Metadata for runbooks:

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

# 15. Suggested Local Files

```text
config/supri_knowledge_routing.yaml
config/supri_guardrails.yaml
data/agent_workspace/runtime/
data/agent_workspace/runtime/status/
data/agent_workspace/runtime/logs/
data/agent_workspace/runtime/summaries/
data/agent_workspace/runtime/incidents/
data/agent_workspace/requests/
data/agent_workspace/errors/
data/agent_workspace/performance/
docs/runbooks/
docs/sop/
```

---

# 16. Ranking Referensi untuk Supri

| Priority | Reference | Value for Supri | Status |
|---:|---|---|---|
| 1 | Linux man-pages | Exact Linux command and interface reference | Core knowledge |
| 2 | tldr pages | Practical command examples | Core quick reference |
| 3 | systemd manuals | Service and journal analysis | Core knowledge |
| 4 | OpenSSH manuals and sshd_config | SSH review and hardening | Core knowledge |
| 5 | NGINX and Apache docs | Web server troubleshooting | Core knowledge |
| 6 | CIS Benchmarks | Security baseline | Core hardening reference |
| 7 | SCAP Security Guide | Compliance audit reference | Controlled audit reference |
| 8 | ComplianceAsCode content | SCAP content source | Controlled reference |
| 9 | Backup restore runbooks | SOP template | Core SOP reference |
| 10 | Loghub | Log analytics benchmark | Offline evaluation |
| 11 | Linux and server log datasets | Log triage evaluation | Offline only |
| 12 | IT Incident Log Dataset | Incident classification | Offline only |
| 13 | Synthetic ServiceNow Incidents | Ticket classification | Offline only |
| 14 | Awesome sysadmin lists | Tool discovery | Secondary reference |
| 15 | Linux monitoring GitHub topic | Tool discovery | Secondary reference |

---

# 17. Final Policy

Supri uses these links as **read-only sysadmin knowledge**, not as execution authority.

```text
Supri reads.
Supri summarizes.
Supri classifies.
Supri writes SOP.
Supri writes troubleshooting notes.
Supri requests safe checks.
Supri does not execute.
```

Hard boundary:

```text
No shell.
No service restart.
No config mutation.
No user modification.
No hardening apply.
No OpenSCAP remediation.
No ansible-playbook execution.
No delete command.
No .env modification.
No secret access.
No commit.
No push.
```
