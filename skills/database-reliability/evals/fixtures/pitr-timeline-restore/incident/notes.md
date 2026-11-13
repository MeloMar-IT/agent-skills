# Incident notes

PostgreSQL 16. Server `log_timezone` is Europe/Berlin.

Log excerpt:

    2026-11-03 14:07:31.204 CET [41822] app_rw@shop LOG:  duration: 5123.004 ms  statement: DELETE FROM invoices

Goal: an isolated, read-only copy on `restore-01` at the last state before that transaction. Someone else decides on promotion.

Earlier on 2026-11-03 a colleague tested a restore on another host; details unknown.

The WAL archive is mounted read-only at `/mnt/wal-archive`.
