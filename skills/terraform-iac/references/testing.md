# Testing

- `run` blocks default to `command = apply` and create real resources. Set `command = plan` for unit tests.
- Use `mock_provider "aws" {}` (1.7+) so no credentials are needed; `terraform test` itself needs 1.6.
- Validation rules: `expect_failures = [var.name]` in a run block that supplies a bad value.
- Do not claim tests passed unless they ran; providers cannot be installed offline.
