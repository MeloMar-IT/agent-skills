# Examples

## Time zone conversions
- US DST starts 2026-03-08. 02:30 New York that day does not exist (07:30Z or 06:30Z); 03:30 EDT = 07:30Z.
- Mon 03:00 Tokyo (UTC+9) = Sun 18:00Z.
- EU DST ends 2026-10-25: Berlin 02:xx happens twice (00:xxZ on CEST, then 01:xxZ on CET).
- On 24 Oct US Eastern is still EDT: 8:30 PM EDT = 00:30Z on 25 Oct.
- Amsterdam on 13 Nov is CET (UTC+1): 02:00 = 01:00Z.
- Amsterdam on 24 Oct is still CEST (UTC+2): 02:30 = 00:30Z.

Scheduler note: a job scheduled in a local zone fires at that zone's wall clock; convert the first post-fix start to UTC for that date, then add the run length.

## Declaration (illustrative, invented policy: SEV1 = login down for 20%+ or data exposed; SEV2 = 5-20%; SEV1 cadence 20 min)
Severity: SEV1 (provisional) — 12% of logins fail, but an unverified report of exposed data matches SEV1; confirm with the access log.
IC: Rosa Meyer
Ops lead: Jin Cho
Comms lead: Rosa Meyer (held by IC)
Scribe: Rosa Meyer (held by IC)
Next update: 14:35Z (declared 14:15Z + 20 min)

## Handoff note (invented)
Current IC: Lena Ott (Max Roy said "yours" but has not acknowledged in the channel).
Handoff: pending
Next step: recall Lena or page the secondary IC before the 08:45Z status update.
Open actions: only unfinished ones, e.g. ACT-5 (owner, state). Finished ones go to the timeline.
Hypotheses: every one with status, rejected ones kept. Mitigations in effect: list them.
Commitments: each promised update with its UTC time.

## Closure decision (invented)
State: monitoring. Fix deployed but the weekly export has not run since. Remove the alert silence before the run; review when the first post-fix run ends (start converted to UTC + run length). Each temporary mitigation becomes a follow-up with owner, due time and removal condition.
