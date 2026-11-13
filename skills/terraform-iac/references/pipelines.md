# Pipelines

```sh
set -eu
terraform init -input=false -lockfile=readonly
terraform plan -input=false -lock-timeout=5m -out=tfplan
terraform show -no-color tfplan > plan.txt   # may hold secrets; redact before sharing
terraform apply -input=false tfplan
```
- A saved plan needs no `-auto-approve`; apply it, do not re-plan. Applying anything but the reviewed plan is the failure to avoid.
- `-upgrade` belongs in a reviewed change that updates `.terraform.lock.hcl`, not in the deploy job.
- `-detailed-exitcode`: 0 none, 1 error, 2 changes. Under `set -e` capture it: `rc=0; terraform plan -detailed-exitcode ... || rc=$?`. Drift job: `plan -refresh-only -detailed-exitcode`.
- `.gitignore`: `.terraform/`, `*.tfstate`, `*.tfstate.*`, `tfplan`, saved `show` output such as `plan.txt`, `crash.log`. Keep `.terraform.lock.hcl` committed; `terraform providers lock -platform=linux_amd64 -platform=darwin_arm64` for several platforms.
- Credentials via OIDC or the environment, not provider blocks or committed tfvars.
