# Modules and providers

Child module `versions.tf`:
```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source                = "hashicorp/aws"
      version               = ">= 5.0"
      configuration_aliases = [aws.replica]
    }
  }
}
```
Caller:
```hcl
module "logs" {
  source    = "./modules/replicated-bucket"
  providers = { aws = aws, aws.replica = aws.replica }
}
```
- No `provider`/`backend` blocks in the module; minimum constraints only; the root pins `~>` and commits the lock file.
- Variables: type, description, validation. `for_each` keys known at plan time. `depends_on` on a module or data source defers reads until apply.
- Extraction keeps resources: add a `moved` block per resource into `module.<name>`; the `provider` blocks stay in the root.
