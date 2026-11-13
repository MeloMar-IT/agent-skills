# Writing for stress

The reader is tired, scared and copy-pasting. Remove every decision that is not about the system.

## Steps
- One action per numbered step. "Check X and restart Y" is two steps.
- Observation steps come first and change nothing. Change steps come after, each alone.
- Branches are explicit: "If output shows A, go to step 5. If B, go to Escalate."

## Targets
- Every command carries its full target, copy-pasteable, with literal values taken from the service docs or alert labels.
- Do not use shell variables for context or namespace; a variable that is unset at 3 a.m. silently targets the wrong place.
- kubectl: `--context <ctx> -n <ns>` on each line. Never `config use-context` (it changes global state for the next command and for other terminals), never `--all`, `-A`, `--all-namespaces`.
- Other tools: aws `--profile --region`; gcloud `--project`; az `--subscription`; `psql -h <host> -d <db>`; `redis-cli -h <host> -p <port> -n <db>`.
- If a value is unknown, write a placeholder like `<ctx>` and say how to get it (for example "label `cluster` on the firing alert").

## Commands
- No `&&`, `;`, or `| xargs` into a state change. A pipe into `grep` or `jq` for reading is fine.
- Prefer the controller: `rollout restart deploy/<name>` over `delete pods`; `rollout undo deploy/<name>` to go back; `scale --replicas=<N>` with N recorded first.
- Record state before changing it (replica count, image tag, config version) in its own read-only step.
- Never write "check the logs". Write the exact command, for example `kubectl --context <ctx> -n <ns> logs deploy/<name> --since=15m --tail=200`.

## DANGER lines
Put `DANGER:` immediately before a state change: blast radius (what and who is affected) and how to undo.
Minimum list: delete, drain, cordon, scale, rollout restart/undo, apply, patch, edit, set image, helm upgrade/rollback, terraform apply, SQL UPDATE/DELETE/TRUNCATE/DROP, FLUSHALL/FLUSHDB, reboot/shutdown, failover. Any other state change also gets one by judgment. Read-only commands do not (`last reboot`, `grep shutdown`).

## After a change
- A bounded wait: `rollout status deploy/<name> --timeout=180s`, `wait --for=condition=Available deploy/<name> --timeout=180s`.
- Then the signal users see: a dashboard panel or query, window, and threshold.
- Say what to do on timeout (usually roll back).

## Expected output
After every command block: `Expected output:` with what good looks like, what bad looks like, and which step is next.

## Escalate
Time box ("after 15 minutes without recovery") and a team or role (`payments-oncall`), never a person. Say what to hand over: commands run, outputs, times.
