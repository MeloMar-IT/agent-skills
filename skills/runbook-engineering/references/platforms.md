# Platforms and migration

| Option | Strengths | Weaknesses |
| --- | --- | --- |
| Docs-as-code (MkDocs, Backstage TechDocs) | Review in pull requests, versioned, CODEOWNERS for ownership, stable URLs, frontmatter checks in CI | Needs a build pipeline; non-engineers edit less |
| Wiki (Confluence and similar) | Easy editing, search | No review gate, drift, URLs tied to page ids or titles, hard to lint |
| Executable runbooks (Rundeck jobs, Ansible playbooks) | Steps run the same way every time, audit log | Needs guardrails ([auto-remediation.md](auto-remediation.md)); prose context still needed |

Default recommendation: docs-as-code for the prose runbook, with executable jobs linked from it for proven steps.

## Migrating
- Keep every published URL working. MkDocs: the `redirects` plugin with `redirect_maps` (old path to new path). Wikis: keep old pages as stubs pointing to the new one.
- Update every `runbook_url` in alert rules, notification templates and service catalog entries in the same change as the move.
- Carry over `owner` and `alerts`; set `last_reviewed` only if the content was actually reviewed during the move.
- Check all links after the move ([alert-links.md](alert-links.md)).
