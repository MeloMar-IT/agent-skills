# Google SRE coverage and source map

## Contents

- [Scope and evidence](#scope-and-evidence)
- [Original SRE book](#original-sre-book)
- [SRE workbook](#sre-workbook)
- [Secure and reliable systems](#secure-and-reliable-systems)
- [Second edition: public topic map](#second-edition-public-topic-map)
- [Investigation methodology sources](#investigation-methodology-sources)
- [Apply the sources](#apply-the-sources)

## Scope and evidence

Use this reference to find the skill workflow corresponding to a book subject. All numbered chapters are accounted for below; front matter and indexes introduce no separate operational workflow. Labels are paraphrased. The mappings are this skill's implementation choices, not Google endorsements.

Sources checked **2026-11-03**. The original book, workbook and security/reliability book have openly readable text. Their tables of contents and selected relevant chapters were inspected when this skill was authored; this package does not reproduce the books or claim to encode every passage. The second edition is mapped from its publicly accessible publisher contents and overview; full-text access was not available. Consult the linked source for nuance and verify current product documentation before using operational commands.

## Original SRE book

**Source:** *Site Reliability Engineering* (first edition, 2016), [official contents](https://sre.google/sre-book/table-of-contents/). Access: public online text.

| Chapters | Subject coverage | Skill references |
| --- | --- | --- |
| 1–2 | Role, lifecycle and production context | organization.md; reliability-engineering.md; kubernetes.md; linux-vms-windows.md |
| 3–4 | Reliability risk, objectives and budgets | reliability-engineering.md |
| 5 | Operational toil | organization.md; cloud-delivery.md |
| 6 | Distributed telemetry | observability.md |
| 7–9 | Automation, delivery and complexity | cloud-delivery.md; changes.md; reliability-engineering.md |
| 10 | Alert design | observability.md |
| 11 | On-call practice | organization.md; incidents.md |
| 12–14 | Diagnosis, emergencies and command | incidents.md |
| 15–16 | Learning and outage records | learning.md; incidents.md |
| 17–18 | Testing and operational software | reliability-engineering.md; cloud-delivery.md |
| 19–20 | Frontend and internal traffic distribution | networking-storage.md; reliability-engineering.md |
| 21–22 | Saturation and propagation of failures | reliability-engineering.md; incidents.md |
| 23 | Quorum and authoritative state | data-services.md; reliability-engineering.md |
| 24–26 | Scheduled work, pipelines and integrity | data-services.md; reliability-engineering.md |
| 27 | Launch readiness | changes.md; cloud-delivery.md |
| 28–32 | Training, interrupts, team overload, collaboration and engagement | organization.md |
| 33–34 | Cross-industry learning and synthesis | learning.md; organization.md |
| Appendices A–F | Availability math; production, incident, review, launch and meeting examples | reliability-engineering.md; incidents.md; learning.md; changes.md; organization.md |

## SRE workbook

**Source:** *The Site Reliability Workbook* (2018), [official contents](https://sre.google/workbook/table-of-contents/). Access: public online text.

| Chapters | Subject coverage | Skill references |
| --- | --- | --- |
| 1 | SRE within DevOps | organization.md |
| 2–3 | Implementing objectives and learning from examples | reliability-engineering.md |
| 4–5 | Instrumentation and budget-based alerts | observability.md; reliability-engineering.md |
| 6–7 | Reducing toil and unnecessary complexity | organization.md; cloud-delivery.md; reliability-engineering.md |
| 8–9 | On-call and incident operations | incidents.md; organization.md |
| 10 | Reviewing failures constructively | learning.md |
| 11–12 | Load behavior and concrete system sizing | reliability-engineering.md |
| 13 | Processing data reliably | data-services.md |
| 14–15 | Configuration architecture and implementation | changes.md; cloud-delivery.md |
| 16 | Progressive release validation | changes.md; cloud-delivery.md |
| 17 | Recovering overloaded engineering teams | organization.md |
| 18–21 | Engagement, wider adoption, team evolution and organizational change | organization.md |
| Appendices A–C | Objective specifications, budget policies and incident-pattern analysis | reliability-engineering.md; learning.md |

Distinguish team operational overload in chapter 17 from service traffic overload in chapter 11. Technical change review and organizational change management also require different workflows.

## Secure and reliable systems

**Source:** *Building Secure and Reliable Systems* (2020), [official hosted book](https://google.github.io/building-secure-and-reliable-systems/) and [contents](https://google.github.io/building-secure-and-reliable-systems/raw/toc.html). Access: public online text.

| Chapters | Subject coverage | Skill references |
| --- | --- | --- |
| 1–2 | Security/reliability interaction and adversarial risk | reliability-engineering.md; incidents.md |
| 3–4 | Safe administration and engineering tradeoffs | cloud-delivery.md; changes.md |
| 5–7 | Minimal privilege, comprehensibility and evolution | cloud-delivery.md; reliability-engineering.md; changes.md |
| 8–10 | Resilience, recoverability and service-exhaustion attacks | reliability-engineering.md; networking-storage.md; incidents.md |
| 11 | Certificate-service case study | networking-storage.md; cloud-delivery.md |
| 12–14 | Safer code, assurance and deployment provenance | cloud-delivery.md; changes.md |
| 15 | Investigation, evidence and controlled debugging | incidents.md; observability.md |
| 16–18 | Disaster preparation, crisis response and recovery | incidents.md; reliability-engineering.md; data-services.md |
| 19–21 | Team lessons, responsibility and sustainable culture | organization.md; learning.md |
| Appendix | Disaster-risk assessment | reliability-engineering.md |

Apply these concerns throughout the skill rather than treating security as a final checklist. Include trusted recovery paths, administrative dependencies, evidence integrity and privacy in diagnostic design.

## Second edition: public topic map

**Source:** *Site Reliability Engineering*, second edition, [publisher contents and overview](https://www.oreilly.com/library/view/site-reliability-engineering/9798341607675/), dated **September 2026**. Google also [lists the edition](https://sre.google/books/). Access: public topic outline; complete chapter text requires access. Do not describe this mapping as a complete reading or reproduction of the edition.

| Chapters | Publicly identified topics | Skill references |
| --- | --- | --- |
| 1–3 | SRE context, business value and production trends | organization.md; reliability-engineering.md; cloud-delivery.md |
| 4–7 | Culture, careers, organizational structure and engagement | organization.md |
| 8 | Objectives including customer-level experience | reliability-engineering.md |
| 9 | Modern observability and measurement limits | observability.md |
| 10–11 | Incident operations and learning | incidents.md; learning.md |
| 12 | Systems-based prospective and retrospective analysis | learning.md; changes.md |
| 13–14 | Automation and assurance | cloud-delivery.md; reliability-engineering.md |
| 15–16 | Capacity and data management | reliability-engineering.md; data-services.md |
| 17–18 | Resilient products and platform engineering | reliability-engineering.md; cloud-delivery.md; organization.md |
| 19–21 | Delivery evolution, operating AI and AI assistance | ai-systems.md; cloud-delivery.md |
| 22–23 | Diverse operating contexts and future direction | organization.md; linux-vms-windows.md; ai-systems.md |
| Appendices A–G | Training economics, charters, meetings, objective composition and telemetry statistics | organization.md; reliability-engineering.md; observability.md |

## Investigation methodology sources

- **Barrier analysis:** James Reason, [Human error: models and management](https://www.bmj.com/content/320/7237/768) (2000); [accessible author article](https://pmc.ncbi.nlm.nih.gov/articles/PMC1070929/). Use the Swiss cheese model to examine immediate actions, latent conditions and defensive weaknesses; route to learning.md.
- **Five Whys:** Google's [example postmortem](https://sre.google/sre-book/example-postmortem/) mentions this technique. Use evidence-backed, branching questions; do not force exactly five steps or one cause. Route to learning.md.
- **Systems analysis:** Google's [STAMP/STPA/CAST overview](https://sre.google/resources/practices-and-processes/stpa/) distinguishes prospective STPA from retrospective CAST. Read the [MIT handbooks](https://psas.scripts.mit.edu/home/books-and-handbooks/) for method detail; route to learning.md and changes.md.
- **Learning culture:** Google's [original postmortem guidance](https://sre.google/sre-book/postmortem-culture/) and [workbook practice](https://sre.google/workbook/postmortem-culture/), plus John Allspaw's [primary Etsy account](https://www.etsy.com/codeascraft/blameless-postmortems). Reconstruct information available at the time, retain accountability for improvements and avoid personal blame.

## Apply the sources

Adapt practices to the actual service, risk tolerance, staffing, ownership and operating constraints. Treat Google-specific implementation details and staffing targets as examples. Separate stable engineering principles from version-sensitive commands and product features. Cite the specific chapter or official technical documentation that supports a factual recommendation; describe local extensions and conclusions as the skill's own analysis.
