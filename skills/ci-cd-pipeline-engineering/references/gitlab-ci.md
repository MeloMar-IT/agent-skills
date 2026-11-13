# GitLab CI details

Docs: https://docs.gitlab.com/ee/ci/yaml/

## Workflow rules without duplicates

```yaml
workflow:
  auto_cancel:
    on_new_commit: interruptible
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS
      when: never
    - if: $CI_COMMIT_BRANCH
```

## Monorepo jobs and a deploy that tolerates missing builds

```yaml
backend_build:
  interruptible: true
  rules:
    - changes: [backend/**/*]
deploy_production:
  interruptible: false
  needs:
    - { job: backend_build, optional: true }
    - { job: frontend_build, optional: true }
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
```

`rules:changes` semantics: MR pipelines diff against the target branch; branch pipelines against the previous push; new branches always match. `changes:compare_to` pins the reference. Jobs on the default branch should usually run unconditionally if later jobs depend on their artifacts.

## Misc

- `cache: key: files: [lockfile]` (max 2 files), `policy: pull` for consumers; artifacts with `expire_in` carry outputs.
- `resource_group: production` serializes deploys.
- `parallel: 4` with `CI_NODE_INDEX` (from 1) and `CI_NODE_TOTAL` to shard tests.
- `when: manual` in `rules` defaults to `allow_failure: false` and blocks the pipeline; set `allow_failure: true` for an optional step.
