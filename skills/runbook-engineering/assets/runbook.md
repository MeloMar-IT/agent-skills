---
title: "UNKNOWN: symptom or task this runbook covers"
owner: team-UNKNOWN
severity: page
alerts: [AlertName]
last_reviewed: YYYY-MM-DD
status: draft
review_interval_days: 90
---

# Symptom or task

## When to use
- Alert or symptom (exact alert names):
- Does not cover (link the right runbook):

## Impact
- Who or what is affected, and how to confirm it:

## Before you start
- Access needed and how to get it:
- Target values (write the literal values): context, namespace, deployment, region:

## Diagnose
1. One observation, one command.

```bash
kubectl --context <ctx> -n <ns> get deploy <name>
```

Expected output: good looks like ...; bad looks like ...; go to step N.

## Mitigate
1. Record current state (read-only).

```bash
kubectl --context <ctx> -n <ns> get deploy <name> -o jsonpath="{.spec.replicas}"
```

Expected output: a number; write it down as the old replica count.

2. DANGER: blast radius ...; undo with ...

```bash
kubectl --context <ctx> -n <ns> rollout restart deploy/<name>
```

Expected output: `restarted`.

3. Wait for completion.

```bash
kubectl --context <ctx> -n <ns> rollout status deploy/<name> --timeout=180s
```

Expected output: `successfully rolled out`; on timeout go to Roll back.

## Verify
- User-visible signal (dashboard or query, time window, threshold):

## Roll back
1. Exact undo steps.

## Escalate
- After N minutes without recovery, page team or role `<team-oncall>`. Include what you ran, outputs and times.
