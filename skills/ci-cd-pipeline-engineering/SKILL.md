---
name: ci-cd-pipeline-engineering
description: "Designs, fixes, speeds up, secures and measures CI/CD pipelines in github actions, gitlab ci and azure pipelines: build once and promote by digest, least-privilege tokens and OIDC, untrusted input, cache vs artifacts, DAG needs, monorepo change rules, required-check gate jobs, safe concurrency for deploys, cross-stage output variables, artifact v4 changes, platform migration, pipeline health and dora metrics. Use when editing or reviewing workflow YAML, .gitlab-ci.yml or azure-pipelines.yml, or when computing pipeline success rate, durations, flaky jobs or DORA metrics from run history."
metadata:
  capabilities: [github-actions, gitlab-ci, azure-pipelines, build-once-promote, artifact-promotion, pipeline-security, oidc-federation, required-status-checks, monorepo-pipelines, pipeline-caching, pipeline-concurrency, deployment-gates, pipeline-migration, pipeline-health, dora-metrics, flaky-jobs]
  technologies: [github, gitlab, azure-devops, yaml, docker]
---

# CI/CD pipeline engineering

Apply the rules below to the platform in use. Details and examples: `references/github-actions.md`, `references/gitlab-ci.md`, `references/azure-pipelines.md`, `references/pipeline-metrics.md`, `references/migration.md`. Out of scope: incident response and SLOs (sre skill), language build tooling, test design, Terraform/Kubernetes internals.

## Principles

- **Build once, promote the same artifact.** Deploy the same immutable artifact by digest to every environment. Never rebuild or retag per environment; inject environment config at deploy time.
- **Cache is not artifacts.** A cache is a best-effort speedup keyed on the lockfile hash. Artifacts are the guaranteed way to pass outputs between jobs. Never pass build output through a cache.
- **Fast feedback.** Use a DAG (`needs`) instead of strict stages, cheap checks first, a timeout on every job. Retry only on infrastructure failures, never to hide flaky tests.
- **Cancel and serialize.** Cancel superseded PR/feature runs. Never cancel or interrupt a production deploy. Run deploys one at a time per environment.
- **Least privilege.** Read-only default token; each job raises only what it needs. Use OIDC, not long-lived keys. Gate production with environment approvals.
- **Untrusted text.** PR titles/bodies, branch names (`github.head_ref`) and commit messages never go straight into a script. Pass through `env` and quote. Never run PR head code under `pull_request_target`.
- Never silently drop a gate when changing or migrating a pipeline. Before calling a pipeline correct, lint it and check the effective config.

## GitHub Actions

- Job-level `permissions` replace the whole set: a job needing `id-token: write` must also list `contents: read`.
- Pin third-party actions to the full 40-character SHA.
- A workflow skipped by `on: paths` leaves its required check pending forever. Keep the trigger unfiltered, detect changes inside a job (job with `outputs`), and skip heavy jobs with a job-level `if: needs.changes.outputs.x == 'true'`.
- A skipped job reports success. A gate job with the default `if` is skipped when a dependency fails, so the merge goes through. Gate: `needs: [all jobs]`, `if: always()`, and a step that fails when any `needs.*.result` is `failure` or `cancelled` (e.g. `contains(needs.*.result, 'failure')`).
- OIDC deploy job: `permissions` with `id-token: write` and `contents: read`, `if: github.event_name == 'push'`, its own `concurrency` group with `cancel-in-progress: false` (a workflow-level `cancel-in-progress: true` would cancel it). Pin the credentials action to a 40-hex SHA.
- Concurrency: PR runs `cancel-in-progress: ${{ github.event_name == 'pull_request' }}`. Deploy job gets its own group with `cancel-in-progress: false`; a group keeps only one pending run.
- Artifacts v4 (v3 is retired): artifacts are immutable, so each matrix job needs a unique name (`dist-${{ matrix.target }}`). Download with `pattern: dist-*` plus `merge-multiple: true`; the pattern must not match unrelated artifacts (e.g. coverage). Set `include-hidden-files: true` on every upload with dotfiles. Hidden files (e.g. `.well-known/`) are excluded by default since v4.4: set `include-hidden-files: true`.
- Cache keys combine `runner.os` and `hashFiles(...)`; caches are scoped to a branch. Write step outputs to `$GITHUB_OUTPUT`.

## GitLab CI

- Use `rules`, not `only`/`except`; the two cannot be mixed in one job.
- Duplicate pipelines (branch + MR pipeline for one push) are fixed in `workflow:rules`: `if: $CI_PIPELINE_SOURCE == "merge_request_event"`, then `if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS` → `when: never`, then `if: $CI_COMMIT_BRANCH`.
- `needs: []` starts a job at once. If a needed job can be excluded by rules, write `needs: [{job: x, optional: true}]` or pipeline creation fails.
- `rules:changes`: MR pipelines compare with the target branch, branch pipelines with the previous push, a new branch always matches (see `compare_to` below).
- Cache: `cache:key:files` (at most 2 files); consumers use `policy: pull`. Pass outputs as `artifacts` with `expire_in`.
- `interruptible: true` is safe on build/test jobs, never on deploys; if `default:` sets it, the deploy job needs `interruptible: false`. Auto-cancel of superseded pipelines needs it. `resource_group` serializes deploys.
- `when: manual` inside `rules` blocks by default (`allow_failure: false`); add `allow_failure: true` so the pipeline can finish without the click.
- To stop a new branch from running everything, use `changes: {paths: [..], compare_to: refs/heads/main}` (a ref name, not `origin/main`). Put an unconditional rule for the default branch (`if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH`) before the `changes` rule: on the default branch `compare_to` compares main with itself, finds nothing and would skip the builds.
- `parallel` with `CI_NODE_INDEX` (counts from 1) and `CI_NODE_TOTAL`.

## Azure Pipelines

- Three expression syntaxes: `${{ }}` compile time, `$(var)` macro, `$[ ]` runtime expression. Mapping values from `dependencies`/`stageDependencies` needs `$[ ]`; `$( )` with text that is not a variable name (shell command substitution) is left unchanged.
- Output variable: `##vso[task.setvariable variable=V;isOutput=true]` in a step that has `name: N`.
  - Other job, same stage: `$[ dependencies.Job.outputs['N.V'] ]`.
  - Other stage: `variables: x: $[ stageDependencies.Stage.Job.outputs['N.V'] ]`, used as `$(x)`.
  - Stage conditions: `dependencies.Stage.outputs['Job.N.V']`. From a deployment job, the step reference is prefixed with the job name.
- The consuming stage must list the producing stage directly in `dependsOn` (e.g. `[Build, Dev]`); transitive dependencies are not visible.
- Every later stage that uses the digest (also a Verify stage after Prod) lists the producing stage in `dependsOn`, e.g. `[Build, Prod]`.
- Environment approvals/checks apply only to `deployment` jobs (`environment: prod`, `strategy: runOnce`). Deployment jobs do not check out the source: add `- checkout: self`. They download pipeline artifacts automatically.
- Also: `Cache@2` keys, `extends` templates for required stages, exclusive-lock checks.

## Pipeline health and DORA

- Success rate = succeeded / (succeeded + failed). Exclude canceled, skipped and never-started runs.
- Duration = finished − started; queue = started − created; report separately. Duration percentiles cover successful runs on the default branch; nearest-rank (`ceil(p·n)`-th sorted value) unless told otherwise; report n. Queue median covers every run that started.
- Flaky = same commit SHA and job with both a failed and a successful attempt (retry or rerun, also across runs of that SHA). Failing on one SHA and passing on another is not flaky.
- Deployment frequency = production deploys in the window ÷ days in the window (inclusive). Change failure rate = production deploys needing rollback or hotfix ÷ all production deploys. Lead time = median over commits of (production deploy finished − committed_at). Recovery time = median from a failed deploy to the next good production deploy, after sorting by time. Exclude non-production deploys and deploys outside the window.
- Never use these numbers to rate individual people.

## Migration

Map concepts, do not translate line by line: see `references/migration.md` (triggers, needs, cache, artifacts, variables, protected secrets → environments, `resource_group` → concurrency, manual job → environment approval).
