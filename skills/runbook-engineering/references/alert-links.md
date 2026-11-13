# Linking alerts to runbooks

## Rule shape
- Every `alert:` rule gets exactly one `runbook_url` under `annotations`: an absolute https URL to the published page, a literal string per rule (no templates that build it).
- `record:` rules take no annotations. Do not add any.
- Check every link, including existing ones. A relative link (`runbooks/x.md`) or a dead one is worse than none: fix it.

## Find the runbook first
1. Search runbook frontmatter `alerts:` lists for the alert name. One runbook can cover several alerts, and its file name may not match the alert name. Reuse it.
2. Only if none names the alert, create a stub from `assets/runbook.md`: `status: draft`, `owner` from the alert's `team` label, `alerts: [<name>]`, `severity` from the alert's `severity` label (`critical` means `page`), no `last_reviewed` (it counts as stale). Put it inside the docs folder.

## Build the URL
Find the platform config, then map the file path to a URL.

MkDocs (`mkdocs.yml`):
- Base is `site_url` (add a trailing slash). Path is relative to `docs_dir` (default `docs`), subfolders kept; the `docs_dir` name is not part of the URL.
- `use_directory_urls: true` (default): `x.md` becomes `x/`; `dir/index.md` becomes `dir/`.
- `use_directory_urls: false`: `x.md` becomes `x.html`; `dir/index.md` becomes `dir/index.html`.
- Example: `site_url: https://runbooks.example.com/`, `docs_dir: runbooks`, `false`: `runbooks/infra/disk.md` is `https://runbooks.example.com/infra/disk.html`.

Other platforms:
- Backstage TechDocs runs MkDocs under its own path prefix (`/docs/<namespace>/<kind>/<name>/` in the default setup); build from that prefix plus the MkDocs path.
- Confluence: use the URL with the page id, not the title (titles change).
- If you cannot confirm the mapping, say so and mark the link unverified.

## Verify
Confirm each URL's target file exists in the docs folder and maps back to the same URL. Network checks are impossible offline; state that.

## Notification path
- Alertmanager `.CommonAnnotations` holds only values identical across the whole group. If `group_by` omits `alertname`, or URLs differ, the link vanishes or is wrong. Render per alert:

```
{{ range .Alerts }}{{ .Labels.alertname }}: {{ .Annotations.runbook_url }}
{{ end }}
```
- Do not use `.CommonAnnotations.runbook_url` in receivers where groups can mix alerts.
- PagerDuty: `links:` in `pagerduty_config` (templated per alert is limited, so link the group's alerts via `details` or the first alert's annotation, and say so).
- Grafana alerting: the `runbook_url` annotation is shown as a button.
- Version note: template and field availability differ across Alertmanager versions; check the installed one.
