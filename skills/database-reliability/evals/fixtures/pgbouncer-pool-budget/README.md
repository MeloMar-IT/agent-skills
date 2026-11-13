# Shop connection setup

PostgreSQL 16 and PgBouncer 1.22.1. The driver runs in autocommit mode; `with conn.transaction():` wraps BEGIN/COMMIT. No app role is a member of `pg_use_reserved_connections`.
