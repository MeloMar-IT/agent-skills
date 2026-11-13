# Refactoring and state

- Rename: `moved { from = aws_s3_bucket.old to = aws_s3_bucket.new }`. Into a module: `to = module.logs.aws_s3_bucket.primary`. One block per resource.
- count to for_each: one `moved` per instance, `from = x[0]`, `to = x["key"]`. Adding `count` alone moves `x` to `x[0]` implicitly.
- Adopt existing objects with `import { to = ... id = ... }` (1.5+); `for_each` in `import` needs 1.7+. Applying an import needs authorization.
- Stop managing: remove the resource block and every reference to it, and add `removed { from = aws_db_instance.legacy lifecycle { destroy = false } }` (1.7+). Without `destroy = false` the object is destroyed.
- `terraform state mv|rm|push` and `force-unlock` bypass review: back up first (`state pull > backup.json`), keep locking on, never `-lock=false`, and require authorization. Prefer blocks when a pipeline only runs plan and apply.
