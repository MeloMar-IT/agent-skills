# shop roles

Database `shop` on PostgreSQL 16, in a cluster upgraded from 13 with `pg_upgrade`.
Schema `app` is owned by `app_owner` (NOLOGIN). Migrations run `SET ROLE app_owner`.
`sql/roles.sql` is run once by `dba_admin` (CREATEROLE, member of `app_owner`, not a superuser).

Policy:
- `app_rw`: SELECT, INSERT, UPDATE and DELETE on current and future tables in `app`, plus use of its sequences and execution of its functions.
- `app_ro`: SELECT on current and future tables only.
- Login roles: `orders_svc` (member of `app_rw`) and `bi_reader` (member of `app_ro`). A secrets operator sets the passwords.
- Only `app_owner` may create objects in `app` or `public`.
- Only these roles may connect to `shop`; nobody may create temp tables.
- No other role may execute functions in `app`, now or in future.
- None of these roles exist yet (except `app_owner` and `dba_admin`).
- Plain SQL only: no DO blocks, no psql meta-commands.
