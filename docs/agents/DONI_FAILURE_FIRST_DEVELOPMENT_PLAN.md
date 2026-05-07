# Doni Failure-First Development Plan

**Project:** `self-development-agent` untuk `ai-rag-local`  
**Agent:** Doni  
**Model lokal:** `qwen3-coder:4b`  
**Role:** DevOps, CI/CD, IaC, deployment, observability, and runtime reviewer  
**Status:** development plan  
**Created:** 2026-05-05 19:22:56

---

# Ringkasan Eksekutif

Doni dirancang sebagai **DevOps reviewer**. Doni menilai risiko CI/CD, Docker, Compose, Kubernetes, Helm, GitOps, Terraform, Ansible, observability, runbook, rollback, dan incident response.

Doni bukan executor bebas.

Doni tidak boleh:

```text
run shell
docker build
docker compose up
kubectl apply
kubectl delete
helm install
helm upgrade
terraform apply
terraform destroy
ansible-playbook
deploy to cloud
restart service
modify .env
commit
push
delete file
```

Doni boleh:

```text
read manifest
read changed DevOps files
read git diff
retrieve DevOps reference
write DevOps review
write validation request
request safe checks through Runner or Verification Engine
block high-risk deployment configuration
```

Core design:

```text
Doni = DevOps reviewer
Runner = controlled executor
Verification Engine = deterministic validator
Senior Reviewer = final reviewer
Human Owner = final authority
```

---

# Bagian A
# Pondasi Anti-Gagal Doni

Bagian ini dipisahkan dari referensi. Jika semua referensi eksternal tidak cocok, Doni tetap harus aman.

---

## A1. Posisi Doni dalam Multi-Agent System

Doni berada pada jalur review setelah Siwa mengklasifikasikan task sebagai DevOps, CI/CD, IaC, deployment, observability, atau runtime-related task.

Alur dasar:

```text
Human Owner or Siwa
  ↓
Task Manifest
  ↓
Siwa routes DevOps-related task
  ↓
Doni reviews configuration and risks
  ↓
Doni writes DevOps Review
  ↓
Doni writes validation request if needed
  ↓
Runner or Verification Engine executes safe checks
  ↓
Senior Reviewer makes final decision
```

Doni tidak boleh menjadi deployment executor.

---

## A2. Failure Taxonomy

| Failure | Contoh | Dampak | Respons |
|---|---|---|---|
| Workflow terlalu permisif | `permissions: write-all` | Supply-chain risk | `request_revision` atau `block` |
| Trigger berbahaya | Deploy on forked PR | Secret exposure | `block` atau human gate |
| Secret leak | Secret plain text di workflow atau Compose | Critical | `block` |
| Docker sample dianggap production-ready | Copy-paste default credential | Runtime exposure | Mark as example-only |
| Compose expose service sensitif | Port DB expose ke publik | Data exposure | `request_revision` atau `block` |
| Kubernetes tanpa resources | No requests/limits | Stability risk | `request_revision` |
| Kubernetes missing probes | No readiness/liveness | Deployment risk | `request_revision` |
| Helm secret in values | Plain secret in values.yaml | Secret exposure | `block` |
| Terraform apply otomatis | Apply dalam CI tanpa gate | IaC mutation risk | human gate |
| Terraform destroy | Destroy command appears | Critical | `block` |
| Ansible non-idempotent | Raw command tanpa guard | Config drift | `request_revision` |
| Grafana invalid JSON | Dashboard gagal load | Observability gap | validation request |
| Prometheus alert too noisy | Alert tanpa threshold jelas | Alert fatigue | `request_revision` |
| Runbook command destructive | `rm -rf`, force restart | Outage risk | `block` |
| Dataset treated as ground truth | Offline dataset dipakai untuk keputusan produksi | Wrong diagnosis | Offline-only policy |
| AIOps hallucination | Doni menyimpulkan incident tanpa evidence | False positive | Evidence gate |
| Silent failure | Doni gagal tanpa report | Tidak bisa audit | Error artifact wajib |

---

## A3. Doni Anti-Failure Gates

Doni harus melewati enam gate:

```text
Scope Gate
File-Type Routing Gate
Reference Retrieval Gate
Evidence Gate
Validation Request Gate
Decision Gate
```

### A3.1 Scope Gate

Doni hanya boleh membaca:

```text
task manifest
git diff
changed files in allowed_paths
relevant workflow/config files
selected DevOps references
previous agent artifacts
```

Doni tidak boleh membaca:

```text
.env
.env.*
.git/
data/secrets/
production secrets
cloud credentials
unrelated local folders
```

Jika perlu scope tambahan, Doni menulis:

```text
data/agent_workspace/requests/{task_id}.doni_scope_request.md
```

### A3.2 File-Type Routing Gate

Doni harus menentukan jenis file sebelum review.

Routing:

```yaml
file_type_routing:
  ".github/workflows/*.yml": github_actions_review
  ".github/workflows/*.yaml": github_actions_review
  "Dockerfile": dockerfile_review
  "docker-compose.yml": compose_review
  "compose.yaml": compose_review
  "k8s/**/*.yaml": kubernetes_review
  "charts/**": helm_review
  "terraform/**/*.tf": terraform_review
  "**/*.tf": terraform_review
  "ansible/**/*.yml": ansible_review
  "grafana/**/*.json": grafana_review
  "prometheus/**/*.yml": prometheus_review
  "runbooks/**/*.md": runbook_review
```

Unknown file type:

```text
status = human_review_required or general_config_review
```

### A3.3 Reference Retrieval Gate

Doni only retrieves references matching the file type.

Examples:

```text
GitHub Actions file → GitHub Actions references only
Dockerfile → Docker references only
Terraform file → Terraform references only
Runbook file → Runbook references only
```

Doni must not retrieve all knowledge base at once.

### A3.4 Evidence Gate

Every finding must include evidence.

Minimum finding:

```yaml
finding:
  title:
  risk:
  evidence:
  affected_file:
  line_or_pattern:
  recommended_fix:
```

No evidence means no blocker.

### A3.5 Validation Request Gate

Doni cannot run validation. Doni only requests it.

Allowed request:

```text
request_yaml_validation
request_github_actions_lint
request_dockerfile_lint
request_compose_config_check
request_kubernetes_dry_run_client
request_helm_template
request_terraform_validate
request_terraform_plan
request_ansible_syntax_check
request_grafana_json_validate
request_prometheus_rule_check
```

### A3.6 Decision Gate

Doni only returns:

```text
approve_devops
request_revision
block
human_required
```

Doni cannot return:

```text
deploy
apply
restart
rollback
commit
push
```

---

## A4. Hard Block Rules

Doni must `block` or create human escalation if patch introduces:

```text
automatic production deploy without approval
terraform apply in CI without human gate
terraform destroy
kubectl apply to real cluster
kubectl delete
helm upgrade without approval
plain text secrets
GitHub Actions permissions too broad for sensitive job
untrusted third-party action in privileged workflow
Docker Compose exposes DB or admin service publicly
runbook with destructive command
agent shell access for deployment
disable tests before deploy
skip verification before deploy
deployment with no rollback path
```

---

## A5. Confidence Model

```yaml
doni_confidence:
  high:
    condition: "Risk directly visible in workflow/config diff."
  medium:
    condition: "Risk inferred from file type and known pattern."
  low:
    condition: "General best-practice concern without direct operational risk."
```

Decision guidance:

| Risk | Confidence | Decision |
|---|---|---|
| Critical | High | block |
| High | High | block or human_required |
| High | Medium | request_revision |
| Medium | High | request_revision |
| Medium | Medium | request_revision or note |
| Low | Low | note only |

---

## A6. Degrade Gracefully Policy

| Condition | Fallback |
|---|---|
| Reference retrieval fails | Review using local rules only |
| YAML parser fails | Write validation request |
| Docker reference unavailable | General Dockerfile checklist |
| Kubernetes reference unavailable | General manifest checklist |
| Terraform unknown provider | Request human review |
| Log dataset unavailable | Skip dataset, review actual logs only |
| Runner validation unavailable | Mark pending verification |
| Output schema invalid | Retry once, then human review |

---

## A7. Performance Budget

Doni efficiency is measured by runtime cost, not script length.

Metrics:

```text
files read
references retrieved
LLM calls
validation requests
review duration
findings count
false positives after Senior review
report length
```

Budget:

```yaml
doni_performance_budget:
  max_llm_calls_per_review: 2
  max_reference_chunks: 10
  max_files_read: 12
  max_validation_requests: 5
  max_review_duration_seconds: 180
  max_report_lines: 350
```

If budget is exceeded:

```text
data/agent_workspace/performance/{task_id}.doni_performance_warning.md
```

---

## A8. Error Artifact

If Doni fails, write:

```text
data/agent_workspace/errors/{task_id}.doni_error.md
```

Template:

```md
# Doni Error Report

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
# Development Plan Doni

---

## B1. Identity Configuration

File:

```text
config/agents.yaml
```

```yaml
doni:
  name: "Doni"
  type: "llm_agent"
  role: "devops_ci_deployment_reviewer"
  model: "doni:latest"
  base_model: "qwen3-coder:4b"
  temperature: 0.1
  max_context_tokens: 8192

  can_assign_tasks: false
  can_write_patch: false
  can_review_patch: true
  can_apply_patch: false
  can_commit: false
  can_push: false
  can_deploy: false

  responsibilities:
    - review_github_actions
    - review_dockerfile
    - review_docker_compose
    - review_kubernetes_manifests
    - review_helm_chart
    - review_argocd_config
    - review_terraform_files
    - review_ansible_playbook
    - review_observability_config
    - review_deployment_runbook
    - review_rollback_procedure
    - review_incident_response_runbook
    - request_safe_validation
    - write_devops_review

  denied_responsibilities:
    - run_shell
    - docker_build
    - docker_compose_up
    - kubectl_apply
    - kubectl_delete
    - helm_install
    - helm_upgrade
    - terraform_apply
    - terraform_destroy
    - ansible_playbook
    - deploy_to_cloud
    - restart_service
    - modify_env
    - git_commit
    - git_push
    - delete_file
```

---

## B2. Modelfile Doni

File:

```text
modelfiles/Modelfile.doni
```

```dockerfile
FROM qwen3-coder:4b

PARAMETER temperature 0.1
PARAMETER top_p 0.75
PARAMETER num_ctx 8192

SYSTEM """
You are Doni, the DevOps, CI/CD, deployment, IaC, observability, and runtime reviewer for ai-rag-local.

Your job:
- review GitHub Actions workflows;
- review Dockerfiles and Docker Compose files;
- review Kubernetes manifests;
- review Helm charts and Argo CD declarations;
- review Terraform and Ansible files;
- review Grafana, Prometheus, runbooks, rollback, and incident response documents;
- identify DevOps reliability, deployment, and operational risks;
- request safe validation through Runner or Verification Engine;
- write structured DevOps review reports.

You must not:
- run shell commands;
- build Docker images;
- run docker compose up;
- run kubectl apply/delete;
- run helm install/upgrade;
- run terraform apply/destroy;
- run ansible-playbook;
- deploy to cloud;
- restart services;
- modify .env;
- commit;
- push;
- delete files;
- bypass Safety Gate;
- bypass Senior Reviewer.

Your output must be evidence-based and review-only.
"""
```

Command:

```bash
ollama create doni -f modelfiles/Modelfile.doni
```

---

## B3. Tool Permission

Allowed tools:

```yaml
doni_tools:
  allow:
    - read_file
    - list_files
    - git_diff
    - retrieve_devops_reference
    - inspect_workflow_yaml
    - inspect_dockerfile
    - inspect_compose_yaml
    - inspect_kubernetes_yaml
    - inspect_helm_chart
    - inspect_terraform_files
    - inspect_ansible_playbook
    - inspect_grafana_dashboard
    - inspect_prometheus_rules
    - inspect_runbook
    - write_devops_review
    - write_validation_request
```

Denied tools:

```yaml
doni_tools:
  deny:
    - run_shell
    - docker_build
    - docker_compose_up
    - kubectl_apply
    - kubectl_delete
    - helm_install
    - helm_upgrade
    - terraform_apply
    - terraform_destroy
    - ansible_playbook
    - restart_service
    - deploy_to_cloud
    - modify_env
    - git_commit
    - git_push
    - delete_file
```

Request-only tools:

```yaml
doni_runner_requests:
  github_actions_lint:
    executor: verification_engine

  yaml_validation:
    executor: verification_engine

  dockerfile_lint:
    executor: verification_engine

  compose_config_check:
    executor: runner
    requires_human_if_network_exposed: true

  kubernetes_dry_run:
    executor: runner
    cluster_required: false
    mode: client_dry_run

  helm_template:
    executor: runner
    no_cluster_required: true

  terraform_validate:
    executor: runner

  terraform_plan:
    executor: runner
    requires_human_approval: true

  ansible_syntax_check:
    executor: runner

  grafana_json_validate:
    executor: verification_engine

  prometheus_rule_check:
    executor: verification_engine
```

---

## B4. Knowledge Base Design

Collection:

```text
doni_devops_knowledge
```

Domains:

```yaml
doni_knowledge_domains:
  cicd:
    - GitHub Actions Starter Workflows
    - GitHub Actions Deploy Pages
    - Azure Actions Workflow Samples
    - AWS SAM Pipeline Template
    - AWS Cross-Account Pipeline
    - AWS QuickStart TaskCat CI

  docker:
    - AWS CodeBuild Docker Images
    - Docker Samples Example Voting App
    - Haxxnet Compose Examples
    - Docker Compose Node.js Examples
    - Debezium Examples

  kubernetes:
    - Kubernetes Course
    - Helm Examples
    - Argo CD Course Apps Definitions

  terraform:
    - Qovery Terraform Provider Examples
    - Cloud Posse Terraform AWS Components
    - Terragrunt Infrastructure Modules Example
    - Infrastructure as Code Examples

  ansible:
    - Ansible Examples
    - Ansible Best Practices
    - Ansible for DevOps

  observability:
    - Sample Grafana
    - Prometheus alerting rules
    - Grafana dashboard JSON

  runbooks:
    - DevOps Templates
    - deployment runbook
    - rollback procedure
    - incident response runbook

  datasets:
    - CI/CD failure logs
    - DevOps incident logs
    - Linux logs
    - server logs
    - suspicious logs
    - AI incident database
```

---

## B5. Knowledge Routing

File:

```text
config/doni_knowledge_routing.yaml
```

```yaml
doni_knowledge_routing:
  ".github/workflows":
    - GitHub Actions Starter Workflows
    - GitHub Actions Deploy Pages
    - Azure Actions Workflow Samples

  "Dockerfile":
    - AWS CodeBuild Docker Images
    - Dockerfile best practices

  "docker-compose.yml":
    - Docker Samples Example Voting App
    - Haxxnet Compose Examples
    - Debezium Examples

  "compose.yaml":
    - Docker Samples Example Voting App
    - Haxxnet Compose Examples

  "k8s":
    - Kubernetes Course

  "kubernetes":
    - Kubernetes Course

  "charts":
    - Helm Examples

  "helm":
    - Helm Examples

  "argocd":
    - Argo CD Course Apps Definitions

  "terraform":
    - Qovery Terraform Provider Examples
    - Cloud Posse Terraform AWS Components
    - Terragrunt Infrastructure Modules Example

  "ansible":
    - Ansible Examples
    - Ansible Best Practices
    - Ansible for DevOps

  "grafana":
    - Sample Grafana

  "prometheus":
    - Sample Grafana

  "runbooks":
    - DevOps Templates

  "logs":
    - CI/CD Pipeline Failure Logs Dataset
    - Server Logs
    - Linux Logs
```

---

## B6. Output Contract

Path:

```text
data/agent_workspace/devops/{task_id}.doni_devops_review.md
```

Template:

```md
# Doni DevOps Review

## Task ID

## Review Mode
review_only

## Inputs Reviewed

## Files Reviewed

## Knowledge Sources Used

| Source | Reason | Mode |
|---|---|---|

## CI/CD Risk

## Docker Risk

## Kubernetes Risk

## Helm and GitOps Risk

## Terraform/IaC Risk

## Ansible Risk

## Observability Risk

## Runbook and Rollback Readiness

## Findings

| ID | Finding | Risk | Confidence | Evidence | Recommended Fix |
|---|---|---|---|---|---|

## Validation Requests

| Check | Executor | Requires Human Approval | Reason |
|---|---|---|---|

## Blockers

## Final Decision
approve_devops | request_revision | block | human_required

## Notes for Senior Reviewer
```

---

## B7. Validation Request Contract

Path:

```text
data/agent_workspace/requests/{task_id}.doni_validation_request.yaml
```

Template:

```yaml
task_id: task-043
requested_by: doni
validation_type: terraform_validate
executor: runner
requires_human_approval: false
reason: "Terraform files changed and need validate check."
allowed_commands:
  - terraform validate
denied_commands:
  - terraform apply
  - terraform destroy
  - terraform import
  - terraform state
```

For high-risk plan:

```yaml
task_id: task-044
requested_by: doni
validation_type: terraform_plan
executor: runner
requires_human_approval: true
reason: "Terraform module changed and plan is needed before review."
allowed_commands:
  - terraform plan
denied_commands:
  - terraform apply
  - terraform destroy
```

---

## B8. Decision Rules

### B8.1 approve_devops

Use when:

```text
No deployment risk found.
No secret risk found.
No broad permissions found.
No high-risk validation needed.
Config aligns with task scope.
```

### B8.2 request_revision

Use when:

```text
Workflow permission too broad but fixable.
Dockerfile lacks healthcheck or non-root note.
Kubernetes lacks resource requests/limits.
Helm values need safer defaults.
Terraform module not pinned.
Runbook lacks rollback validation.
Observability gap exists.
```

### B8.3 block

Use when:

```text
Production deployment without approval.
Terraform apply or destroy in automation.
Plain text secrets.
kubectl apply to real cluster without gate.
helm upgrade without approval.
GitHub Actions write-all for sensitive job.
Docker exposes sensitive service publicly.
Runbook contains destructive command.
```

### B8.4 human_required

Use when:

```text
Cloud deployment policy changes.
Terraform plan needed.
Production environment mentioned.
Credential or secret management changes.
Rollback procedure affects production.
```

---

# Bagian C
# Implementation Roadmap

---

## C1. Phase 0: Contract Freeze

Deliverables:

```text
config/agents.yaml
config/doni_knowledge_routing.yaml
config/doni_guardrails.yaml
schemas/doni_devops_review.schema.json
schemas/doni_validation_request.schema.json
```

Exit criteria:

```text
Doni has no execution tools.
Doni cannot deploy.
Doni cannot run shell.
Doni cannot commit or push.
Doni cannot modify .env.
```

---

## C2. Phase 1: Review-Only Doni

Capabilities:

```text
read manifest
read git diff
detect changed DevOps files
write DevOps review
detect hard blockers
```

Exit criteria:

```text
Doni blocks terraform destroy in workflow.
Doni blocks plain text secret in compose file.
```

---

## C3. Phase 2: CI/CD and Docker Review

Capabilities:

```text
review GitHub Actions workflow
review Dockerfile
review docker-compose.yml
request YAML validation
request Dockerfile lint
```

Exit criteria:

```text
Doni can identify risky workflow permissions.
Doni can identify exposed sensitive ports.
```

---

## C4. Phase 3: Kubernetes, Helm, and GitOps Review

Capabilities:

```text
review Kubernetes manifests
review Helm chart structure
review Argo CD declarations
request client-side dry-run
request helm template
```

Exit criteria:

```text
Doni can detect missing probes and resource limits.
Doni can request helm template without running cluster changes.
```

---

## C5. Phase 4: Terraform and Ansible Review

Capabilities:

```text
review Terraform files
review Terraform modules
review Ansible playbooks
request terraform validate
request ansible syntax check
```

Exit criteria:

```text
Doni can escalate terraform plan to Human Owner.
Doni blocks terraform apply or destroy automation.
```

---

## C6. Phase 5: Observability and Runbook Review

Capabilities:

```text
review Grafana dashboard JSON
review Prometheus rules
review deployment runbook
review rollback procedure
review incident response runbook
```

Exit criteria:

```text
Doni can request revision when deployment lacks rollback.
Doni can identify alert or dashboard gaps.
```

---

## C7. Phase 6: Offline Dataset Evaluation

Purpose:

```text
Evaluate Doni on failure classification using offline datasets.
Do not use dataset as production decision authority.
```

Metrics:

```text
pipeline failure classification accuracy
log triage precision
false positive rate
incident category match
review usefulness score
```

Exit criteria:

```text
Doni can summarize failure logs without claiming production certainty.
```

---

## C8. Phase 7: Tuning and Stabilization

Metrics:

```text
finding precision
false positive rate
Senior acceptance rate
average review time
validation request usefulness
block accuracy
human_required accuracy
```

Exit criteria:

```text
Doni improves review quality without slowing workflow excessively.
```

---

# Bagian D
# Referensi Terpisah dari Pondasi Anti-Gagal

Referensi tidak menjadi dependency inti. Referensi hanya menjadi knowledge base, pattern, atau validation idea.

---

## D1. Compatibility Score

| Criteria | Weight |
|---|---:|
| Matches review-only DevOps use | 20 |
| Can be used read-only | 15 |
| Does not require live deployment | 15 |
| Supports failure-first workflow | 10 |
| Supports validation or linting | 10 |
| Low overengineering risk | 10 |
| Clear examples or templates | 10 |
| Can be scoped by file type | 10 |

Decision:

```text
>= 80  core knowledge
60-79  optional knowledge
40-59  example only
< 40   exclude
```

---

## D2. CI/CD References

| Reference | Link | Use |
|---|---|---|
| GitHub Actions Starter Workflows | https://github.com/actions/starter-workflows | Workflow structure and CI/deploy patterns |
| GitHub Actions Deploy Pages | https://github.com/actions/deploy-pages | Pages deployment permissions and artifact flow |
| Azure Actions Workflow Samples | https://github.com/Azure/actions-workflow-samples | Deployment workflow examples |
| AWS SAM Pipeline Template | https://github.com/aws-samples/cookiecutter-aws-sam-pipeline | AWS SAM pipeline structure |
| AWS Cross-Account Pipeline | https://github.com/awslabs/aws-refarch-cross-account-pipeline | Cross-account pipeline architecture |
| AWS TaskCat CI | https://github.com/aws-quickstart/quickstart-taskcat-ci | CI testing for AWS templates |

---

## D3. Docker and Compose References

| Reference | Link | Use |
|---|---|---|
| AWS CodeBuild Docker Images | https://github.com/aws/aws-codebuild-docker-images | Docker image build environment reference |
| Docker Samples Voting App | https://github.com/dockersamples/example-voting-app | Multi-container Compose and Kubernetes example |
| Haxxnet Compose Examples | https://github.com/Haxxnet/Compose-Examples | Compose examples with caution |
| Docker Compose Node.js Examples | https://github.com/geekcell/docker-compose-nodejs-examples | Node.js Compose pattern |
| Debezium Examples | https://github.com/debezium/debezium-examples | Data stack Compose examples |

---

## D4. Kubernetes, Helm, and GitOps References

| Reference | Link | Use |
|---|---|---|
| Kubernetes Course | https://github.com/ag-computational-bio/kubernetes-course | Kubernetes manifests and YAML examples |
| Helm Examples | https://github.com/helm/examples | Helm chart structure |
| Argo CD Course Apps Definitions | https://github.com/mabusaa/argocd-course-apps-definitions | Argo CD app-of-apps and declarative GitOps examples |

---

## D5. Terraform and IaC References

| Reference | Link | Use |
|---|---|---|
| Qovery Terraform Provider Examples | https://github.com/Qovery/terraform-provider-examples | Terraform provider examples |
| Cloud Posse Terraform AWS Components | https://github.com/cloudposse/terraform-aws-components | AWS component/module examples |
| Terragrunt Infrastructure Modules Example | https://github.com/gruntwork-io/terragrunt-infrastructure-modules-example | Module/live split pattern, caution because deprecated |
| Infrastructure as Code Example | https://github.com/Artemmkin/infrastructure-as-code-example | General IaC pattern |
| Infrastructure As Code Intro | https://github.com/MasonEgger-Edu/Infrastructure-As-Code-Intro | Introductory IaC reference |

---

## D6. Ansible References

| Reference | Link | Use |
|---|---|---|
| Ansible Best Practices | https://github.com/fdavis/ansible-best-practices | Best practice structure |
| DevOps Masterclass | https://github.com/rohanmistry231/DevOps-Masterclass-Terraform-Kubernetes-Ansible-Docker | Cross-domain examples |
| Ansible Examples | https://github.com/ansible/ansible-examples | Playbook examples |
| Ansible for DevOps | https://github.com/geerlingguy/ansible-for-devops | Practical Ansible examples |

---

## D7. Observability and Runbook References

| Reference | Link | Use |
|---|---|---|
| Sample Grafana | https://github.com/cirocosta/sample-grafana | Grafana and Prometheus provisioning example |
| DevOps Templates | https://github.com/kiurakku/devops-templates | Runbook, rollback, incident response, CI/CD, monitoring templates |

---

## D8. Dataset References

Datasets are secondary. They are for offline evaluation only.

| Dataset | Link | Use |
|---|---|---|
| CI/CD Pipeline Failure Logs | https://www.kaggle.com/datasets/mirzayasirabdullah07/cicd-pipeline-failure-logs-dataset-for-aiops | Pipeline failure classification |
| AI-Driven CI/CD Pipeline Logs | https://www.kaggle.com/datasets/rahuljangir78/ai-driven-cicd-pipeline-logs-dataset | CI/CD log pattern testing |
| DevOps Pipeline Incident Logs | https://www.kaggle.com/datasets/ved0902/devops-pipeline-incident-logs-and-description | Incident taxonomy |
| AWS and Azure Effectiveness Deployment | https://www.kaggle.com/datasets/nickkinyae/devops-aws-and-azure-effectiveness-deployment/code | Cloud deployment example analysis |
| Pipeline Defect Dataset | https://www.kaggle.com/datasets/simplexitypipeline/pipeline-defect-dataset | Defect pattern analysis |
| Server Logs | https://www.kaggle.com/datasets/vishnu0399/server-logs | Server log parsing |
| Server Logs Suspicious | https://www.kaggle.com/datasets/kartikjaspal/server-logs-suspicious | Suspicious log examples |
| Web Server Access Logs | https://www.kaggle.com/datasets/eliasdabbas/web-server-access-logs | Access log patterns |
| Linux Logs | https://www.kaggle.com/datasets/ggsri123/linux-logs | Linux logs |
| Loghub Linux Log Data | https://www.kaggle.com/datasets/omduggineni/loghub-linux-log-data/code | Linux log benchmark |
| Linux Auth Log Anomalies | https://www.kaggle.com/datasets/lnorbaci/linux-auth-log-anomalies | Auth anomaly examples |
| AI Incident Database | https://www.kaggle.com/datasets/konradb/ai-incident-database | AI incident taxonomy |

Rules:

```text
Offline only.
No production diagnosis authority.
No automatic remediation.
No direct runtime decision.
```

---

# Bagian E
# Test and Acceptance Criteria

---

## E1. Minimum Acceptance Criteria

Doni is ready for early use if:

```text
Can read manifest.
Can detect DevOps file type.
Can review GitHub Actions workflow.
Can review Dockerfile and Compose file.
Can review Terraform or Kubernetes file in review-only mode.
Can write Doni DevOps Review.
Can write validation request.
Can block destructive operations.
Can escalate high-risk deployment.
```

---

## E2. Failure Acceptance Criteria

The system is safe if:

```text
Doni cannot run shell.
Doni cannot deploy.
Doni cannot run Docker.
Doni cannot run kubectl.
Doni cannot run helm.
Doni cannot run terraform apply/destroy.
Doni cannot run ansible-playbook.
Doni cannot restart service.
Doni cannot modify .env.
Doni cannot commit.
Doni cannot push.
Doni writes error artifact when failing.
```

---

## E3. First Dry-Run Scenario

Input:

```yaml
task_id: task-devops-001
task_type: ci_workflow_change
risk_level: medium
changed_files:
  - .github/workflows/test.yml
```

Expected:

```text
Doni detects GitHub Actions workflow.
Doni checks trigger, permissions, secrets, artifact, deploy gate.
Doni writes DevOps review.
Doni may request YAML validation.
No workflow execution.
No deploy.
```

---

## E4. Terraform Failure Scenario

Input:

```yaml
task_id: task-iac-001
task_type: terraform_change
risk_level: high
changed_files:
  - terraform/main.tf
```

Expected:

```text
Doni reviews Terraform change.
Doni blocks terraform apply in CI.
Doni requests terraform validate.
Doni marks terraform plan as human_required.
No apply.
No destroy.
```

---

## E5. Docker Compose Failure Scenario

Input:

```yaml
task_id: task-compose-001
task_type: compose_change
risk_level: medium
changed_files:
  - docker-compose.yml
```

Expected:

```text
Doni checks exposed ports, volumes, env, default credentials, healthcheck.
Doni requests revision if database is exposed publicly.
Doni does not run docker compose up.
```

---

# Final Summary

Doni must be built as a failure-first DevOps reviewer.

Final rule:

```text
Doni reviews.
Doni requests validation.
Runner executes safe checks.
Human Owner approves high-risk actions.
Doni never deploys.
```

This keeps Doni useful for CI/CD and infrastructure review without turning it into an unsafe deployment agent.
