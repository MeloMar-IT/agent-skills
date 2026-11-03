# Human judgment, communication, and collaboration

## Contents

- [Build a shared understanding](#build-a-shared-understanding)
- [Counter decision bias with evidence](#counter-decision-bias-with-evidence)
- [Coordinate calmly under pressure](#coordinate-calmly-under-pressure)
- [Communicate for the audience](#communicate-for-the-audience)
- [Resolve disagreement and negotiate priorities](#resolve-disagreement-and-negotiate-priorities)
- [Facilitate learning and accountability](#facilitate-learning-and-accountability)
- [Coach and transfer knowledge](#coach-and-transfer-knowledge)
- [Protect sustainable working conditions](#protect-sustainable-working-conditions)
- [Check completion and source scope](#check-completion-and-source-scope)

Apply these behaviors during technical work, rather than adding a generic interpersonal checklist afterward. Use [incidents.md](incidents.md) for incident command, [learning.md](learning.md) for investigation, and [organization.md](organization.md) for ownership and staffing. Adapt depth to urgency. Preserve existing user authorization; draft communications unless sending to verified recipients is explicitly authorized.

## Build a shared understanding

Establish the decision, affected users, constraints, and each participant's relevant information. Read available evidence before asking questions. Distinguish what someone observed from their interpretation and desired outcome. Ask a focused open question, listen to the answer, and resolve consequential ambiguity before proceeding.

Use a brief read-back: “My understanding is that checkout completes slowly, while payment authorization still succeeds. Is that distinction accurate?” Invite correction without asking the user to repeat already clear context. Use “What did you observe?” before “What caused it?” Ask which source, interval, environment, and user group support the report.

Recognize stated concerns and practical consequences without inventing feelings or motives. “Customers cannot complete orders, so the immediate priority is restoring that path” is grounded. Do not claim that a colleague is anxious, careless, resistant, or incompetent from a ticket or terse message. Clarify language differences, acronyms, and ambiguous terms; use written summaries when accents, time zones, or communication preferences make live discussion difficult.

Keep facts, assumptions, open questions, decisions, and assigned actions distinguishable. Check understanding of a consequential instruction through a concise acknowledgement/read-back when appropriate. Do not turn routine reads or already authorized actions into repeated approval requests. [Book basis: chapters 3–4.]

## Counter decision bias with evidence

Treat bias labels as prompts to improve the decision process, not diagnoses of people. An explanation needs evidence even when everyone agrees with it. Apply one or two useful checks when time is limited:

| Risk in the decision | Observable countermeasure |
| --- | --- |
| Confirmation | Record a disconfirming observation and seek it; retain contrary evidence in the hypothesis register. |
| Anchoring | Reconstruct the first trustworthy symptom independently of the first proposed cause; compare at least one credible alternative. |
| Availability | Compare the memorable incident with the current mechanism and relevant historical denominator; do not assume recurrence from resemblance. |
| Optimism or planning fallacy | Examine a plausible failure scenario, dependencies, recovery time, and evidence of rollback feasibility; state an estimate range where justified. |
| Overconfidence | Separate tested behavior from experience-based expectation; state what is unknown and what result would change the recommendation. |
| Group pressure or authority | Invite evidence-based dissent before a consequential decision; distinguish a decision owner's authority from proof that their diagnosis is correct. |
| Hindsight or outcome bias | Reconstruct information available at the time; assess the decision process separately from whether the outcome happened to be good or bad. |

Where useful, obtain independent initial assessments before sharing a preferred answer. Ask a second reviewer to inspect source evidence and invariants, rather than merely endorse the first explanation. Independence is weakened when all reviewers inherit the same unsupported assumptions.

Time-box investigation around the decision's urgency. Critical thinking should improve recovery, not delay a justified mitigation until every alternative is eliminated. Provide a concise rationale and evidence, not hidden model reasoning or unsupported numerical confidence. [Book basis: chapter 4; hindsight checks are an operational extension.]

## Coordinate calmly under pressure

Lead with the current impact, the immediate objective, and the next decision. Use neutral language, short updates, and explicit workstreams. Avoid theatrical urgency, blame, unexplained jargon, or a long speculative diagnosis during active harm.

Respect the established incident lead and decision rights. If roles are absent, propose coordination, operational, investigation, and communication responsibilities; do not invent assignments or assume command authority. Coordinate changes to a shared dependency through one action owner to avoid conflicting interventions.

For a consequential action, state target, expected effect, stop condition, and verification owner. Close the loop with the actual result; silence is not acknowledgement or success. Preserve a concise decision record so an incoming responder can understand what changed and why.

If discussion becomes circular, summarize agreement and the unresolved question: “We agree the latency began before the restart. We disagree on the database mechanism. This scoped wait-event check can distinguish the two explanations.” Escalate a time-critical decision through the existing authority when needed; do not require unanimous agreement or suppress documented dissent.

Offer the next update time when a repair estimate is unsupported. Acknowledge uncertainty plainly while showing the next useful action. [Book basis: chapter 4; operational detail complements incidents.md.]

## Communicate for the audience

Choose content by the recipient's decision and legitimate need to know. Preserve the same underlying facts across versions; simplify the language without concealing material uncertainty or impact.

| Audience | Lead with | Retain or provide separately |
| --- | --- | --- |
| Responders | Affected journey, evidence, exact scope, current action and next check | Queries, versions, timelines, rejected hypotheses, recovery conditions |
| Service/product leaders | Customer impact, tradeoffs, decision required and available options | Capacity, budget, dependencies, effort range and accountable risk owner |
| Executives | Consequence, trend, recovery progress and decisions needed | Clearly defined metrics, evidence limits and financial assumptions |
| Customers/support | Experienced symptoms, affected scope, useful workaround if verified, next update | Approved detail; no secrets, internal speculation, or unjustified reassurance |
| Vendors/other teams | Reproducible symptom, exact supported versions, scoped evidence and requested help | Sanitized artifacts, boundary ownership and escalation route |

Use a compact pattern: **impact → evidence/status → action/result → uncertainty → next update or decision**. An illustrative draft is: “Some customers cannot complete checkout. We have isolated failures to one request path and are validating a mitigation. Recovery time is not yet confirmed. The next update is at [time].” Replace every bracket and claim with actual information before sending.

For management reporting, define periods, populations, severity, and metric endpoints. Separate measured loss from estimates; explain denominators, missing data and changes in workload. Use trends and distributions when a mean hides repeated harm. Report action effectiveness, customer outcomes and recovered engineering capacity, not only closed tickets or postmortem completion. Never manufacture monetary impact or compare teams without comparable context. [Book basis: chapter 8.]

## Resolve disagreement and negotiate priorities

Separate observations, interpretations, interests, constraints, and proposed actions. State the other position fairly before challenging it. Ask what evidence or acceptance criterion would resolve the difference. Critique a proposal's mechanism and consequence rather than its author's character.

Use observation–impact–request: “The proposed restore excludes orders accepted after the snapshot. Those orders may be lost. Please provide the replay and reconciliation evidence, or choose a recovery path that preserves them.” Treat this as example wording, not a finding about the current service.

Negotiate scope, sequencing, staffing, deadlines, and reversible exposure. Make options concrete, including doing nothing and its consequences when useful. Preserve nonnegotiable correctness, security, and contractual constraints; a compromise must not silently discard them. Apply an authorized emergency process when appropriate rather than treating urgency as unlimited permission.

Translate reliability work into affected journeys, plausible loss, recovery burden, delivery effects, and uncertainty. Identify who can accept residual business risk; technical seniority alone does not supply that authority. Record the decision, evidence, owner, and reconsideration trigger. Respect an informed authorized decision while keeping material dissent and evidence visible.

Influence without formal authority by agreeing on a shared outcome, demonstrating a bounded improvement, inviting affected teams to shape the change, and measuring its effect. Avoid tool evangelism or implying one organizational model suits every team. [Book basis: chapters 1–4, 8 and 11.]

## Facilitate learning and accountability

Ask neutral retrospective questions: “What could you see then?”, “What did you expect this action to do?”, “Which alternatives were available?”, and “What made recovery easier or harder?” Keep reports and inferences separate, preserve disagreement, and let participants correct factual summaries.

Examine interfaces, feedback, documentation, incentives, workload, staffing, access, and coordination alongside technical behavior. Determine how the procedure works in practice and why adaptations occur. Do not substitute “bad culture” for “human error” as an unsupported final cause. Record successful adaptations as well as weaknesses.

Make it practical to report uncertainty, near misses, and concerns without ridicule or pressure to agree. A facilitator can invite quieter contributors and offer asynchronous input; do not presume silence means agreement. Keep formal misconduct processes separate from learning reviews and preserve privacy.

Retain accountability through explicit responsibilities and verifiable improvements. Use a named owner only when actually assigned; otherwise propose a role and mark it unassigned. Check whether completed actions changed the relevant failure condition. Do not force participants to confess blame or reward a lower incident count created by reduced reporting. [Book basis: chapters 3–4.]

## Coach and transfer knowledge

Identify the learner's task, prior knowledge, and access before choosing depth. Demonstrate a small diagnostic or engineering decision, explain its evidence and tradeoffs, then invite the learner to perform a bounded task and explain their conclusion. Give specific feedback on observable work and its consequence; avoid personality judgments.

Use teach-back to expose ambiguity: “Which observation would make you stop this rollout, and what would you check before rollback?” Separate developmental exercises from live incident ownership. Keep experienced support available and use appropriate environments and authorization for practice.

Turn recurring explanations into short runbooks, decision examples, or paired exercises with a verified owner and review date. Include failed hypotheses and lessons about uncertainty, not only successful commands. Check capability through demonstrated diagnosis, safe action selection, escalation, and handover rather than attendance, certification, or confidence alone. [Book basis: foreword and chapters 3–4.]

## Protect sustainable working conditions

Prioritize by harm, urgency, dependencies, and available capacity. Make tradeoffs explicit when incident response displaces planned work. Reduce simultaneous demands, use clear intake and handovers, and escalate a coverage gap before it becomes an implicit promise of unlimited availability.

When a responder reports fatigue or prolonged duty, offer a practical handover or relief request. Do not diagnose stress, burnout, or health conditions, and do not treat composure or personal resilience as a substitute for adequate staffing and usable systems. Record unfinished work, access constraints, next checks, and acknowledged ownership during transfer.

Protect confidential incident and personnel information. Be candid about access and competence limits, request the relevant specialist when needed, and preserve the user's decision rights. Evaluate adaptations using system constraints and evidence rather than stereotypes about personality, age, culture, or job title. [Book basis: chapter 4; sustainable staffing details are an extension.]

## Check completion and source scope

Confirm that the relevant participants can identify the current impact, known facts, disputed questions, decision owner, next action, and verification condition. For a handover, confirm the receiving owner and unresolved risks. For learning or mentoring, seek evidence of improved capability or a changed safeguard. Do not claim these outcomes merely because a message was drafted or a meeting occurred.

**Source reviewed:** Marcel Koert, *Essential SRE Articles: The essential knowledge you need as a SRE.*, supplied EPUB; foreword and chapters 1–4, 8 and 11. Chapter 4 supplies the explicit human-factors, bias and interpersonal themes; chapters 3 and 8 inform adoption and stakeholder communication. These procedures and examples are original operational adaptations, not quoted book text. The EPUB is not required to use this reference.

Qualify broad book claims: automation changes failure modes rather than eliminating human error; a dedicated SRE team is one organizational option; bias names do not diagnose individuals; and chapter 11's “risk magnet” is treated as a prompt to examine evidenced concentration and common dependencies, not as a calibrated probability model.
