# Doni Knowledge Base Links

**Agent:** Doni  
**Role:** DevOps, CI/CD, deployment, IaC, observability, and runtime review agent  
**Purpose:** daftar rujukan knowledge base untuk Doni  
**Created:** 2026-05-05 19:22:56

---

# 1. Fungsi Knowledge Base Doni

Knowledge base ini dipakai untuk memperkuat Doni sebagai **DevOps reviewer**. Doni memakai link ini untuk membaca pola, checklist, template, contoh konfigurasi, dan data evaluasi.

Doni tidak boleh memakai link ini sebagai izin untuk menjalankan deployment, apply infrastructure, restart service, atau menjalankan command aktif.

Prinsip:

```text
Knowledge base = boleh dibaca
Execution = harus lewat Runner atau Verification Engine
High-risk operation = wajib Human Owner approval
```

---

# 2. Core Base Knowledge

| Domain | Isi yang perlu dipahami | Fungsi Doni |
|---|---|---|
| Kubernetes manifests | Deployment, Service, Ingress, ConfigMap, Secret, probes, resources | Review deployment YAML |
| Dockerfile best practices | Base image, layer, user, port, env, healthcheck | Review image build risk |
| Docker Compose | Service, network, volume, env, dependency | Review local runtime config |
| GitHub Actions workflow YAML | Jobs, steps, permissions, secrets, triggers, artifacts | Review CI/CD workflow |
| Terraform module registry pattern | Provider, modules, version pinning, plan/apply split | Review IaC risk |
| Ansible playbook structure | Inventory, tasks, handlers, roles, vars, templates | Review automation risk |
| Helm chart structure | Chart.yaml, values.yaml, templates, release config | Review Helm deployment |
| Prometheus alerting rules | Alert expression, labels, severity, runbook links | Review alert readiness |
| Grafana dashboard JSON | Panels, datasource, provisioning, dashboard JSON | Review observability |
| Deployment runbook | Deployment steps, validation, rollback trigger | Review operational readiness |
| Rollback procedure | Rollback decision, artifact, version, verification | Review recovery plan |
| Incident response runbook | Triage, escalation, containment, postmortem | Review failure response |

---

# 3. Dataset Knowledge Base

Datasets hanya untuk **offline evaluation**, **failure taxonomy**, dan **log pattern testing**. Dataset tidak boleh menjadi sumber keputusan produksi.

| No | Dataset | Link | Intended Use | Runtime Use |
|---:|---|---|---|---|
| 1 | CI/CD Pipeline Failure Logs Dataset for AIOps | https://www.kaggle.com/datasets/mirzayasirabdullah07/cicd-pipeline-failure-logs-dataset-for-aiops | Klasifikasi failure pipeline, benchmark Doni | Offline only |
| 2 | AI-Driven CI/CD Pipeline Logs Dataset | https://www.kaggle.com/datasets/rahuljangir78/ai-driven-cicd-pipeline-logs-dataset | CI/CD log pattern and incident triage | Offline only |
| 3 | DevOps Pipeline Incident Logs and Description | https://www.kaggle.com/datasets/ved0902/devops-pipeline-incident-logs-and-description | Incident taxonomy and failure description | Offline only |
| 4 | DevOps AWS and Azure Effectiveness Deployment | https://www.kaggle.com/datasets/nickkinyae/devops-aws-and-azure-effectiveness-deployment/code | Cloud deployment effectiveness example | Offline only |
| 5 | Pipeline Defect Dataset | https://www.kaggle.com/datasets/simplexitypipeline/pipeline-defect-dataset | Pipeline defect analysis | Offline only |
| 6 | DevOps Pipeline Incident Logs Code | https://www.kaggle.com/datasets/ved0902/devops-pipeline-incident-logs-and-description/code | Notebook/code exploration for incident logs | Offline only |
| 7 | Server Logs | https://www.kaggle.com/datasets/vishnu0399/server-logs | Server log parsing and anomaly examples | Offline only |
| 8 | Server Logs Suspicious | https://www.kaggle.com/datasets/kartikjaspal/server-logs-suspicious | Suspicious log pattern testing | Offline only |
| 9 | Web Server Access Logs | https://www.kaggle.com/datasets/eliasdabbas/web-server-access-logs | Access log analysis examples | Offline only |
| 10 | Linux Logs | https://www.kaggle.com/datasets/ggsri123/linux-logs | Linux system log review examples | Offline only |
| 11 | Loghub Linux Log Data | https://www.kaggle.com/datasets/omduggineni/loghub-linux-log-data/code | Linux log parsing and benchmark examples | Offline only |
| 12 | Linux Auth Log Anomalies | https://www.kaggle.com/datasets/lnorbaci/linux-auth-log-anomalies | Auth anomaly pattern testing | Offline only |
| 13 | AI Incident Database | https://www.kaggle.com/datasets/konradb/ai-incident-database | AI incident taxonomy and postmortem reference | Offline only |
| 14 | Kaggle Q&A Reference | https://www.kaggle.com/questions-and-answers/95502 | Supplementary discussion reference | Reference only |

---

# 4. Kubernetes Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Kubernetes Course | https://github.com/ag-computational-bio/kubernetes-course | Kubernetes manifests, Deployment, Service, Ingress, volumes, storage, YAML examples |

Use for Doni:

```text
Review Kubernetes YAML
Check probes
Check resource requests and limits
Check namespace and labels
Check secret/configmap references
Check rollout and service exposure risk
```

Restrictions:

```text
Doni cannot run kubectl apply
Doni cannot run kubectl delete
Doni can request client-side dry-run through Runner
```

---

# 5. Docker and Docker Compose Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | AWS CodeBuild Docker Images | https://github.com/aws/aws-codebuild-docker-images | Dockerfile and build image environment reference |
| 2 | Docker Samples Example Voting App | https://github.com/dockersamples/example-voting-app | Multi-container app, Compose, Swarm, Kubernetes example |
| 3 | Haxxnet Compose Examples | https://github.com/Haxxnet/Compose-Examples | Docker Compose examples and self-hosting patterns |
| 4 | Docker Compose Node.js Examples | https://github.com/geekcell/docker-compose-nodejs-examples | Node.js Docker Compose examples |
| 5 | Debezium Examples | https://github.com/debezium/debezium-examples | Compose examples for data and streaming stacks |

Use for Doni:

```text
Review Dockerfile
Review Docker Compose services
Check base image
Check exposed ports
Check volume mounts
Check environment variables
Check healthcheck
Check service dependencies
Check network exposure
```

Restrictions:

```text
Doni cannot run docker build
Doni cannot run docker compose up
Doni cannot expose service
Doni can request compose config validation through Runner
```

---

# 6. GitHub Actions and CI/CD Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | GitHub Actions Starter Workflows | https://github.com/actions/starter-workflows | Starter CI, deployment, automation, code scanning, pages workflow patterns |
| 2 | Azure Actions Workflow Samples | https://github.com/Azure/actions-workflow-samples | Deployment workflow examples for Azure services |
| 3 | GitHub Actions Deploy Pages | https://github.com/actions/deploy-pages | GitHub Pages deployment action and permissions |
| 4 | AWS SAM Pipeline Template | https://github.com/aws-samples/cookiecutter-aws-sam-pipeline | AWS SAM CI/CD pipeline template |
| 5 | AWS Cross-Account Pipeline | https://github.com/awslabs/aws-refarch-cross-account-pipeline | Cross-account AWS pipeline architecture |
| 6 | AWS QuickStart TaskCat CI | https://github.com/aws-quickstart/quickstart-taskcat-ci | CI testing for AWS QuickStart / TaskCat |

Use for Doni:

```text
Review workflow triggers
Review job permissions
Review secrets usage
Review artifact flow
Review deployment environment
Review unpinned actions
Review production deployment gates
```

Restrictions:

```text
Doni cannot trigger deployment
Doni cannot modify secrets
Doni cannot push workflow changes
Doni can request YAML validation and workflow linting
```

---

# 7. Terraform and IaC Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Qovery Terraform Provider Examples | https://github.com/Qovery/terraform-provider-examples | Terraform provider examples |
| 2 | Cloud Posse Terraform AWS Components | https://github.com/cloudposse/terraform-aws-components | AWS component and module patterns |
| 3 | Terragrunt Infrastructure Modules Example | https://github.com/gruntwork-io/terragrunt-infrastructure-modules-example | Terragrunt module/live split and module source pattern |
| 4 | Infrastructure as Code Example | https://github.com/Artemmkin/infrastructure-as-code-example | General IaC example |
| 5 | Infrastructure As Code Intro | https://github.com/MasonEgger-Edu/Infrastructure-As-Code-Intro | Introductory IaC learning reference |

Use for Doni:

```text
Review provider version pinning
Review module source and version pinning
Review plan/apply separation
Review remote state risk
Review sensitive variable handling
Review environment separation
```

Restrictions:

```text
Doni cannot run terraform apply
Doni cannot run terraform destroy
Doni can request terraform validate
Doni can request terraform plan only with Human Owner approval
```

---

# 8. Ansible Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Ansible Best Practices | https://github.com/fdavis/ansible-best-practices | Ansible structure and best practice reference |
| 2 | DevOps Masterclass Terraform Kubernetes Ansible Docker | https://github.com/rohanmistry231/DevOps-Masterclass-Terraform-Kubernetes-Ansible-Docker | Cross-domain DevOps examples |
| 3 | Ansible Examples | https://github.com/ansible/ansible-examples | Official starter examples for playbooks |
| 4 | Ansible for DevOps | https://github.com/geerlingguy/ansible-for-devops | Practical Ansible examples and learning reference |

Use for Doni:

```text
Review inventory
Review playbook structure
Review roles
Review tasks and handlers
Review idempotency
Review become usage
Review variable and secret handling
```

Restrictions:

```text
Doni cannot run ansible-playbook
Doni can request syntax check through Runner
```

---

# 9. Helm and GitOps Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Helm Examples | https://github.com/helm/examples | Helm chart minimal examples |
| 2 | Argo CD Course Apps Definitions | https://github.com/mabusaa/argocd-course-apps-definitions | Declarative Argo CD Application, Project, Cluster, and Repo examples |

Use for Doni:

```text
Review Chart.yaml
Review values.yaml
Review templates
Review release config
Review Argo CD Application
Review sync policy
Review app-of-apps pattern
```

Restrictions:

```text
Doni cannot run helm install
Doni cannot run helm upgrade
Doni cannot run argocd sync
Doni can request helm template through Runner
```

---

# 10. Observability Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Sample Grafana | https://github.com/cirocosta/sample-grafana | Grafana dashboard provisioning, Prometheus and Docker Compose example |

Use for Doni:

```text
Review Grafana dashboard JSON
Review provisioning config
Review Prometheus scrape config
Review alert rules
Review dashboard drift
```

Restrictions:

```text
Doni cannot restart Grafana
Doni cannot modify production dashboard directly
Doni can request JSON validation
```

---

# 11. Runbook and Operational Readiness Knowledge Base

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | DevOps Templates | https://github.com/kiurakku/devops-templates | Deployment, rollback, incident response, CI/CD, DevSecOps, monitoring, backup, DR templates |

Use for Doni:

```text
Review deployment runbook
Review rollback procedure
Review incident response runbook
Review postmortem template
Review backup and restore readiness
Review SLO/SLA notes
```

Restrictions:

```text
Doni cannot execute runbook command
Doni cannot trigger rollback
Doni can write runbook readiness review
```

---

# 12. Suggested Knowledge Routing

Suggested file:

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

# 13. Chroma Metadata Suggestion

For source documents:

```json
{
  "agent": "doni",
  "source_type": "devops_reference",
  "allowed_use": "review_and_recommendation",
  "runtime_dependency": false,
  "can_execute": false,
  "requires_runner": true,
  "risk": "medium",
  "topic": "github_actions_workflow"
}
```

For datasets:

```json
{
  "agent": "doni",
  "source_type": "offline_dataset",
  "allowed_use": "offline_evaluation_only",
  "runtime_dependency": false,
  "can_decide_production_incident": false,
  "risk": "medium"
}
```

---

# 14. Final Policy

Doni may use these references to write reviews, recommendations, and validation requests.

Doni must not execute deployment, infrastructure mutation, cloud operation, or service restart.

```text
Doni reads.
Doni reviews.
Doni requests validation.
Runner executes allowed safe checks.
Human Owner approves high-risk actions.
```
