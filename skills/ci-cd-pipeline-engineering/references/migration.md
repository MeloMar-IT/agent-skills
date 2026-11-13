# Platform migration mapping

Docs: https://docs.github.com/actions/migrating-to-github-actions, https://docs.gitlab.com/ee/ci/migration/

| Concept | GitLab CI | GitHub Actions | Azure Pipelines |
|---|---|---|---|
| Trigger | `workflow:rules`, `rules:if` | `on:` plus job `if:` | `trigger`, `pr`, `condition` |
| Ordering | `stages`, `needs` | `needs` | `dependsOn` (direct only) |
| Cache | `cache:key:files` | `actions/cache` key with `hashFiles` | `Cache@2` |
| Artifacts | `artifacts` + `expire_in` | `upload/download-artifact@v4` | pipeline artifacts, `PublishPipelineArtifact` |
| Variables | CI/CD variables | `vars`, `env`, `$GITHUB_OUTPUT` | variables, `isOutput=true` |
| Protected secrets | protected variables | environment secrets | variable groups, environment |
| Serialize deploys | `resource_group` | `concurrency` with `cancel-in-progress: false` | exclusive lock check |
| Manual gate | `when: manual` | environment required reviewers | environment approval on `deployment` job |
| Cancel superseded | `interruptible` | `concurrency` cancel (not deploys) | batch / autoCancel |
| Jenkins | `Jenkinsfile` stages | one workflow per pipeline, jobs per stage | stages and jobs |

Rules: map intent, not syntax; keep every gate (approvals, protected branches, manual steps) or list it explicitly as dropped and why; switch long-lived credentials to OIDC; pin actions; lint the result and compare the effective config before cutover.
