# GitHub Actions details

Docs: https://docs.github.com/actions

## Change-detecting gate for a required check

```yaml
jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      backend: ${{ steps.diff.outputs.backend }}
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - id: diff
        run: |
          # compare against the PR base or the previous push; set backend=true|false
          echo "backend=true" >> "$GITHUB_OUTPUT"
  backend:
    needs: changes
    if: needs.changes.outputs.backend == 'true'
    runs-on: ubuntu-latest
    steps:
      - run: make backend-test
  ci-gate:
    needs: [changes, backend]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - run: test "${{ contains(needs.*.result, 'failure') || contains(needs.*.result, 'cancelled') }}" = "false"
```

Skipped needs report `skipped`, which is acceptable; `failure` and `cancelled` are not.

## Permissions and OIDC

Top level `permissions: contents: read`; raise per job. A job with `permissions: id-token: write` loses every other scope, so add `contents: read`. Cloud access: exchange the OIDC token with the provider's trust policy bound to repo and environment; no stored keys.

## Untrusted input

Unsafe: `run: echo "${{ github.event.pull_request.title }}"`. Safe: `env: TITLE: ${{ github.event.pull_request.title }}` and `run: echo "$TITLE"`. Same for `github.head_ref` and commit messages. `pull_request_target` runs with secrets: never check out or run the PR head there.

## Artifacts v4

Unique name per matrix job, `pattern` + `merge-multiple: true` on download, `include-hidden-files: true` for dot-directories, retention set explicitly.

## Concurrency

```yaml
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
# deploy job:
concurrency: { group: deploy-prod, cancel-in-progress: false }
```
