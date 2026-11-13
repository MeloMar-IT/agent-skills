---
name: terraform-iac
description: "Writes, reviews and refactors Terraform and OpenTofu code safely: plan JSON summaries and gates with secret redaction, moved/removed/import blocks, retiring and protecting resources, reusable modules with provider aliases, version constraints and lock files, and CI jobs that apply the reviewed plan. Use when a task touches terraform or opentofu files, plan or state JSON, or terraform CI scripts; not for Pulumi, CloudFormation or Bicep, or for incident work (use sre)."
metadata:
  capabilities: [terraform, opentofu, terraform-plan-review, terraform-state-refactoring, terraform-modules, terraform-ci, terraform-testing]
  technologies: [terraform, opentofu, hcl]
---

# Terraform and OpenTofu

## Operating stance

Make the reviewed plan the thing that is applied, destroy nothing by accident, and let no secret reach a log or comment. Prefer reviewable configuration (blocks, files) over imperative commands. Incidents and outages belong to the `sre` skill.

| Task | Read |
|---|---|
| Parse, summarize or gate plan or state JSON; redact secrets | [references/plan-json.md](references/plan-json.md) |
| Rename, move, import, stop managing, `state` commands | [references/refactoring-and-state.md](references/refactoring-and-state.md) |
| Adding a language construct, `required_version`, OpenTofu differences | [references/versions.md](references/versions.md) |
| Extracting or writing modules, provider aliases, variables | [references/modules-and-providers.md](references/modules-and-providers.md) |
| CI scripts, `.gitignore`, lock files, drift jobs | [references/pipelines.md](references/pipelines.md) |
| `terraform test`, mocks | [references/testing.md](references/testing.md) |

## 1. Evidence and authority
- Find the tool and version first: `required_version`, `.terraform.lock.hcl`, the CI image.
- Label claims observed, reported, inferred, hypothesis or unknown.
- Do not claim init, plan, apply or test ran. Say which checks were not run; providers cannot be installed offline.
- `plan` runs provider code and data sources and takes a state lock; it is not free of side effects.
- Apply, destroy, `state` commands, `force-unlock` and imports change real infrastructure: do them only with explicit authorization.
- Do not invent provider hashes, IDs, owners or approvals.

## 2. Plan and state JSON
- `["delete","create"]` and `["create","delete"]` are both a replace; the second is create-before-destroy. Do not classify by `actions[0]`.
- `["no-op"]` with `change.importing` is an import; `["no-op"]` with `previous_address` is a move. Report both; drop plain no-ops.
- `mode: "data"` with `["read"]` is a read, not an infrastructure change. List `action_reason` values. A `deposed` entry is a separate object at the same address.
- `resource_changes` may be missing. Fail closed on `errored`, malformed input or an unknown action combination. `resource_drift` is change made outside Terraform.
- `show -json` and `output -json`/`-raw` print sensitive values in clear. The only signal is `before_sensitive` / `after_sensitive`: `true` for the whole value, or a nested map/list mirroring the value with `true` on sensitive leaves. Walk those trees recursively, for before and after. Do not print `variables`, `prior_state` or `planned_values` raw. Render `after_unknown` leaves as "(known after apply)". Plan files are secret artifacts.

## 3. Refactoring without destroying
- Use `moved` blocks (1.1+) for renames and moves into a module; count to for_each needs one `moved` per instance (adding `count` maps `x` to `x[0]` implicitly, `for_each` does not).
- To stop managing a resource without destroying it: delete the resource block and every reference to it (outputs, other resources), and add `removed { from = ... lifecycle { destroy = false } }` (1.7+).
- Prefer config blocks to `state` commands, which bypass review. For `state` commands take a backup and never pass `-lock=false`.

## 4. Version truth
- When you add a construct, raise `required_version` to the release that supports it (table in references/versions.md) and check the constraint admits that release.
- Keep OpenTofu-only features separate; state a version fact only if official docs confirm it, otherwise say "check the release notes".

## 5. Protecting data
- `prevent_destroy` stops working once the block is removed from configuration. Pair it with the provider's own protection: `deletion_protection = true` on `aws_db_instance`, `skip_final_snapshot = false` plus `final_snapshot_identifier`, `force_destroy = false` on S3 buckets, `deletion_protection_enabled` on DynamoDB tables.

## 6. Modules
- Child modules contain no `provider` or `backend` blocks. Declare aliases with `configuration_aliases` in `required_providers`; the caller passes `providers = { aws = aws, aws.replica = aws.x }`.
- Reusable modules set only minimum constraints (`>=`); the root pins with `~>` and commits `.terraform.lock.hcl`.
- Variables get a type, description and validation. `for_each` keys must be known at plan time. `depends_on` on a module or data source defers reads to apply.
- When moving resources into a module, add `moved` blocks so nothing is recreated.

## 7. CI pipelines
- `terraform init -input=false -lockfile=readonly`; no `-upgrade` in a deploy job.
- Use `-lock-timeout`, not `-lock=false`.
- `plan -out=tfplan`, then apply that saved file; do not re-plan with `-auto-approve`.
- `-detailed-exitcode` returns 0, 1 (error) or 2 (changes); `set -e` stops on 2. Drift jobs use `-refresh-only`.
- `.gitignore`: `.terraform/`, `*.tfstate`, `*.tfstate.*` (backups), plan files and any saved `show` output such as `plan.txt` (it holds secrets), `crash.log`. Do not ignore `.terraform.lock.hcl`; use `providers lock -platform=...` for several platforms.
- No credentials in provider blocks or committed tfvars; prefer OIDC.

## 8. Testing
- `run` blocks default to `command = apply` and create real resources. Unit tests use `command = plan` with `mock_provider` and `expect_failures` for validation rules.
