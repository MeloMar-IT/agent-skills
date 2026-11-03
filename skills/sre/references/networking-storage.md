# Network, identity, time, and storage foundations

## Contents

- Model the path and choose a comparison
- Diagnose DNS, connectivity and TLS
- Inspect network controls and identity
- Diagnose storage from application to media
- Recover and verify

## Model the path and choose a comparison

Draw the actual request path: client/resolver → proxy/CDN/WAF/load balancer → gateway/service → application → dependency. Record source and destination identities, protocol, port, DNS name, address family, region/zone, endpoint and time. Identify which segments are controlled by other teams. Add the return path: asymmetric routing can make a working forward route misleading.

Choose a matrix that separates mechanisms: affected and healthy clients; one failing and healthy zone; DNS name and selected address; direct dependency and normal service path. Preserve hostname/SNI and authorization when selecting an address. Do not bypass a mandatory proxy, firewall, identity check or policy boundary merely to obtain a successful test. Explain what each comparison proves and what remains unchanged.

Prefer existing metrics, connection/error samples, deployment/audit records and scoped configuration excerpts. A probe creates traffic; a packet capture creates a sensitive artifact. Bound destination, rate, duration, sample size and output. Never scan a subnet or capture all traffic as an initial step. Retain timestamps and measurement location so observations can be compared.

## Diagnose DNS, connectivity and TLS

Use a known permitted endpoint and verified nonempty variables. Examples below perform a small number of active requests; they are not passive telemetry. Ensure the selected HTTP path has no business side effect.

```bash
: "${SRE_DNS_NAME:?}" "${SRE_HTTPS_URL:?}"
dig "$SRE_DNS_NAME" A +time=2 +tries=1
dig "$SRE_DNS_NAME" AAAA +time=2 +tries=1
curl --silent --show-error --connect-timeout 3 --max-time 10 \
  --max-filesize 16384 --output /dev/null \
  --write-out 'status=%{http_code} dns=%{time_namelookup} tcp=%{time_connect} tls=%{time_appconnect} first_byte=%{time_starttransfer} total=%{time_total}\n' \
  "$SRE_HTTPS_URL"
```

Interpret curl timings as cumulative milestones, not independent stage durations. A completed curl invocation can return an HTTP error status without a failing process exit code; inspect both. A response-size limit or timeout deliberately interrupts collection and must remain visible in the evidence. Do not add `-k`, attach tokens to command arguments, follow redirects into unverified destinations, or include verbose request headers in shared evidence. See the official [curl manual](https://curl.se/docs/manpage.html) and [BIND dig documentation](https://bind9.readthedocs.io/en/v9.20.23/manpages.html).

For DNS, distinguish NXDOMAIN, NODATA, SERVFAIL, timeout and stale answers. Compare the resolver actually used by the application with authoritative data through authorized queries; inspect split-horizon zones, delegation, records, TTLs, negative caching, search suffixes and DNSSEC errors as relevant. A workstation result does not prove the application resolves the same name. Do not move clients to a public resolver as a generic fix for private-zone failures.

For TLS, verify the server name, certificate chain and trust store, validity interval, negotiated protocol, SNI/ALPN, client certificate identity and revocation dependencies where used. Different nodes or proxies may present different certificates. A TCP connection alone does not establish a valid TLS session. If OpenSSL and a compatible timeout utility are already installed, a bounded inspection is:

```bash
: "${SRE_TLS_HOST:?}"
timeout 10s openssl s_client -connect "${SRE_TLS_HOST}:443" \
  -servername "$SRE_TLS_HOST" -verify_hostname "$SRE_TLS_HOST" \
  -verify_return_error -brief </dev/null
```

Use the real port and appropriate trusted CA configuration for the environment. `-verify_return_error` matters because diagnostic clients may otherwise continue after verification errors. `timeout` is an external utility, not an OpenSSL flag; choose an available bounded equivalent on other operating systems. Do not export private keys. See [OpenSSL s_client](https://docs.openssl.org/3.0/man1/openssl-s_client/).

## Inspect network controls and identity

| Evidence pattern | Investigate | Avoid concluding |
| --- | --- | --- |
| Name resolves but connection times out | Source/return route, security rules, listener, LB health, address family | Timeout proves a firewall caused it. |
| TCP works; TLS fails | Name/trust/expiry/mTLS/clock/protocol | Server process is healthy because the port opens. |
| Small requests work; large transfers stall | MTU/PMTUD, retransmits, proxy limits, congestion | DNS is responsible for every intermittent connection. |
| Failure only under traffic spikes | NAT/conntrack/ephemeral ports, accept queues, pooling, limits | More application replicas always create more capacity. |
| One zone or node fails | Routes, CNI, subnet/IP exhaustion, zonal appliance or backend | Healthy global averages exclude a localized outage. |
| Authentication suddenly fails | Identity provider, keys/JWKS, audience/issuer, token expiry, time, policy rollout | Every 401/403 is a password problem. |

Inspect relevant routes, interface counters, sockets and policy rules using the host or cloud's supported read commands. Correlate flow logs with both accepted and denied traffic; aggregation or missing logs limits what they prove. Distinguish cloud security groups/NSGs, host firewall, WAF, service-mesh policy and Kubernetes NetworkPolicy rather than treating them as one boundary. Identify stateful versus stateless rules and return-path requirements.

For IPAM, compare address allocations, DHCP leases, static assignments, ARP/neighbor observations and switch/cloud records over time. A duplicate address hypothesis needs conflicting ownership evidence. Do not move a cluster/listener IP until dependencies and authoritative ownership are understood.

For identity, trace user/workload → issuer → token/credential → service validation → authorization decision. Check rotation overlap, cached keys, RBAC/group propagation, federation and managed/workload identity changes. Inspect credential metadata and expiry without retrieving secrets. Separate permission failures from network failures; request the narrow owning-team action when access is legitimately unavailable.

For time, use current offset and source status together with historical clock events. `chronyc tracking` and `chronyc sources` are useful where chrony is installed; a source being reachable is not sufficient proof the system is synchronized. Use [chrony monitoring semantics](https://chrony-project.org/doc/4.4/chronyc.html). A step adjustment can affect leases and time ordering; changing time is an intervention, not a read diagnostic. Mark timestamp uncertainty instead of inventing a precise sequence across skewed hosts.

If captures are necessary, select the interface, host/port filter, finite duration and packet count, minimum needed payload, approved destination and retention. Protect application payloads, tokens and private addresses. Avoid debug logs or decrypted traffic when counters and handshake metadata answer the question. Use an existing packet-capture process where available.

## Diagnose storage from application to media

Map application file/table/object → filesystem/mount → volume → storage pool/backend → physical or cloud failure domain. Record device and filesystem identity, access mode, quotas, mount options, capacity/inodes, free reserve, latency, throughput, IOPS, queueing, errors and provider limits. Differentiate network filesystem, block storage, object storage and local ephemeral disk; their guarantees and failure modes differ.

Compare application latency with backend/device observations. A full filesystem, exhausted inodes, application quota, thin pool, cloud throttling or unavailable key can all reject writes despite apparently free capacity elsewhere. Increasing volume size does not necessarily expand the partition/filesystem. Determine which component requires expansion before proposing a change.

For NFS/SMB, inspect server availability, authentication, locks, mount state and timeout behavior. Avoid traversing a hung remote mount with an unbounded filesystem scan. For multipath/SAN, inspect path state and controller events before considering a rescan or failover. Those operations can disrupt I/O.

For Kubernetes, inspect PVC/PV binding, StorageClass, topology, attachment state, access mode, CSI events, snapshots and reclaim policy. `Delete` reclaim behavior can remove the backing storage; do not delete and recreate a claim to clear a warning. Read [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) for the deployed driver and release behavior.

For distributed storage such as Ceph, distinguish serving availability from degraded redundancy and recovery progress. Inspect affected placement groups/objects, quorum, placement rules, full thresholds and recovery traffic. Do not lower replication/minimum-write requirements or mark data lost to clear health alarms without an explicit data-risk decision. See [Ceph placement-group troubleshooting](https://docs.ceph.com/en/latest/rados/troubleshooting/troubleshooting-pg/).

For corruption, stop destructive experimentation. Preserve logs and the original affected data, establish scope, protect a verified recovery copy, and involve the data owner. Filesystem repair, format, trim, snapshot revert, force detach and storage rebuild are not benign diagnostics. Verify writer fencing and consistency before attaching a volume elsewhere.

## Recover and verify

Make the smallest authorized change that addresses the evidenced boundary. Define rollback feasibility, propagated caches/TTLs, connection draining, storage resynchronization and data-risk limits. Verify from the original client location and representative peers, through normal DNS/TLS/identity paths. Confirm successful business operations, latency, error rates, durable writes, restored redundancy and expired-cache behavior. Keep the healthy comparator, evidence limitations and next owner in the incident record.
