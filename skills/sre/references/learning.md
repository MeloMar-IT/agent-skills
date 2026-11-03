# Postmortems and systems investigation

## Contents

- [Prepare a blameless investigation](#prepare-a-blameless-investigation)
- [Reconstruct events and conditions](#reconstruct-events-and-conditions)
- [Apply Swiss cheese barrier analysis](#apply-swiss-cheese-barrier-analysis)
- [Use 5 Whys as a branching inquiry](#use-5-whys-as-a-branching-inquiry)
- [Select complementary methods](#select-complementary-methods)
- [Create and verify improvements](#create-and-verify-improvements)
- [Write and review the postmortem](#write-and-review-the-postmortem)
- [Sources](#sources)

## Prepare a blameless investigation

Use [soft-skills.md](soft-skills.md) for open interview questions, read-backs, facilitation, constructive disagreement, and evidence-based bias countermeasures. Separate the reliability question from speculation about a person's intentions or competence.

Start after immediate response is under control; preserve early memories and volatile evidence sooner when feasible. Set the learning question, scope, owner, contributors, privacy boundaries, and review date. Include near misses, repeated small failures, recovery difficulties, and surprising successes when they reveal important risks. Do not make the process a punishment for declaring an incident.

Separate learning from any formal misconduct or compliance process. Describe actions accurately without using character judgments as explanations. “An operator selected production” is an event to investigate; ask what the interface showed, why the selection was reasonable at the time, and what checks could limit the consequence. Do not automatically blame the operator, the organization, or the vendor instead.

Interview participants with their information available at that moment: what they saw, expected, attempted, feared, and had no visibility into. Preserve disagreement and incomplete memory. Avoid leading questions such as “Why did you ignore the obvious warning?” Record successful adaptations and barriers that held, as well as failure. Use evidence to test the account rather than rewriting the account to fit the outcome.

## Reconstruct events and conditions

Reuse the evidence ledger from `incidents.md`. Distinguish observed facts, participant reports, inferences, and unresolved questions. Separate impact onset, detection, acknowledgement, useful intervention, mitigation, full recovery, and data reconciliation. Keep original timestamps and clock uncertainty. Define interval endpoints before reporting detection or recovery metrics; do not merge distinct impact periods or hide continuing degradation.

Map the trigger, enabling conditions, propagation, detection gaps, recovery obstacles, and successful containment. Use a causal graph when interacting branches matter. Label edges with a mechanism and evidence, not only temporal order. Include the conditions under which the same action normally succeeds. Do not require one final “root cause”; where a local template requires that heading, describe the supported causal mechanisms and contributing conditions with their limits.

Ask counterfactual questions as hypotheses: if a barrier had worked, what specific harm would it have prevented, and what evidence supports that prediction? A plausible counterfactual does not prove causation. Keep explanations tied to the system as it existed, including constraints on budget, tools, staffing, architecture, and feedback.

## Apply Swiss cheese barrier analysis

Use the Swiss cheese model to inspect how intended defenses failed to prevent or contain harm. Treat it as a structured conversation about barriers, not a quantitative reliability model. Do not multiply assumed independent failure probabilities or infer that adding more checks necessarily creates independent protection.

1. Define the hazardous state and actual loss in user or business terms.
2. List the intended preventive, detective, containment, and recovery barriers.
3. Establish how each barrier was designed to work and whether it was present, bypassed, ineffective, overloaded, or never applicable.
4. Connect each gap to evidence and underlying conditions. Distinguish a barrier that failed from one merely imagined after the incident.
5. Identify shared dependencies, correlated assumptions, and changes that weakened several barriers together.
6. Propose changes that close a demonstrated gap or limit harm; define how their effectiveness will be checked.

| Barrier | Intended protection | Observed behavior / evidence | Underlying condition | Dependency or shared assumption | Improvement and proof |
| --- | --- | --- | --- | --- | --- |
| Named safeguard | Specific hazard stopped or detected | Fact and evidence ID | Mechanism, not blame | Correlated failure opportunity | Owner, check, success condition |

**Illustrative invented example: certificate expiry causes checkout failure.** This example is not an incident finding; replace every row with actual evidence before using it operationally.

| Barrier | Hypothetical gap | Investigation question |
| --- | --- | --- |
| Certificate inventory | An internal TLS hop is absent | Which discovery scope excluded it, and why? |
| Automated renewal | Renewal fails after an identity change | Which audit and renewal results demonstrate this? |
| Expiry alert | Alert watches only the public endpoint | Did it cover the certificate actually used by checkout? |
| Redundancy | All replicas share the expiring certificate | What common dependency defeats independent availability? |
| Recovery runbook | Instructions update the edge certificate only | Which path and validation steps are missing? |

Check for related services sharing the same inventory or renewal identity. Consider independently observing the internal handshake and verifying renewal end to end. Do not settle for “someone should remember the certificate.” Preserve any safeguards that reduced the actual impact.

## Use 5 Whys as a branching inquiry

Use repeated “why” or “what made this possible?” questions for a bounded mechanism. Five is a prompt to investigate further, not a mandatory chain length or proof of completeness. Branch whenever more than one supported condition contributes. Examine both occurrence and escape: why the failure happened, why it reached users, and why recovery was difficult.

For each link, record the claim, evidence, competing explanations, and next discriminating question. Stop a branch when the evidence ends, the scope boundary is reached, or a useful controllable mechanism is sufficiently understood. Mark the gap and how to investigate it; never manufacture an answer to reach five. Stop circular wording and question unsupported labels such as “insufficient training,” “bad process,” or “human error.”

For the invented certificate example, one branch might examine renewal identity authorization, another inventory coverage, another observability, and another shared-certificate placement. Each branch requires its own evidence. Choosing only the most convenient branch would obscure interacting conditions. Prefer a causal graph or CAST when feedback loops and control decisions cannot be represented fairly as a chain.

## Select complementary methods

| Method | Use it for | Required care |
| --- | --- | --- |
| Timeline and causal graph | Reconstructing evidence, interactions, and recovery | Mark uncertainty; sequence alone is not causation |
| Barrier / Swiss cheese analysis | Prevention, detection, containment, recovery gaps | Check shared dependencies; do not count layers as reliability |
| 5 Whys | Exploring a bounded mechanism with available evidence | Branch and stop honestly; avoid hindsight and blame |
| Fault tree | Reasoning backward from a clearly defined undesirable event using AND/OR relationships | Check completeness and dependence; no invented probabilities |
| FMEA / FMECA | Reviewing component or process failure modes before a change | Include interfaces; justify severity and detectability rather than trusting a composite score |
| STPA | Discovering hazards in control actions, timing, feedback, and interactions before loss | Define losses, hazards, constraints, and control structure with domain owners |
| CAST | Investigating an actual event through system control and feedback | Examine why controls were inadequate in context, including management and coordination |

For STPA, identify unacceptable losses and system hazards, model controllers and feedback, and examine unsafe control actions: needed action absent, harmful action provided, wrong timing/order, or incorrect duration. Develop causal scenarios and enforceable constraints; verify them through design review and targeted tests. For CAST, use the actual incident to examine the control structure, local process models, missing feedback, conflicting responsibilities, and conditions that allowed unsafe behavior. Engage a competent facilitator for consequential formal analyses; do not claim that a short AI-generated table is a complete safety assessment.

## Create and verify improvements

Prioritize a small set of actions by plausible risk reduction, reach, effort, and new operational burden. Prefer removing a hazardous state, reducing blast radius, or making the safe path easier over adding routine manual approvals to every operation. Use training where a demonstrated knowledge gap matters, paired with interface or system improvements where feasible. Do not treat more monitoring as a complete prevention strategy.

Each action needs a linked finding, owner or proposed owner, due/review date, tracking reference, expected behavior, acceptance evidence, and an effectiveness review. Distinguish implementation completion from risk reduction. For example, “alert added” is weaker evidence than a scoped exercise demonstrating detection, routing, response, and useful lead time. Assess whether a new safeguard adds a common dependency or produces enough noise to be ignored.

Record accepted residual risks and the actual decision owner. Revisit overdue actions and patterns across incidents: recurring dependencies, ineffective defenses, long diagnosis gaps, or fragile recoveries. Avoid ranking people by incident count or attributing improved reliability solely to a lower count when traffic, reporting, or service boundaries changed.

## Write and review the postmortem

Produce: executive impact summary; system context; evidence-backed timeline; causal mechanisms and contributing conditions; barrier analysis; response and recovery assessment; what worked; uncertainty; prioritized actions; and source/evidence references. Keep the summary intelligible to people outside the service team. Use quantifiable impact with honest estimates and denominators; state unavailable data.

Review with participants for factual accuracy and with adjacent teams for missing dependencies. Check that every strong causal assertion has evidence, every action addresses a finding, and disagreements remain visible where unresolved. Draft any announcement for the intended audience; publish or send only with explicit authorization and the appropriate privacy scope. Schedule follow-up only when requested or already authorized. Use the learning to improve runbooks, design, tests, onboarding, and exercise scenarios.

## Sources

- [Google SRE Workbook: Postmortem Culture](https://sre.google/workbook/postmortem-culture/) — factual, actionable, blameless learning.
- [James Reason: Human error—models and management, BMJ 2000](https://www.bmj.com/content/320/7237/768) — original systems and barrier model; DOI `10.1136/bmj.320.7237.768`.
- [Lean Enterprise Institute: 5 Whys](https://www.lean.org/lexicon-terms/5-whys/) — repeated questioning; five is not a required count.
- [Google SRE: STAMP, STPA, and CAST](https://sre.google/resources/practices-and-processes/stpa/) — prospective versus retrospective systems analysis.
- [Google SRE: Teaching STPA](https://sre.google/stpa/teaching/) — applying the method to software systems.

The evidence tables, invented certificate example, and operational workflow are original synthesis. The methods complement investigation; none guarantees a complete explanation.
