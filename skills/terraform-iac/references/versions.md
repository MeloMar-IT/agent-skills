# Version facts (Terraform)

| Construct | Minimum |
|---|---|
| `moved` | 1.1 |
| `optional()` with defaults | 1.3 |
| `import`, `check` blocks | 1.5 |
| `terraform test` | 1.6 |
| `removed`, `import` with `for_each`, `mock_provider` | 1.7 |
| Validation referring to other variables | 1.9 |
| Ephemeral values | 1.10 |
| Write-only arguments | 1.11 |

Raise `required_version` (for example `>= 1.7.0`) whenever you add one of these.

OpenTofu: state encryption is OpenTofu-specific, and `.tofu` files override `.tf` files of the same name. For any other OpenTofu version fact, say "check the release notes" unless official docs confirm it.
