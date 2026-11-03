# Kubernetes and container platforms

Use this playbook after identifying the affected user journey and the incident time window. Treat a cluster symptom as a hypothesis about the service, not proof of the customer impact or cause.

## Contents

- Establish scope and gather bounded evidence
- Select the diagnostic branch
- Inspect shared platform components
- Handle platform variants and upgrades
- Recover and verify

## Establish scope and gather bounded evidence

Record the cloud account/project/subscription, cluster, region, environment, namespace, workload owner, image digest, rollout revision, and relevant server/client versions. Read the current context name, then put the verified context explicitly on every command. Do not change the operator's default context as a side effect of investigation. Discover installed APIs and CLI flags before relying on version-specific behavior.

Choose one affected workload and a healthy comparator. Bind the following variables to verified, nonempty values before running selected examples; do not execute the whole block as a universal collector. Confirm the selector resolves only to the intended workload. Keep queries narrow even when the caller has cluster-admin rights.

```bash
: "${SRE_CTX:?}" "${SRE_NS:?}" "${SRE_SELECTOR:?}"
kubectl --context "$SRE_CTX" -n "$SRE_NS" --request-timeout=10s \
  get pods -l "$SRE_SELECTOR" -o wide

: "${SRE_POD:?}" "${SRE_CONTAINER:?}"
kubectl --context "$SRE_CTX" -n "$SRE_NS" --request-timeout=10s \
  get pod "$SRE_POD" \
  -o jsonpath='{.status.phase}{"\n"}{.status.conditions}{"\n"}{.status.containerStatuses}{"\n"}'
kubectl --context "$SRE_CTX" -n "$SRE_NS" --request-timeout=10s \
  logs "$SRE_POD" -c "$SRE_CONTAINER" --since=15m --tail=200 \
  --limit-bytes=65536 --timestamps=true
```

Select `--previous` for the immediately preceding terminated container when it exists. Preserve pod UID, node, container identity, exit reason, restart count, event times, and collection time. Events are best-effort evidence with finite retention; an absent event does not demonstrate that something did not happen. Container logs may expose credentials or personal data; inspect and redact before quoting or attaching them. A 15-minute window is an example, not a reason to omit the actual failure interval. See the official [application troubleshooting](https://kubernetes.io/docs/tasks/debug/debug-application/) and [logs reference](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_logs/).

Query events by object identity and incident interval where supported. A scoped `describe` can help after reviewing its disclosure risk; full manifests can contain literal environment secrets, annotations, or sensitive arguments. Never begin with all-namespace YAML, Secret objects, raw kubeconfig, or a whole cluster dump. Record permission failures and use the correct owner; do not broaden privileges automatically.

## Select the diagnostic branch

| Symptom | Distinguishing evidence | Next decision and common trap |
| --- | --- | --- |
| Pending | Scheduling events; requested resources; node taints; affinity/topology; quota; PVC state | Separate capacity from placement, admission, and storage. Spare average CPU does not imply a schedulable node. |
| Image pull failure | Exact image digest/tag; registry status; pull-secret reference; node egress and trust | Check image existence, architecture, authentication, certificate trust, and rate limits. Do not print pull-secret values. |
| Restarting / CrashLoopBackOff | Last termination reason/code; previous logs; rollout/config timing; probes | CrashLoopBackOff describes retry behavior. Exit 137 alone does not prove a memory limit caused the kill. Correlate kernel/cgroup evidence. |
| Running but not ready | Probe result; application startup and dependency state; endpoints | Distinguish application failure from a bad probe or dependency gating. Running is not evidence of availability. |
| Timeouts / 5xx | Compare direct application, Service, ingress/gateway and client paths; affected versions/nodes/zones | Locate the failing hop before replacing pods. Separate upstream latency from proxy deadlines and retries. |
| High latency without errors | Queueing; CPU throttling; memory/GC; storage; dependency latency; connection pools | Compare latency distributions and load, not only CPU means. More replicas may overload the database. |
| StatefulSet / volume failure | PVC/PV binding; attachment; topology; CSI events; filesystem and backend | Respect volume ownership and fencing. Recreating a PVC can delete its backing storage. |
| HPA not scaling | HPA conditions; metrics availability; requests; target; min/max; stabilization; node capacity | Separate missing measurements from an inactive scaling rule. Check interactions with VPA and cluster autoscaling. |

For probes, identify startup, readiness, and liveness separately. A dependency-wide liveness check can restart healthy processes during a downstream outage. Consider startup duration and graceful termination; correlate endpoints, inflight requests, preStop behavior, and termination grace periods before changing them.

For service routing, inspect selected Service fields, selectors, EndpointSlices, port/targetPort, ready backends, ingress or Gateway API routes, load-balancer health, and certificate identity. Follow [Kubernetes service debugging](https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/) with the real namespace and cluster domain. Compare DNS name and an explicitly selected address while preserving TLS hostname/SNI. A successful request from a laptop does not establish reachability from the affected pod.

## Inspect shared platform components

Widen scope when multiple unrelated workloads share a failure boundary, documenting why broader access is necessary.

- **Nodes/runtime:** Correlate node Ready/pressure conditions, kubelet and container runtime errors, eviction, disk/inodes, PID limits, cgroup pressure, and host changes. Distinguish node pressure eviction from container OOM and application termination.
- **DNS:** Check response code, latency, search domains, resolver configuration, CoreDNS health and upstream reachability. Compare UDP and TCP only when the evidence suggests transport behavior; do not assume the domain is `cluster.local`.
- **CNI/network policy:** Compare same-node, cross-node, and cross-zone paths; policy selection; routes; MTU; SNAT/conntrack pressure; eBPF or kube-proxy state; cloud subnet/IP capacity. Confirm whether a policy engine actually enforces the policies present.
- **CSI/storage:** Correlate controller and node-side events, attachment limits, access modes, storage-zone constraints, IOPS/throughput ceilings, and backend health. Do not force detach a volume until the former writer is fenced.
- **Service mesh:** Separate application behavior from sidecar/gateway configuration, mTLS identity/expiry, discovery/control-plane convergence, outlier ejection, rate limits, and compounded retries.
- **Control plane:** Inspect API availability/latency, request throttling, authentication/RBAC failures, admission webhook latency/failure mode, controller progress and scheduler behavior. Existing traffic can continue despite an API outage; conversely, working API calls do not prove data-plane health. Start with the official [cluster troubleshooting guide](https://kubernetes.io/docs/tasks/debug/debug-cluster/).
- **etcd:** Establish membership/quorum, leader changes, disk latency, space alarms and the latest verified backup. Use the platform owner's procedure. A restore is a cluster recovery change with identity/revision implications, not an ordinary pod repair. Match the exact release's [recovery procedure](https://etcd.io/docs/v3.6/op-guide/recovery/); do not improvise member removal or force a new cluster.

`kubectl exec` executes code inside the workload; review its exact command and load. `kubectl debug`, ephemeral containers, diagnostic pods, port forwarding and node debug sessions create resources or privileged access paths. They are not passive observations. Define lifetime, cleanup, image provenance, credentials, disclosure and performance limits before using authorized access.

## Handle platform variants and upgrades

For AKS, GKE, and EKS, distinguish provider-owned control planes from customer-owned node pools, identity, networking and workloads. Review provider events and documented support boundaries. Investigate cloud API quota, subnet address exhaustion, workload identity/token changes, node image updates, disk limits and maintenance activity. Match the deployed release and mode; do not assume standard GKE and Autopilot, or all EKS/AKS node-management modes, expose identical controls. Start with [AKS reliability](https://learn.microsoft.com/en-us/azure/aks/best-practices-app-cluster-reliability), [GKE autoscaling](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/cluster-autoscaler), and [EKS troubleshooting](https://docs.aws.amazon.com/eks/latest/userguide/troubleshooting.html).

For OpenShift, inspect affected ClusterOperator conditions, machine config pools, operator reconciliation, Routes, security context constraints and cluster version transitions. Do not edit operator-managed resources blindly. `oc adm must-gather` runs collection workloads and produces a sensitive support bundle; authorize that specific scope and handle the result accordingly. Consult the deployed release's [collection guidance](https://docs.redhat.com/en/documentation/openshift_container_platform/4.14/html/support/gathering-cluster-data); this linked release is illustrative, not a recommended target version.

Before upgrades or drains, check skew compatibility, deprecated APIs, CRDs/webhooks, add-ons, node surge capacity, storage mobility, topology and recovery options. A PodDisruptionBudget constrains supported voluntary evictions; it does not guarantee availability through involuntary failures or govern workload rolling-update strategy. Check replica distribution and workload rollout settings separately. See [disruptions](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/).

## Recover and verify

Choose a minimal authorized intervention with a defined target, impact limit, rollback or forward-recovery path, and observation period. Avoid simultaneous restarts or a whole-cluster rollout that destroys evidence and widens impact. For stateful services, preserve membership and data integrity before restoring write traffic.

Verify the customer journey and SLI, error and latency distributions, backlog age, data correctness, stable restart counts, ready endpoints, deployment convergence, and node/zone redundancy. Observe under representative load, not just one successful health check. Reconcile emergency changes into the desired configuration, remove diagnostic access/resources, restore paused automation when appropriate, and record the remaining risk and owner.
