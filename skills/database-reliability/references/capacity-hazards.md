# Capacity hazards
- `integer` sequences stop at 2147483647. Also check foreign key columns that reference them. Widening to `bigint` rewrites the table: use an online plan.
- Transaction ID wraparound: watch `age(datfrozenxid)` and `age(relfrozenxid)`. Cleanup is held back by long transactions, idle-in-transaction sessions, prepared transactions, lagging replication slots and hot standby feedback. Find the oldest holder before tuning autovacuum.
