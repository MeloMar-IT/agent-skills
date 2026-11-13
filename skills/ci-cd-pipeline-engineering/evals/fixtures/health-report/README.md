# Pipeline health report

Write `report.py` (Python 3, standard library only):

    python3 report.py runs.json deployments.json report.json

Reporting window: 2026-10-01 to 2026-10-14, both days inclusive (UTC).

## runs.json

List of pipeline runs: `id`, `sha`, `ref`, `status` (success, failed, canceled, skipped),
`created_at`, `started_at`, `finished_at` (ISO 8601 UTC; null when the run never started),
`jobs`: list of `{name, attempt, status}`.

## deployments.json

List of deployments (file order is not guaranteed): `id`, `environment` (production or staging),
`finished_at`, `remediation` (none, rollback or hotfix), `commits`: list of `{sha, committed_at}`.

## report.json

One JSON object with these keys:

- `pipeline_success_rate` (fraction, 4 decimals)
- `p50_duration_s`, `p90_duration_s` (seconds)
- `median_queue_s` (seconds)
- `flaky_jobs` (sorted list of job names)
- `deployment_frequency_per_day`
- `change_failure_rate` (fraction, 4 decimals)
- `lead_time_median_h` (hours)
- `recovery_time_median_h` (hours)
