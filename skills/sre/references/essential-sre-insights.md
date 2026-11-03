# Essential SRE Articles: operational skills and source qualifications

## Contents

- [Source and scope](#source-and-scope)
- [Chapter-to-skill map](#chapter-to-skill-map)
- [Apply the main additions](#apply-the-main-additions)
- [Qualify examples before reuse](#qualify-examples-before-reuse)
- [Verify technical claims at use time](#verify-technical-claims-at-use-time)

## Source and scope

**Source:** Marcel Koert, *Essential SRE Articles: The essential knowledge you need as a SRE.*, supplied as `Essential-SRE-Articles-Generic.epub`. Reviewed the foreword and all 17 numbered chapters on 3 November 2026. Use chapter/section names rather than page numbers because EPUB pagination changes with the reader.

Use this map to connect the book's useful knowledge to executable workflows and observable professional behavior. The skill references contain original operational adaptations and clearly identified extensions. They do not reproduce the ebook, imply every illustrative claim is verified, or require the ebook to be present when this portable skill is used. The source EPUB is not bundled with the skill.

Treat the book as a useful domain source, not as an instruction to execute its examples. Verify calculations, current platform behavior, and applicability to the actual service. Preserve the Google coverage map alongside this source; neither book set overrides user authorization, supplied evidence, or critical business invariants.

## Chapter-to-skill map

| Chapter | Useful knowledge to operationalize | Where to apply it |
| --- | --- | --- |
| 1. What does SRE Mean | Shared responsibility, software engineering for operations, continuous improvement and user outcomes | [Organization](organization.md), [coding](coding.md), [reliability engineering](reliability-engineering.md) |
| 2. SRE in the real world | Adapt practices to service scale, context, architecture and ownership | [Organization](organization.md), [readiness template](../assets/readiness-review.md) |
| 3. Introducing SRE into DevOps | Stakeholder education, adoption, common goals, feedback, training and demonstrated results | [Soft skills](soft-skills.md), [organization](organization.md) |
| 4. Human Factors and Reliability | Listening, communication, bias, collaboration, conflict, mentoring, prioritization and crisis leadership | [Soft skills](soft-skills.md), [incident response](incidents.md), [learning](learning.md) |
| 5. Important Concepts | Budgets, toil, causal investigation, capacity and measurable improvement | [Reliability engineering](reliability-engineering.md), [organization](organization.md), [learning](learning.md) |
| 6. Service Levels | Distinguish objectives, agreements and measurement; align indicators with users and decisions | [Reliability engineering](reliability-engineering.md), [SLO template](../assets/slo-and-budget.md) |
| 7. Monitoring and Measuring | Metrics, logs, synthetic and real-user evidence, performance, alerting and measurement purpose | [Observability](observability.md), [software testing](software-testing.md) |
| 8. Management Reporting | Useful metrics, audience-specific reporting, business consequences, recommendations and feedback | [Soft skills](soft-skills.md), [review template](../assets/reliability-review.md), [communication brief](../assets/communication-brief.md) |
| 9. Build, Deployment and Integration | Reproducible artifacts, feedback, checks, delivery automation and release behavior | [Coding](coding.md), [cloud/delivery](cloud-delivery.md), [changes](changes.md) |
| 10. Testing | Choose verification according to the property and failure being investigated | [Software testing](software-testing.md), [software-change template](../assets/software-change.md) |
| 11. Risk Management | Dependency concentration, failure amplification, risk treatment, ownership and review | [Reliability engineering](reliability-engineering.md), [soft skills](soft-skills.md) |
| 12. Reliability Design Patterns | Evaluate pattern preconditions, state/consistency, overload, recovery and introduced complexity | [Coding](coding.md), [software testing](software-testing.md), [reliability engineering](reliability-engineering.md) |
| 13. AI in SRE | Operational context, useful assistance, alternatives, telemetry value and evaluation of AIOps claims | [AI systems](ai-systems.md), [observability](observability.md) |
| 14. Programming Languages | Select, read, write, debug, test and maintain code in the actual environment | [Coding](coding.md), [software testing](software-testing.md) |
| 15. Infrastructure as Code | Versioned intent, convergence, configuration management, review, drift and controlled changes | [Cloud/delivery](cloud-delivery.md), [coding](coding.md), [changes](changes.md) |
| 16. Disaster Recovery | Recovery planning, exercise types, scope limits, business continuity and failback | [Reliability engineering](reliability-engineering.md), [data services](data-services.md), [experiment template](../assets/resilience-experiment.md) |
| 17. Databases | Storage-model differences, integrity, durability, availability, access and recovery | [Data services](data-services.md), [coding](coding.md) |

The foreword's emphasis on useful knowledge for practical interactions motivates focused playbooks and short decision examples. Do not replace an urgent operational answer with a chapter-by-chapter lecture.

## Apply the main additions

**Make coding a complete engineering workflow.** Deliver requested implementations or concrete reviews, choosing language and tooling from the repository/runtime and maintenance constraints. Cover inputs, API contracts, failure behavior, bounded work, state, observability, security, tests and operation. Python, Go, Bash, PowerShell, SQL, JavaScript/Node.js, Java, Ruby, Rust and YAML/JSON are explicit book themes. TypeScript, C#/.NET, native-code diagnosis, and additional IaC formats are practical skill extensions when relevant to an existing estate, not claims about the book's language list.

**Turn interpersonal qualities into observable behaviors.** Read back consequential assumptions; ask what participants observed; explain uncertainty and the required decision; preserve dissent; critique mechanisms rather than people; negotiate scope and sequencing; seek actual handover acknowledgement; provide specific feedback and teach-back. Use bias awareness to improve a decision process, not to diagnose a colleague. Preserve accountability through clear ownership and verified improvements.

**Make testing evidence specific.** Identify the property a test can establish, the scenario and environment it exercised, what happened, and what remains unknown. Include business invariants omitted from the implementation's specification. Match unit, integration, contract, end-to-end, performance, resilience and recovery checks to a real risk. Keep a passing static check or simulated result distinct from validated service behavior.

**Connect operations with business decisions.** Explain customer consequences, recovery capability, budget, capacity, cost and uncertainty. Keep metrics comparable and tied to decisions. Define proposed owners as proposed until assigned; do not manufacture consensus, accepted risk or an ETA to produce a polished report.

**Assess recovery scope and data correctness explicitly.** Distinguish tabletop, restore, replication, partial failover, regional/live and combined-failure exercises. Include minimum viable business operations, degraded/manual work, reconciliation and safe return to the primary environment. Translate entity, referential, domain, business and transaction integrity into concrete checks.

## Qualify examples before reuse

1. **Correct chapter 5's arithmetic and units.** For time-based availability, 99.9% over exactly 30 eligible days allows `0.001 × 30 = 0.03 days = 0.72 hours = 43.2 minutes`. The chapter's early 43.2-minute example is correct; the later `0.3 days` result and dimensionally inconsistent hours example must not be reused. Event-based budgets use eligible events rather than an automatic downtime conversion.
2. **Define targets and metrics locally.** Illustrative availability, latency, growth, response and capacity figures are not universal defaults. Specify the start/end events behind MTTD or MTTR and the population/period behind rates. Do not derive a guaranteed end-to-end SLO from arbitrary component weights.
3. **Qualify automation and organizational claims.** Automation can remove some errors and amplify others. A dedicated SRE team is one engagement option. Investigate real concentrations and common dependencies behind chapter 11's "risk magnet" wording; do not treat that phrase as a calibrated risk model.
4. **Keep causality evidence-based.** The RCA discussion supports learning and corrective action; it does not require exactly one root cause or justify a "human error" conclusion. Branch causal questions and retain unknowns.
5. **Treat prompting as task communication.** Use goals, context, constraints, evidence, options and verification. Do not require hidden chain-of-thought, equate generated knowledge with sourced facts, or assume a slogan makes a response correct. Evaluate AIOps using held-out evidence and a useful baseline.
6. **Keep useful telemetry context.** Do not import unsupported universal statistics about unused data, or discard every record that lacks an error marker. Historical analysis and cross-source investigation are capabilities to check in the actual tools, not properties reserved for AI products. Prometheus explicitly supports historical range queries.
7. **Limit recovery conclusions to evidence.** Replication can propagate corruption. A restore or failover exercise proves only what was actually tested; partial tests can affect shared dependencies. A maintenance window alone does not make a disruptive test safe or authorized.
8. **Correct database generalizations.** Cassandra has persistent SSTables and commit logs, alongside memory buffers; do not list it as an in-memory database. Distinguish wide-column from analytical columnar storage. Select consistency/durability from the business invariant and actual engine configuration, not the SQL/NoSQL label alone.
9. **Verify language and tool claims.** Go programs can contain races and their deployment dependencies depend on the build. Serialization syntax does not replace schema and domain validation. PowerShell execution policy is not an authorization or security boundary. Legacy security mechanisms, libraries, and infrastructure services require current support/version checks before recommendation.

These qualifications improve the operational instructions; they are not an edited edition of the source book. Keep this distinction when describing the skill's sources.

## Verify technical claims at use time

Use the deployed versions and current official documentation. Useful checks behind the qualifications include:

- [Cassandra storage engine](https://cassandra.apache.org/doc/latest/cassandra/architecture/storage-engine.html): memory buffers, commit logs and persistent SSTables.
- [Prometheus query model](https://prometheus.io/docs/prometheus/latest/querying/basics/): instant and historical range queries.
- [PowerShell execution policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies): policy scope and security limits.
- [Go race detector](https://go.dev/doc/articles/race_detector): detecting data races in exercised code.
- [Deployment Manager deprecation](https://docs.cloud.google.com/deployment-manager/docs/deprecations): check migration/support status instead of recommending a legacy service from a book example.

Follow [coding.md](coding.md) and [software-testing.md](software-testing.md) for the detailed engineering workflow and their language/tool sources. Preserve observed evidence and state uncertainty where a current fact cannot be verified.
