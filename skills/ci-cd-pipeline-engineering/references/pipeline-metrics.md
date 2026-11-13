# Pipeline health and DORA metrics

Docs: https://dora.dev/guides/dora-metrics/

## Definitions (apply exactly, state the choice made)

| Metric | Definition |
|---|---|
| Success rate | succeeded / (succeeded + failed); exclude canceled, skipped, never started |
| Duration | finished − started, successful runs on the default branch; nearest-rank percentile, report n |
| Queue time | started − created, every run that started |
| Flaky job | same SHA + job has a failed and a successful attempt (retry or rerun, across runs of the SHA) |
| Deployment frequency | production deploys in window ÷ days in window |
| Change failure rate | production deploys needing rollback or hotfix ÷ all production deploys |
| Lead time | median over commits of (production deploy finished − committed_at) |
| Recovery time | median from failed deploy to next good production deploy, sorted by time |

Nearest rank: sort ascending, take element `ceil(p/100 · n)` (1-based). No interpolation.

## Pitfalls

- Sort deployments by time before pairing failures with recoveries; input order is not guaranteed.
- Window bounds are inclusive on both days; deploys outside the window are excluded even if they supply commits.
- Lead time per commit, not per deployment: a deploy with three commits contributes three values.
- A job failing on SHA A and passing on SHA B is a regression/fix, not flakiness.
- Report numbers per team or service; never rank individuals.
