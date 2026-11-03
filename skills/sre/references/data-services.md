# Databases, caches, queues, and data recovery

## Contents

- Protect correctness and select the investigation
- Make integrity and storage guarantees explicit
- Inspect relational databases
- Inspect Cassandra, Redis, and Kafka
- Investigate pipelines and batch processing
- Execute a controlled recovery

## Protect correctness and select the investigation

Identify database/cluster/version, cloud account, role/primary, region, topology, replication/consistency mode, ownership, and affected business operations. Establish availability, latency, correctness and durability separately. A service can return HTTP 200 while dropping, duplicating or serving stale data. Define which invariants must survive: balances, uniqueness, ordering, referential relationships, authorization, retention, or a business-specific reconciliation total.

Record the first and last known good transactions, affected partitions/tenants, commit or checkpoint identifiers, and source of each fact. Avoid retrieving business rows when aggregate metadata or approved synthetic records answer the question. Read queries still consume resources, acquire locks in some cases, and expose data; bound runtime and results. Use least-privilege monitoring access and approved credential handling, never passwords on command lines.

Separate connection/authentication failure, query/lock contention, resource saturation, replication failure, storage failure, and application retry behavior. Compare one failing operation with a healthy operation on the same dependency and with a healthy shard/region. Correlate schema/config/index/deployment changes, traffic mix, maintenance and failover; do not assume the latest change is causal.

Before any failover, determine which writer is authoritative and how the old writer is fenced. Never promote both sides of a partition or remove quorum protection merely to make a dashboard green. Establish acknowledged-write guarantees and possible lost or divergent transactions. Keep the selected intervention within existing user authorization; obtain an additional decision only when its data-loss or access scope exceeds that authority.

## Make integrity and storage guarantees explicit

Translate each critical invariant into its enforcement point, relevant concurrency/failure cases, detection method, and recovery owner. Adapt chapter 17 of the supplied *Essential SRE Articles* through these concrete checks; see [source qualifications](essential-sre-insights.md).

| Integrity concern | Check against the real business model |
| --- | --- |
| Entity identity | Required identifiers exist and are unique within the intended scope. |
| Referential relationships | References resolve; deletion and updates preserve the intended relationships. |
| Domain validity | Types, ranges, formats, and allowed states remain valid. |
| Business rules | Balances, inventory, ownership, and state transitions satisfy the actual invariants. |
| Transactions/concurrency | Partial writes, retries, duplicates, and concurrent updates preserve required atomicity and isolation. |

State which properties are enforced by constraints, transactions, application code, messaging, or reconciliation. Database uptime and ACID support alone do not prove business correctness. Do not silently disable constraints to resolve integrity failures. Review parameterized queries, access separation, audit coverage, backup exposure, and key recovery alongside availability.

Distinguish relational, document, key-value, graph, time-series, persistent wide-column, and analytical columnar models. A wide-column system is not interchangeable with an analytical columnar store. Cassandra uses persistent SSTables and commit logs as well as in-memory buffers; do not classify it as an in-memory database. Verify actual consistency, transaction, durability, and indexing behavior for the deployed engine/version/configuration. "NoSQL" alone determines none of those guarantees. Derive acceptable staleness and consistency from the business invariant rather than imposing one consistency model on every workload. See the official [Cassandra storage engine](https://cassandra.apache.org/doc/latest/cassandra/architecture/storage-engine.html).

## Inspect relational databases

| Engine | Prioritized evidence | Interpretation traps |
| --- | --- | --- |
| PostgreSQL | Connections/waits; long transactions; locks/blockers; query-plan changes; WAL/archive and replication; disk/checkpoint/autovacuum | A missing lag value is not zero; stale transactions can block cleanup; a query timeout may still leave uncertain application outcomes. |
| MySQL | Performance Schema waits/threads; locks/long transactions; redo/binlog; replication channel/applier state; storage | Replica delay alone does not establish transaction completeness; avoid treating a stopped applier as just a connectivity failure. |
| SQL Server / Always On | Waits/blocking; transaction log; replica synchronization/send/redo queues; lease and health checks; WSFC/listener/client path | Database synchronization, cluster quorum, listener reachability and client reconnect are different recovery milestones. |

For PostgreSQL, begin with selected columns from `pg_stat_activity`, `pg_locks`, `pg_stat_replication`, replication slots and archiver views as relevant and permitted. Avoid query text unless necessary because literal SQL can expose personal data or secrets. Statistics availability and columns vary by version; current statistics are not an incident history. See the [statistics system](https://www.postgresql.org/docs/current/monitoring-stats.html).

An example bounded observation through a previously verified connection to the affected database is:

```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout = '3s';
SELECT state, wait_event_type, wait_event, count(*) AS sessions
FROM pg_stat_activity
WHERE datname = current_database()
GROUP BY state, wait_event_type, wait_event;
ROLLBACK;
```

This changes only session/transaction settings and reads metadata; it is not a universal performance test. Explain permission-limited visibility and timeout results. Inspect targeted blocking relationships before considering cancellation; terminating sessions may roll back large transactions and amplify load.

Distinguish ordinary `EXPLAIN` from `EXPLAIN ANALYZE`, which executes the statement. An apparent read query can call functions with side effects, and rollback does not erase every external effect. Do not run production statements simply to obtain a plan. Prefer existing plans and observed query statistics, then a controlled representative environment. See [EXPLAIN](https://www.postgresql.org/docs/18/sql-explain.html).

For replication, distinguish transport/write/flush/replay positions, synchronous acknowledgement policy and application read visibility. Asynchronous replication can lose acknowledged transactions during failover. Do not remove a replication slot or WAL to recover space until downstream recovery requirements are understood. Consult [PostgreSQL standby behavior](https://www.postgresql.org/docs/current/warm-standby.html).

For MySQL, select version-appropriate Performance Schema replication channel, connection and applier fields and relevant error metadata. Correlate GTID/binlog positions with application outcomes and source/replica connectivity. Avoid blind error skipping or reset/reseed operations: they can conceal divergence. Use [Performance Schema replication tables](https://dev.mysql.com/doc/refman/8.4/en/performance-schema-replication-tables.html) as the schema reference, matching the actual release.

For SQL Server Always On, align SQL error logs, AlwaysOn_health, cluster resource transitions and customer failures. Identify the initiating condition: quorum, lease/health timeout, manual action, host pressure, storage or replica transport. Verify synchronous/asynchronous mode and synchronization before selecting a destination. Measure failover, database readiness, listener resolution and application reconnection separately. Avoid forced quorum, forced failover or cluster-service restarts as generic remedies. Use Microsoft's [monitoring guide](https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/always-on-availability-groups-troubleshooting-and-monitoring-guide?view=sql-server-ver17) and [failover investigation](https://learn.microsoft.com/en-us/troubleshoot/sql/database-engine/availability-groups/troubleshooting-availability-group-failover).

## Inspect Cassandra, Redis, and Kafka

**Cassandra:** Establish replication factor and placement per data center, actual client consistency levels, coordinator/node health, token distribution, repair history, pending compactions, tombstones, GC and disk headroom. Use selected read operations such as `nodetool status`, `tpstats`, `compactionstats` and `netstats` under the correct local/remote authentication and version. Different consistency levels impose different acknowledgement requirements; do not lower them without assessing the business invariant. Quorum arithmetic is not a substitute for understanding concurrent writes, timestamps and application semantics. Review [Cassandra architecture](https://cassandra.apache.org/doc/stable/cassandra/architecture/dynamo) and [nodetool](https://cassandra.apache.org/doc/latest/cassandra/managing/tools/nodetool/nodetool.html).

Treat repair, cleanup, compact, rebuild, decommission and topology changes as load-producing or destructive operations. Check incremental/full repair semantics, interval, tombstone retention and topology before selecting a procedure. A generic repair during saturation may worsen the outage. See [repair guidance](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/repair.html).

**Redis:** Establish whether it is a disposable cache, session store, queue or source of record. Inspect selected `INFO` sections for memory, eviction, persistence, replication and clients; compare latency with command mix and host pressure. Avoid `KEYS *`, unrestricted `MONITOR` and whole-keyspace scans. Fields differ by release; see [INFO](https://redis.io/docs/latest/commands/info/). Treat key/value samples as production data.

Correlate eviction policy and TTL behavior with cache misses and downstream load. Inspect RDB/AOF completion and failures, fork/memory overhead and replication offsets. Replication is not an independent backup and asynchronous failover can lose writes. Before flushing, restarting or failing over, determine persistence, warm-up cost and durability requirements. Consult [persistence](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) and [replication](https://redis.io/docs/latest/operate/oss_and_stack/management/replication/).

**Kafka:** Inspect affected topics/partitions, producer acknowledgements/errors/retries, leaders and ISR, offline/under-replicated partitions, broker disks, retention, controller quorum and consumer groups. Compare lag in records with oldest-unprocessed age and partition throughput; high lag can reflect deliberate replay, while low lag can coexist with bad downstream processing. Inspect repeated rebalances, partition skew, poison messages and sink latency. Match monitoring names and quorum administration to the actual Kafka release and KRaft or legacy architecture; see [monitoring](https://kafka.apache.org/44/operations/monitoring/) and [KRaft](https://kafka.apache.org/42/operations/kraft/).

Resetting offsets, enabling unclean elections, changing ISR requirements or deleting topics can discard work or durability. Kafka transactions do not automatically make an external payment, email or database side effect exactly once. Establish offset/output atomicity or idempotency across the actual boundary. See [delivery semantics](https://kafka.apache.org/41/design/design/).

## Investigate pipelines and batch processing

Trace source → ingestion → queue → transform → storage → consumer. Record event time versus processing time, watermarks, expected partition completeness, checkpoints, dead-letter queues, schema/version compatibility and upstream/downstream contract changes. Separate missing, late, duplicated, corrupted and deliberately filtered records. A completed job is not proof its output is correct.

For replays and backfills, establish the exact interval and identifiers, deduplication key, idempotency, ordering requirements, concurrency, retention and downstream capacity. Use a small verifiable cohort first. Avoid blind full-dataset reprocessing. Validate source-to-sink counts and business totals where meaningful; explain exclusions and late-arrival semantics. Check schedules, timezone/DST transitions, overlapping jobs, missed triggers, resource limits and dependency gates.

## Execute a controlled recovery

State RPO and RTO targets separately from measured capability. Choose a recovery point using evidence, not just the newest backup filename. Verify backup completion, checksums where supported, encryption keys, identity, schema/engine compatibility, continuous log coverage, storage capacity and restore dependency order. For PostgreSQL PITR, a base backup and the required continuous WAL sequence must be available; use the actual version's [backup/recovery procedure](https://www.postgresql.org/docs/18/backup.html).

Restore into an isolated destination when feasible, preserving the original evidence. Validate integrity, expected transactions and business invariants before switching writers or traffic. Prevent duplicate writes during promotion and reconcile uncertain outcomes from retries. Record the actual data loss/window and time to usable service; a restore command succeeding is insufficient. Re-establish replicas, backup coverage, monitoring, fencing, recovery documentation and a follow-up restore test. If recovery cannot meet the target, state the gap and the decision needed explicitly.
