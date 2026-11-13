# Orders database migrations

PostgreSQL 16. Migrations in `migrations/` are applied in filename order.

Each file is sent as ONE simple-query string. By default the runner sends BEGIN, the file, then COMMIT. If the first line is exactly `-- runner: no-transaction` the file is sent as-is.

- `orders` has about 400 million rows and about 2,500 writes per second.
- Reporting queries on the primary run up to 90 s.
- Two app versions run side by side during deploys.
- Operators run backfills from `backfill/` with psql.
