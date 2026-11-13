# Replication and failover
- Always fence the old primary before promoting. Failover needs explicit authorization.
- PostgreSQL: an unused or lagging replication slot retains WAL and can fill the disk; bound it with `max_slot_wal_keep_size`. Dropping a slot needs explicit authorization.
- MySQL GTID: choose the candidate by Executed ∪ Retrieved GTID sets (relay-log events not yet applied count). Check for errant GTIDs (present on a replica, absent on the source). Semi-sync `AFTER_SYNC` means committed transactions reached at least one replica's relay log.
- SQL Server availability group: only a `SYNCHRONIZED` synchronous-commit replica fails over without data loss; otherwise a forced failover with possible data loss, which needs explicit authorization.
