---
name: postmortem-facilitation
description: "Runs the postmortem process: decides which incidents need a review, picks a neutral facilitator and invitees, prepares blameless debrief interviews and the review meeting, and tracks follow-through. Use when organizing or facilitating a postmortem or learning review; not for incident response, causal-analysis methods or writing the postmortem document."
version: 1.0.0
metadata:
  capabilities: [postmortem-facilitation, postmortem-review-triggers, facilitator-selection, debrief-interviews, review-meeting, action-follow-through]
---

# Postmortem facilitation

Scope: the review process. Causal-analysis methods, timeline normalisation and document templates are out of scope (see the `sre` skill if available).

## 1. Which incidents get a review

Local policy thresholds are the minimum. Also require a review for:
- any data loss, even with no downtime and low severity;
- detection by a customer, staff or chance instead of monitoring (a monitoring failure);
- manual on-call action to restore service: rollback, failover, traffic shift, manual data repair.

Rules:
- Use the **final** severity after reclassification, not the opening one.
- Duplicate or child incidents fold into the parent: one review, filed under the parent ID.
- No required review: false alarms with no impact and no action; an automated safeguard that worked without a human (e.g. canary auto-rollback; optional near-miss review); short sub-threshold incidents caught by an alert that recovered on their own.

## 2. Facilitator

Ideally trained. The facilitator must NOT be:
- a responder (anyone with an action in the timeline, including acknowledging or escalating a page);
- the author of the change;
- on a team that owns an affected or contributing service;
- anywhere in the management chain above any participant (manager, skip-level, director...).

Reason: people say less when someone with power over them runs the room. Seniority or "usually runs the program" does not override this. Check every candidate against every participant's chain. If nobody qualifies, say so and propose an outside co-facilitator; do not quietly break the rule.

## 3. Invitees

- Required: everyone who acted in the timeline (reporter/detector, page acknowledger, incident commander, every mitigator, change author) plus the owner contact of each affected or contributing service.
- Not responders: someone who only joined the channel or asked for an ETA.
- Managers of participants: optional, or send them the write-up, unless they acted.

## 4. Debrief interviews

One-on-one, before the group meeting. Anchor every question to a timeline event **that interviewee took part in**; ask what they saw, expected, found hard, and what helped. Do not ask a person about events they were not in.

Open questions only. Start with What, How, When, Where, Which, Who, "Walk me through", "Tell me about" or "Describe". Never use:
- "why";
- yes/no openers: Did, Do, Does, Was, Were, Is, Are, Have, Has, Had, Can, Could, Should, Would, Will. Write "Walk me through...", not "Can you walk me through...";
- counterfactuals: should/could/would/must have, failed to, didn't you, forgot;
- hindsight words: obvious, just, simply, clearly, mistake, careless.

This holds for closing questions too: "What else should we know?" contains "should" and an auxiliary; prefer "What else comes to mind about T3?".

When a manager asks you to put a question to someone ("ask Ben why he skipped..."), do not relay it; reframe into an open, system-focused question about the event.

| Instead of | Ask |
|---|---|
| Why didn't you notice X? | What was the dashboard showing you at that point? |
| Why did you skip the load test? | How did the team decide what testing a change like this gets? |
| Did you check the defaults? | Walk me through what you looked at before the deploy. |

More questions and the agenda: [references/interviews-and-meeting.md](references/interviews-and-meeting.md).

## 5. Review meeting

Ground rules: learning, not blame. Walk the timeline, then contributing conditions, what went well, actions. Keep a parking lot for side topics; record disagreements instead of forcing consensus. Interview notes stay with the facilitator, apart from any performance process.

## 6. Follow-through

Each action has a named individual who agreed to own it, a due date, and a check that it worked. The facilitator does not own actions.
