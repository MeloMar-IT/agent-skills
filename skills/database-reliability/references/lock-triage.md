# Lock-chain triage (PostgreSQL, read-only)
- Find waiters and blockers with `pg_blocking_pids(pid)` over `pg_stat_activity`; follow the chain to the root blocker.
- Root blockers are often `idle in transaction`. `pg_cancel_backend` cancels a running query only; it does not end an idle-in-transaction session. Ending it needs `pg_terminate_backend`, which needs explicit authorization.
- A block held by a prepared transaction shows as pid 0; look in `pg_prepared_xacts`. `ROLLBACK PREPARED` needs explicit authorization.
- Queued DDL blocks all later conflicting requests: the visible victim is often not the cause.
- Prevent with `lock_timeout` and `idle_in_transaction_session_timeout`.

Docs: https://www.postgresql.org/docs/current/explicit-locking.html
