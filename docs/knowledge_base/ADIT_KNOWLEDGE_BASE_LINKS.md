# Adit Knowledge Base Links

**Agent:** Adit  
**Role:** Documentation architect, technical documentation maintainer, API documentation assistant, runbook writer, and documentation style reviewer  
**Purpose:** daftar rujukan knowledge base untuk Diataxis, technical documentation style, API reference docs, OpenAPI, AsyncAPI, IT SOP, incident runbook, release notes, README, dan ADR  
**Created:** 2026-05-05 19:38:58

---

# 1. Fungsi Knowledge Base Adit

Knowledge base ini dipakai untuk memperkuat Adit sebagai **documentation agent**.

Adit memakai referensi ini untuk:

```text
Diataxis tutorials, how-to, reference, explanation
Microsoft writing style guide
technical documentation structure
API reference documentation template
OpenAPI YAML examples
AsyncAPI event-driven API documentation
IT SOP template
incident runbook template
release notes template
README best practices
Architecture Decision Record ADR template
```

Adit tidak boleh memakai referensi ini sebagai izin untuk:

```text
mengubah source code
menjalankan build docs
install dependency
deploy documentation
publish documentation
mengubah .env
commit
push
execute runbook command
```

Prinsip:

```text
Knowledge base = boleh dibaca
Docs patch = boleh dibuat sesuai manifest
Build or deploy = harus lewat Runner
Final approval = Senior Reviewer
High-risk docs change = Human Owner
```

---

# 2. Core Base Knowledge untuk Adit

| Domain | Isi yang perlu dipahami | Fungsi Adit |
|---|---|---|
| Diataxis | Tutorials, how-to guides, reference, explanation | Mengklasifikasi dan menata dokumentasi |
| Microsoft writing style | Clear, concise, developer-oriented technical writing | Menjaga gaya dokumentasi |
| API reference docs | Endpoint, method, parameter, request, response, error, auth | Menulis API reference |
| OpenAPI YAML | `openapi`, `paths`, `components`, `schemas`, `security` | Membantu struktur API spec |
| AsyncAPI docs | Event, channel, message, schema, broker, subscription | Dokumentasi event-driven API |
| IT SOP | Purpose, scope, roles, procedure, approval, revision history | Membuat SOP operasional |
| Incident runbook | Detection, triage, impact, mitigation, escalation, rollback | Membuat runbook insiden |
| Release notes | Version, date, changes, breaking changes, migration notes | Membuat catatan rilis |
| README | Project overview, setup, usage, config, test, contribution | Memperbaiki README |
| ADR | Context, decision, consequences, status | Menulis keputusan arsitektur |

---

# 3. Diataxis Documentation Framework

## 3.1 Primary References

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Diataxis official website | https://diataxis.fr/ | Teori utama Diataxis |
| 2 | Diataxis GitHub repository | https://github.com/evildmp/diataxis-documentation-framework | Source repository Diataxis |
| 3 | Diataxis tutorials | https://diataxis.fr/tutorials/ | Panduan membuat tutorial |
| 4 | Diataxis how-to guides | https://diataxis.fr/how-to-guides/ | Panduan membuat how-to |
| 5 | Diataxis reference | https://diataxis.fr/reference/ | Panduan membuat reference docs |
| 6 | Diataxis explanation | https://diataxis.fr/explanation/ | Panduan membuat explanation docs |

## 3.2 Agent-Oriented Diataxis References

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Diataxis Claude Agent | https://github.com/amrani/diataxis-claude-agent | Pola agent untuk evaluasi docs berbasis Diataxis |
| 2 | Diataxis Documentation Restructurer | https://github.com/anneKsiy/diataxis-documentation-restructurer | Pola restrukturisasi dokumentasi dengan Diataxis |

Use for Adit:

```text
Classify docs as tutorial, how-to, reference, or explanation.
Detect missing documentation type.
Write documentation gap report.
Suggest docs structure.
Avoid mixing tutorial, how-to, reference, and explanation in one page.
```

Suggested local output:

```text
data/agent_workspace/docs/{task_id}.doc_gap_report.md
data/agent_workspace/docs/{task_id}.adit_docs_plan.md
```

---

# 4. Microsoft Writing Style Guide and Technical Documentation Style

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Microsoft Writing Style Guide | https://learn.microsoft.com/en-us/style-guide/welcome/ | Technical writing style guide |
| 2 | Microsoft Style Guide: Writing principles | https://learn.microsoft.com/en-us/style-guide/welcome/#writing-principles | Clear and concise writing principles |
| 3 | Microsoft Style Guide: Procedures and instructions | https://learn.microsoft.com/en-us/style-guide/procedures-instructions/ | Step-by-step procedure writing |
| 4 | Microsoft Style Guide: Formatting text in instructions | https://learn.microsoft.com/en-us/style-guide/procedures-instructions/formatting-text-in-instructions | Instruction formatting |
| 5 | Microsoft Style Guide: Code examples | https://learn.microsoft.com/en-us/style-guide/developer-content/code-examples | Code example writing |
| 6 | Google Developer Documentation Style Guide Rules for Vale | https://github.com/vale-cli/Google | Vale-compatible style rules |
| 7 | Wrappid Guide Module | https://github.com/wrappid/guide-module | Example of structured developer guide module |

Use for Adit:

```text
Improve clarity.
Reduce ambiguity.
Write direct procedures.
Keep command examples readable.
Review docs style.
Create style review report.
```

Restrictions:

```text
Adit may write style suggestions.
Adit may write docs patch.
Adit may not run Vale directly.
Adit may request Vale check through Verification Engine.
```

---

# 5. API Reference Documentation Template

## 5.1 General API Documentation References

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Redoc | https://github.com/Redocly/redoc | OpenAPI generated API reference docs |
| 2 | Redoc Documentation | https://redocly.com/docs/redoc | Redoc usage and configuration |
| 3 | Swagger Core | https://github.com/swagger-api/swagger-core | Swagger/OpenAPI generation and annotation ecosystem |
| 4 | NelmioApiDocBundle | https://github.com/nelmio/NelmioApiDocBundle | API docs bundle example for Symfony |
| 5 | Ktor OpenAPI Tools | https://github.com/SMILEY4/ktor-openapi-tools | OpenAPI docs tooling example for Ktor |
| 6 | Pterodactyl API Docs | https://github.com/NETVPX/pterodactyl-api-docs | Docusaurus API documentation example |

## 5.2 Suggested API Reference Template

```md
# API Reference: {endpoint_name}

## Overview

## Endpoint

`{method} {path}`

## Authentication

## Request Headers

| Header | Required | Description |
|---|---:|---|

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---:|---|

## Query Parameters

| Parameter | Type | Required | Description |
|---|---|---:|---|

## Request Body

## Example Request

```bash
curl -X {method} "{base_url}{path}"
```

## Response

## Example Response

```json
{}
```

## Error Responses

| Status | Code | Meaning | Suggested Fix |
|---:|---|---|---|

## Notes
```

Use for Adit:

```text
Write endpoint reference docs.
Keep request and response examples consistent.
Document authentication and errors.
Do not invent API behavior not found in source or manifest.
```

---

# 6. OpenAPI YAML Examples

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | OpenAPI Specification | https://github.com/OAI/OpenAPI-Specification | Official OpenAPI Specification repository |
| 2 | OpenAPI Initiative | https://www.openapis.org/ | OpenAPI initiative and ecosystem |
| 3 | Swagger OpenAPI Guide | https://swagger.io/docs/specification/about/ | Practical OpenAPI guide |
| 4 | EazyBytes OpenAPI | https://github.com/eazybytes/openapi | OpenAPI learning examples |
| 5 | Swagger Core | https://github.com/swagger-api/swagger-core | OpenAPI generation tooling |
| 6 | Konfig OpenAPI Examples | https://github.com/konfig-sdks/openapi-examples | Public OpenAPI specification examples |
| 7 | Redoc | https://github.com/Redocly/redoc | OpenAPI rendered documentation |

Suggested OpenAPI skeleton:

```yaml
openapi: 3.1.0
info:
  title: Example API
  version: 1.0.0
paths:
  /health:
    get:
      summary: Health check
      responses:
        "200":
          description: Service is healthy
components:
  schemas: {}
  securitySchemes: {}
```

Use for Adit:

```text
Review OpenAPI docs.
Write OpenAPI explanation.
Suggest API docs structure.
Request OpenAPI validation through Verification Engine.
```

Restrictions:

```text
Adit may edit openapi.yaml only if manifest allows.
Adit may not run Redoc build directly.
Adit may request OpenAPI validation.
```

---

# 7. AsyncAPI Event-Driven API Documentation

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | AsyncAPI Specification | https://github.com/asyncapi/spec | Official AsyncAPI Specification |
| 2 | AsyncAPI Documentation | https://www.asyncapi.com/docs | AsyncAPI official docs |
| 3 | AsyncAPI Example | https://github.com/alexandramartinez/asyncapi-example | Example AsyncAPI project |
| 4 | AsyncAPI Generator | https://github.com/asyncapi/generator | Generate docs/code from AsyncAPI definitions |
| 5 | AsyncAPI Studio | https://studio.asyncapi.com/ | Editor and preview for AsyncAPI |

Suggested AsyncAPI skeleton:

```yaml
asyncapi: 3.0.0
info:
  title: Example Event API
  version: 1.0.0
channels:
  user.signedup:
    address: user.signedup
    messages:
      UserSignedUp:
        $ref: "#/components/messages/UserSignedUp"
components:
  messages:
    UserSignedUp:
      payload:
        type: object
        properties:
          userId:
            type: string
```

Use for Adit:

```text
Document event-driven APIs.
Explain channels, messages, payloads, and subscribers.
Request AsyncAPI validation through Verification Engine.
```

---

# 8. IT SOP Template

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | GitLab Handbook | https://handbook.gitlab.com/ | Operating handbook and procedure style reference |
| 2 | DevOps Templates | https://github.com/kiurakku/devops-templates | SOP, runbook, incident, deployment template references |
| 3 | Atlassian Incident Management Templates | https://www.atlassian.com/incident-management/incident-response/templates | Incident and operational templates |
| 4 | Google SRE Book | https://sre.google/sre-book/table-of-contents/ | SRE operational reference |
| 5 | Google SRE Workbook | https://sre.google/workbook/table-of-contents/ | Practical SRE procedures |

Suggested IT SOP template:

```md
# SOP: {procedure_name}

## Document Control

| Field | Value |
|---|---|
| Owner | |
| Version | |
| Effective Date | |
| Review Cycle | |

## Purpose

## Scope

## Roles and Responsibilities

## Prerequisites

## Procedure

1. Step one.
2. Step two.
3. Step three.

## Validation

## Rollback or Recovery

## Risks and Controls

## Escalation

## Revision History
```

Use for Adit:

```text
Write SOP for local AI operations.
Write SOP for Chroma rebuild.
Write SOP for agent dry-run.
Write SOP for docs release.
```

Restrictions:

```text
Adit writes SOP only.
Adit does not execute SOP steps.
```

---

# 9. Incident Runbook Template

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Runbook Template | https://github.com/khalidx/runbook | Markdown runbook concept |
| 2 | DevOps Templates | https://github.com/kiurakku/devops-templates | Incident response and runbook templates |
| 3 | Google SRE Workbook: Incident Response | https://sre.google/workbook/incident-response/ | Incident response practice |
| 4 | Atlassian Incident Response Templates | https://www.atlassian.com/incident-management/incident-response/templates | Incident response template references |
| 5 | PagerDuty Incident Response | https://response.pagerduty.com/ | Incident response operational reference |

Suggested incident runbook template:

```md
# Incident Runbook: {incident_type}

## Severity

## Symptoms

## Detection Signal

## Immediate Actions

## Triage Checklist

## Impact Assessment

## Mitigation Steps

## Rollback Steps

## Escalation Path

## Communication

## Verification

## Post-Incident Review
```

Use for Adit:

```text
Create incident runbook template.
Document recovery flow.
Document escalation path.
Document rollback checklist.
```

Restrictions:

```text
Adit may write runbook.
Adit may not execute incident commands.
```

---

# 10. Release Notes Template

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Keep a Changelog | https://keepachangelog.com/en/1.1.0/ | Changelog format and categories |
| 2 | Semantic Versioning | https://semver.org/ | Versioning reference |
| 3 | GitHub Release Notes | https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes | GitHub release notes reference |
| 4 | Release Drafter | https://github.com/release-drafter/release-drafter | Automated release draft pattern |
| 5 | Changesets | https://github.com/changesets/changesets | Version and changelog management pattern |

Suggested release notes template:

```md
# Release Notes: v{version}

## Release Date

## Summary

## Added

## Changed

## Fixed

## Deprecated

## Removed

## Security

## Breaking Changes

## Migration Notes

## Verification

## Known Issues
```

Use for Adit:

```text
Write release notes.
Update CHANGELOG.md.
Document breaking changes.
Document migration notes.
```

Restrictions:

```text
Adit may not create GitHub release.
Adit may not push tags.
```

---

# 11. README Best Practices

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Make a README | https://www.makeareadme.com/ | README structure guide |
| 2 | Awesome README | https://github.com/matiassingers/awesome-readme | README examples and patterns |
| 3 | Standard Readme | https://github.com/RichardLitt/standard-readme | Standard README specification |
| 4 | Common Readme | https://github.com/noffle/common-readme | README convention |
| 5 | GitHub About READMEs | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes | GitHub README guidance |

Suggested README structure:

```md
# Project Name

## Overview

## Features

## Architecture

## Requirements

## Installation

## Configuration

## Usage

## Development

## Testing

## Documentation

## Security

## Troubleshooting

## Contributing

## License
```

Use for Adit:

```text
Improve README.
Add installation and usage docs.
Add architecture summary.
Add troubleshooting section.
```

Restrictions:

```text
Adit must not invent unsupported installation steps.
Adit must use manifest or actual repo evidence.
```

---

# 12. Architecture Decision Record ADR Template

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | Michael Nygard ADR | https://github.com/joelparkerhenderson/architecture-decision-record/tree/main/locales/en/examples/nygard | Classic ADR format |
| 2 | ADR GitHub Organization | https://adr.github.io/ | ADR overview and links |
| 3 | Architecture Decision Record Repository | https://github.com/joelparkerhenderson/architecture-decision-record | ADR templates and examples |
| 4 | MADR Template | https://github.com/adr/madr | Markdown Architectural Decision Records |
| 5 | Log4brains | https://github.com/thomvaill/log4brains | ADR static site generator |

Suggested ADR template:

```md
# ADR-{number}: {title}

## Status

Proposed | Accepted | Deprecated | Superseded

## Context

## Decision

## Consequences

### Positive

### Negative

### Neutral

## Alternatives Considered

## Related Decisions
```

Use for Adit:

```text
Write ADR for architecture changes.
Document why multi-agent design uses Kanban and message bus.
Document why Asep and Doni are reviewer-only.
Document why Commit Gate is a tool, not agent.
```

Restrictions:

```text
Adit may draft ADR.
Senior Reviewer or Human Owner approves ADR.
```

---

# 13. MkDocs and Docusaurus Documentation Site References

| No | Source | Link | Intended Use |
|---:|---|---|---|
| 1 | MkDocs | https://www.mkdocs.org/ | Static documentation site generator |
| 2 | MkDocs Material | https://squidfunk.github.io/mkdocs-material/ | Material theme documentation |
| 3 | Philly Community Wireless Docs | https://github.com/phillycommunitywireless/docs | MkDocs Material technical docs example |
| 4 | Obsidian Publish MkDocs | https://github.com/jobindjohn/obsidian-publish-mkdocs | Obsidian to MkDocs pattern |
| 5 | MkDocs Jekyll | https://github.com/vsoch/mkdocs-jekyll | MkDocs/Jekyll template |
| 6 | Docusaurus | https://docusaurus.io/ | Documentation framework |
| 7 | Pterodactyl API Docs | https://github.com/NETVPX/pterodactyl-api-docs | Docusaurus API docs example |
| 8 | Protected Docs Example | https://github.com/levino/protected-docs-example | Cautionary reference for protected docs |

Use for Adit:

```text
Suggest docs site structure.
Draft docs navigation.
Write MkDocs or Docusaurus docs plan.
```

Restrictions:

```text
Adit may not run mkdocs build.
Adit may not run docusaurus build.
Adit may not deploy docs.
```

---

# 14. Suggested Knowledge Routing

Suggested file:

```text
config/adit_knowledge_routing.yaml
```

```yaml
adit_knowledge_routing:
  "docs/tutorials":
    - Diataxis tutorials
    - Microsoft writing style guide

  "docs/how-to":
    - Diataxis how-to guides
    - Microsoft procedures and instructions

  "docs/reference":
    - Diataxis reference
    - API reference documentation template

  "docs/explanation":
    - Diataxis explanation
    - Microsoft technical writing style

  "openapi.yaml":
    - OpenAPI Specification
    - Swagger OpenAPI Guide
    - Redoc

  "asyncapi.yaml":
    - AsyncAPI Specification
    - AsyncAPI Documentation

  "README.md":
    - Make a README
    - Awesome README
    - Standard Readme

  "CHANGELOG.md":
    - Keep a Changelog
    - Semantic Versioning

  "docs/runbooks":
    - incident runbook template
    - DevOps Templates
    - Google SRE Workbook

  "docs/sop":
    - IT SOP template
    - GitLab Handbook
    - Google SRE Book

  "docs/adr":
    - ADR template
    - MADR
    - Architecture Decision Record repository
```

---

# 15. Suggested Chroma Collection

Collection:

```text
adit_documentation_knowledge
```

Metadata for general references:

```json
{
  "agent": "adit",
  "source_type": "documentation_reference",
  "allowed_use": "writing_and_structure_guidance",
  "runtime_dependency": false,
  "can_execute": false,
  "risk": "low",
  "topic": "diataxis"
}
```

Metadata for docs build tools:

```json
{
  "agent": "adit",
  "source_type": "docs_tool_reference",
  "allowed_use": "suggestion_only",
  "runtime_dependency": false,
  "can_execute": false,
  "requires_runner": true,
  "risk": "medium"
}
```

---

# 16. Suggested Local Files

```text
config/adit_knowledge_routing.yaml
config/adit_guardrails.yaml
data/agent_workspace/docs/
data/agent_workspace/patches/
data/agent_workspace/reports/
data/agent_workspace/requests/
docs/tutorials/
docs/how-to/
docs/reference/
docs/explanation/
docs/runbooks/
docs/sop/
docs/adr/
```

---

# 17. Ranking Referensi untuk Adit

| Priority | Reference | Value for Adit | Status |
|---:|---|---|---|
| 1 | Diataxis official framework | Documentation architecture | Core knowledge |
| 2 | Microsoft Writing Style Guide | Technical writing style | Core knowledge |
| 3 | OpenAPI Specification | API spec structure | Core knowledge |
| 4 | AsyncAPI Specification | Event-driven API docs | Core knowledge |
| 5 | Redoc | API reference generated docs | Tool reference |
| 6 | Keep a Changelog | Release notes and changelog | Core knowledge |
| 7 | Standard Readme / Make a README | README structure | Core knowledge |
| 8 | ADR / MADR | Architecture decision records | Core knowledge |
| 9 | Google SRE Book / Workbook | SOP and incident runbook | Operational docs knowledge |
| 10 | DevOps Templates | Runbook and SOP examples | Template reference |
| 11 | MkDocs / MkDocs Material | Docs site structure | Optional docs site |
| 12 | Docusaurus | Large docs site | Optional advanced docs site |
| 13 | Vale Google Rules | Style lint reference | Optional validation |
| 14 | Protected Docs Example | Cautionary reference | Warning only |

---

# 18. Final Policy

Adit uses these links as **documentation knowledge**, not as automatic execution authority.

```text
Adit classifies.
Adit plans.
Adit writes documentation patches.
Adit proposes validation.
Adit does not build.
Adit does not deploy.
Adit does not execute runbook commands.
```

Hard boundary:

```text
No source code modification.
No shell.
No docs deployment.
No dependency install.
No commit.
No push.
No .env modification.
No invented behavior.
```
