---
name: database-reliability
description: "Engineers relational database reliability, mainly PostgreSQL: online schema migrations, lock contention triage, PgBouncer pooling and connection budgets, least-privilege roles, backup and point-in-time recovery, replication and failover (MySQL GTID, SQL Server availability groups), sequence exhaustion and transaction ID wraparound. Use when changing a PostgreSQL schema without downtime, reviewing pooling or privileges, planning a restore, or judging a failover candidate. Not for Cassandra, Kafka, IBM MQ, Redis, Oracle or ORM tutorials."
metadata:
  capabilities: [database-reliability, online-schema-migration, lock-contention-triage, connection-pooling, connection-pool-sizing, least-privilege-roles, database-access-control, point-in-time-recovery, backup-restore-verification, replication-failover, mysql-gtid-failover, sql-server-availability-groups, sequence-exhaustion, transaction-id-wraparound]
  technologies: [postgresql, mysql, sql-server, pgbouncer]
---

# Database reliability

## Stance
- Scope: PostgreSQL (schema changes, locks, pooling, privileges, backup and PITR, replication, ID exhaustion, wraparound). MySQL: GTID failover only. SQL Server: availability group failover only. Incident command, SLOs and postmortems: use `skills/sre`.
- Label statements observed, reported, inferred, hypothesis or unknown. Never invent query results, commands run, metrics, owners or approvals. Say plainly what was offline or not run.
- Read-only first. These need explicit authorization for that action plus its preconditions: `pg_terminate_backend`, `ROLLBACK PREPARED`, dropping a replication slot, failover or forced failover, a restore that replaces data.
- No credentials in SQL or config files. State the version for version-sensitive facts. Link only official https documentation.

## Online schema migration (PostgreSQL)
- Most `ALTER TABLE` forms take ACCESS EXCLUSIVE. A waiting lock request blocks every later conflicting request, so one waiting DDL stalls all reads. Begin each DDL transaction with `SET lock_timeout` (and `statement_timeout`) and retry on timeout.
- `ADD COLUMN … DEFAULT <non-volatile>` (constants, `now()`, `NOT NULL DEFAULT 'x'`) is metadata-only from PostgreSQL 11: one statement, never backfill. A volatile default (`gen_random_uuid()`, `clock_timestamp()`, `random()`) rewrites the table. Instead: add the column with no default; `ALTER COLUMN … SET DEFAULT` as a separate statement; backfill outside migrations in batches (`LIMIT` or key ranges) and only `WHERE col IS NULL`, so a re-run never overwrites values new rows already got.
- `int` to `bigint` rewrites the table; raising `varchar(n)` or `varchar` to `text` does not.
- NOT NULL: `ADD CONSTRAINT c CHECK (col IS NOT NULL) NOT VALID`; `VALIDATE CONSTRAINT c` (SHARE UPDATE EXCLUSIVE); `SET NOT NULL` (PostgreSQL 12+ skips the scan given a validated check); drop the check. PostgreSQL 18 can add NOT NULL as NOT VALID directly.
- Foreign keys: `ADD … FOREIGN KEY … NOT VALID` (SHARE ROW EXCLUSIVE on both tables), then `VALIDATE CONSTRAINT` in a separate, later transaction/file: locks last until commit, so validating in the same transaction blocks writes for the whole scan.
- `CREATE [UNIQUE] INDEX CONCURRENTLY` cannot run in a transaction block. A multi-statement query string is an implicit transaction, so a file sent without its own transaction must hold exactly that one statement: no `SET`, no `DROP … IF EXISTS` before it. A failed build leaves an INVALID index: `DROP INDEX CONCURRENTLY`, retry. Make it a constraint with `ADD CONSTRAINT … USING INDEX`.
- Renames and drops: expand, then contract, because two app versions run side by side.

## PgBouncer pooling
- Transaction mode breaks: session `SET`/`search_path`, session advisory locks (`pg_advisory_lock`, `pg_try_advisory_lock`), `LISTEN`, `WITH HOLD` cursors, SQL-level `PREPARE`/`EXECUTE` (even with `max_prepared_statements`), temp tables living across transactions. Safe: `SET LOCAL`, `pg_advisory_xact_lock`, `ON COMMIT DROP` temp tables inside one transaction, protocol-level prepared statements on PgBouncer 1.21+ with `max_prepared_statements` > 0.
- Budget: pools are per (database, user) pair; each opens `pool_size` (or `default_pool_size`; a per-database `pool_size` overrides it) plus `reserve_pool_size`. Multiply by PgBouncer instances that can run at once (a percentage `maxSurge` rounds up; `maxSurge: 0` adds none). `max_db_connections` caps server connections per PgBouncer database entry (reserve included) per instance: per entry take the smaller of the cap and the sum of its pools. Add clients connecting straight to PostgreSQL (a CronJob that may overlap counts its max). Client-side pool sizes count against PgBouncer `max_client_conn`, not server connections.
- Slots for app roles = `max_connections − superuser_reserved_connections − reserved_connections` (`reserved_connections` from PostgreSQL 16). WAL senders (12+) and autovacuum workers use separate slots. Fits only if worst case ≤ slots.

## Privileges
- Owner role NOLOGIN, NOLOGIN group roles, login roles as members. Grant schema `USAGE`. `GRANT … ON ALL … IN SCHEMA` covers only existing objects.
- `ALTER DEFAULT PRIVILEGES` affects only objects created by the `FOR ROLE` target (default: the role running it): always write `FOR ROLE owner`. `IN SCHEMA` defaults only add to global ones; removing PUBLIC's default EXECUTE on new functions needs a global `ALTER DEFAULT PRIVILEGES FOR ROLE owner REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC`; also revoke EXECUTE on existing functions.
- `serial`/`bigserial` columns need sequence `USAGE`. PUBLIC has CONNECT and TEMP on every database. PostgreSQL 15 removed PUBLIC's CREATE on schema `public` only for new clusters/databases; `pg_upgrade` or restored dumps keep it, so revoke explicitly.
- Avoid `pg_read_all_data`/`pg_write_all_data`, `GRANT ALL`, `WITH GRANT OPTION`, `TRUNCATE`. `SECURITY DEFINER` needs `SET search_path`.

## Backup and point-in-time recovery
- A base backup is usable only if it completed, stopped before the recovery target, and archived WAL is continuous from its start segment to the target along the target timeline (retention may have removed the start segment). Pick the newest usable one.
- WAL names are timeline + log ID + segment; after `…FF` comes the next log ID.
- A `duration:` log line is stamped when the statement ends, so the transaction began at least that long earlier: with only a time known, subtract the duration and stay before it. Prefer an XID or LSN target with `recovery_target_inclusive = off`. A time target needs an explicit zone (else server `TimeZone`). Set exactly one `recovery_target*`.
- PostgreSQL 12+: default timeline is `latest`; pin `recovery_target_timeline` when the archive holds timelines from other promotions or test restores (read the `.history` files). Use `recovery.signal`, not `standby.signal`; `recovery.conf` is unsupported.
- `recovery_target_action = pause` acts like `shutdown` when `hot_standby` is off. A restore copy must not archive into the production archive: `archive_mode = off` or a separate archive.
- Verify against business invariants; record measured RPO and RTO.

## References
- [lock-triage](references/lock-triage.md), [replication-failover](references/replication-failover.md), [capacity-hazards](references/capacity-hazards.md).
