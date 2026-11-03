# Linux, virtual machines, and Windows

## Contents

- Establish host and workload identity
- Diagnose Linux by contention and failure evidence
- Inspect virtual infrastructure
- Diagnose Windows and clustered services
- Restore and verify

## Establish host and workload identity

Map service → process/container → guest OS → hypervisor/cloud host → storage/network. Record which layers are actually observable. Establish environment, host identity, OS/kernel, boot time, patch/build, service version, process/container/cgroup, CPU and memory limits, timezone and clock state. Use `hostname`, `uname -r`, `/etc/os-release` and process-specific metadata where applicable; avoid whole environment dumps and command lines that may contain credentials.

Compare the failing host with a healthy peer serving similar traffic. Preserve the incident interval before restarting a service or rotating logs. Distinguish current state from historical state: low CPU after a crash does not rule out earlier saturation, and counters reset at process or host restart. Missing monitoring is an explicit evidence gap.

Choose only commands needed to distinguish current hypotheses. Prefer installed tools and existing telemetry. Installing packages, attaching profilers, taking memory dumps, changing trace verbosity, or running stress tests are operational changes; establish scope, overhead and cleanup. Reads can consume resources, disclose information or block on failed mounts.

## Diagnose Linux by contention and failure evidence

| Branch | Initial evidence | Interpretation and next test |
| --- | --- | --- |
| CPU | Run queue; per-core utilization; throttling; process CPU; steal time | Separate CPU demand, throttling, lock contention and hypervisor scheduling. One saturated thread can coexist with low host average CPU. |
| Memory | Available memory; swap activity; major faults; OOM evidence; cgroup events; PSI | Separate cache from reclaim pressure, leaks, allocation limits and OOM. A process may hit its cgroup limit while the host has free memory. |
| Storage | Device latency, queueing, throughput; filesystem fullness/inodes; errors | Separate disk saturation, throttling, broken paths, filesystem exhaustion and remote mount latency. `%util` alone is insufficient for modern devices. |
| Process/service | Exit status, unit state, start/restart timestamps, dependency failures, open descriptors | Determine what terminated the process and whether the supervisor is amplifying the failure. A successful restart is mitigation evidence, not a causal explanation. |
| Network | Interface counters; socket states; retransmits; listening endpoint; route | Separate connectivity, name resolution, handshake, backlog and application latency. Correlate with the network playbook. |
| Time | Clock offset, source, synchronization state, jumps and boot/migration events | Preserve offset uncertainty in the timeline. Inspect time-sensitive authentication, leases and certificate validation. |

Useful bounded observations, where these tools exist:

```bash
uptime
vmstat 1 5
iostat -xz 1 3
free -m
cat /proc/pressure/cpu /proc/pressure/memory /proc/pressure/io
```

Read the first report's semantics; some tools initially show averages since boot. Use the later interval samples for incident contention. PSI measures time tasks are stalled on resources and complements utilization; distinguish `some` from `full` and host from workload scope. See the kernel's [PSI documentation](https://docs.kernel.org/accounting/psi.html).

Locate the affected process's actual cgroup and confirm v1 versus v2 before reading controller files. For cgroup v2, inspect selected `cpu.stat`, `cpu.max`, `memory.current`, `memory.max`, `memory.high`, `memory.events`, `memory.stat` and pressure files where present. Compare counters over a bounded interval; distinguish local from hierarchical events. `memory.high` reclaim/throttling differs from `memory.max` enforcement. Avoid writing to control files as a diagnostic shortcut. See [cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html).

Use `df -h` and `df -i` only on the affected mount when possible. Check `findmnt`/`lsblk` for the mount-to-device mapping. Avoid recursive filesystem scans during an I/O incident. If deleted-but-open files are suspected, inspect the relevant process's descriptors or a narrowly scoped `lsof`; do not truncate file descriptors or remove application files to obtain space without understanding recovery consequences. Never delete database logs or change filesystem ownership recursively as an incident reflex.

For systemd services, set verified unit and explicit UTC bounds, then select the relevant fields and logs:

```bash
: "${SRE_UNIT:?}" "${SRE_START_UTC:?}" "${SRE_END_UTC:?}"
systemctl show "$SRE_UNIT" \
  -p ActiveState -p SubState -p Result -p ExecMainStatus -p NRestarts
journalctl -u "$SRE_UNIT" --since "$SRE_START_UTC" \
  --until "$SRE_END_UTC" --utc --no-pager -n 200
```

Include `UTC` in bound strings so input interpretation is explicit. Select kernel messages over the same window if investigating OOM, I/O, network-driver or hung-task evidence. Review logs for secrets before outputting them. `journalctl` filtering, output timezone and record limits are documented in its [manual](https://freedesktop.org/software/systemd/man/latest/journalctl.html). `systemctl status` or broad `show` output can reveal command arguments; the narrowed fields above avoid unnecessary disclosure.

For suspected CPU/GC/runtime issues, correlate service latency with language runtime evidence: JVM pauses and thread pools; .NET GC/thread-pool queues; Python worker concurrency; Go goroutine pressure; native allocator growth. Take stack samples only with approved attachment and overhead limits. Avoid core dumps by default: they may contain secrets and customer data.

## Inspect virtual infrastructure

Correlate guest and hypervisor clocks and events: placement changes, vMotion/live migration, snapshots, backup jobs, host contention, storage path changes, HA restarts, maintenance, and cloud instance events. Treat timing as a candidate mechanism, not proof that migration caused the incident.

Check CPU ready/co-stop or equivalent host scheduling metrics, guest steal time where meaningful, memory ballooning/swapping, reservations/limits, NUMA placement, datastore latency, storage throttling/burst credits and NIC drops. A guest without scheduling visibility cannot exclude a hypervisor bottleneck. Ask the owning platform for a bounded metric/event extract rather than guessing.

Verify redundancy across physical failure domains. Two guests on one host or datastore do not provide independence against that shared failure. Inspect anti-affinity, reserved failover capacity and placement rules without assuming configured rules were effective at incident time.

A VM snapshot depends on its underlying disk chain and is not an independent backup. Snapshot creation, consolidation and reversion can pause workloads, consume space, or rewind state. Reverting a database or directory server requires product-specific consistency and replication planning; do not apply a generic snapshot rollback. See [VMware snapshot practices](https://knowledge.broadcom.com/external/article/318825/best-practices-for-using-vmware-snapshot.html). Establish crash consistency versus application consistency, restore tests, credentials/keys and recovery dependency order.

For cloud VMs, verify the account/region/instance identity, provider health, guest agent, extension state, disk and NIC limits, routing/security controls, identity access, maintenance and quota. Do not assume a healthy provider status page excludes one host, zone or account-specific failure.

## Diagnose Windows and clustered services

Identify Windows build, recent update/reboot, service account, process identity, relevant Event Log channels, system time and performance-counter availability. Use known provider/event filters and explicit time bounds; log messages can include connection strings and user data. An example bounded read, after binding actual times:

```powershell
$SreStart = [DateTimeOffset]::Parse('2026-11-03T06:00:00Z').UtcDateTime
$SreEnd = [DateTimeOffset]::Parse('2026-11-03T06:15:00Z').UtcDateTime
Get-WinEvent -FilterHashtable @{
  LogName = 'System'; StartTime = $SreStart; EndTime = $SreEnd
} -MaxEvents 100 | Select-Object TimeCreated, Id, ProviderName, LevelDisplayName
```

The timestamps are illustrative; replace them with the incident interval. Retrieve selected event messages only when their IDs/provider justify it. See [Get-WinEvent](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.diagnostics/get-winevent?view=powershell-7.5).

Inspect service failures, CPU/working-set/commit pressure, disk latency/queues, pagefile exhaustion, network endpoints, Defender/EDR activity, certificate stores and scheduled tasks as hypotheses require. For Active Directory dependencies, correlate DNS/SRV resolution, DC availability/replication, secure channel, Kerberos clock tolerance, SPNs, account lockout and certificate trust. Avoid domain-wide repair or policy changes based on one client error.

For WSFC/SQL Server Always On, align Windows events, cluster resource transitions, SQL error log, AlwaysOn_health and client reconnect evidence. Distinguish node/cluster quorum, witness, listener/DNS/IP conflicts, lease expiry, health-check timeout, replica synchronization, database recovery and client behavior. Quarantine or isolation is evidence of protection behavior; do not disable it or restart cluster services merely to clear a status. Use the [Always On failover investigation guide](https://learn.microsoft.com/en-us/troubleshoot/sql/database-engine/availability-groups/troubleshooting-availability-group-failover) and the data-services playbook for state and durability decisions.

## Restore and verify

For each authorized intervention, specify the affected service/host, dependencies, preserved evidence, failure domain, stop condition and recovery path. Change one meaningful variable at a time when practical. Verify service behavior, data integrity, clock stability, resource headroom and peer redundancy across a representative observation window. Recheck scheduled work and backup/monitoring agents that may have been paused. Record the reason the intervention helped separately from any unproven causal claim.
