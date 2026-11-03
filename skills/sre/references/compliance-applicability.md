# Regulatory applicability, standards, and assurance

Use this reference to identify which obligations may govern an SRE service, action, evidence set, or AI use. Pair it with [enterprise governance](enterprise-governance.md), [audit evidence](audit-evidence.md), and [AI governance](ai-governance.md). Treat the multinational's legal entities and services as the scope; do not infer that every subsidiary shares the parent's obligations or certification.

## Contents

- [Establish applicability before claiming compliance](#establish-applicability-before-claiming-compliance)
- [Distinguish candidate obligations](#distinguish-candidate-obligations)
- [Translate requirements into operational controls](#translate-requirements-into-operational-controls)
- [Control data movement and evidence handling](#control-data-movement-and-evidence-handling)
- [Maintain separate notification obligations](#maintain-separate-notification-obligations)
- [Interpret assurance accurately](#interpret-assurance-accurately)
- [Maintain the register and sources](#maintain-the-register-and-sources)

## Establish applicability before claiming compliance

Start with the organization's authoritative obligations register, contracts, policies, regulatory correspondence, and current service inventory. If these are unavailable, produce a candidate mapping with explicit unknowns and named decisions to resolve. Do not invent a legal conclusion, appointed officer, accepted exemption, or certification to fill a template. Continue useful analysis and authorized diagnostics while those decisions are resolved.

1. **Identify the entities and activities.** Record the legal entity providing the service, contracting entities, customers, employing entities, establishments, operating countries, and relevant regulators. Map the business service to systems, shared platforms, suppliers, and material subcontractors. A global platform can support several separately accountable entities.
2. **Describe the actual use.** Record service purpose and criticality, regulated business activities, public-company status where relevant, customer commitments, payment processing, personal or sensitive data, and the consequences of failure. For AI, identify intended purpose, actual autonomy, users, provider/deployer roles, affected people, and material modifications.
3. **Verify the source and timing.** Use enacted law and applicable national implementation, regulator rules, binding contracts, and adopted internal policy. Distinguish proposals, guidance, standards, and assurance commitments. Record version, jurisdiction, publication/effective/application dates, transition or grandfathering provisions, and date checked. A press release can identify a change; it does not replace the operative text for a clause-level interpretation.
4. **Obtain the appropriate determination.** Route unresolved legal scope to the designated Legal/Compliance owner and privacy issues to the responsible privacy function or DPO where appointed. Record the actual determination, rationale, source, scope, and review trigger. Do not assign a person or approval that has not been confirmed.
5. **Map to controls and evidence.** Link each applicable obligation to control objectives, accountable owners, implementation, affected service population, verification, evidence retention, and any reporting playbook. Keep one control linked to several obligations where justified; do not claim that a crosswalk makes them legally equivalent.

Use [regulatory-applicability.md](../assets/regulatory-applicability.md). Give each entry a status such as **confirmed applicable**, **confirmed not applicable with rationale**, **pending determination**, or **future requirement being prepared for**. Keep applicability separate from whether the controls are effective. An applicable requirement with no evidence is not a compliant requirement.

## Distinguish candidate obligations

Use this matrix as a starting inventory, not an exhaustive country or sector opinion. Confirm the entity, activity, current text, exceptions, and national or contractual details before treating a row as binding.

| Candidate source | Resolve applicability and scope | Translate into SRE work where applicable |
| --- | --- | --- |
| **EU/EEA GDPR and local privacy law** | Identify personal-data processing, territorial scope, controller/processor relationships, and local supplementary rules. An EU hosting region alone does not settle these questions. | Data-flow inventory, access control, minimization, security and recovery, processor arrangements, retention, breach evidence, and transfer assessment. See [Commission guidance on GDPR application](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/application-gdpr_en). |
| **NIS2 and national implementing law** | Check sector, entity size and exceptions, essential/important classification, establishment/jurisdiction, national registration and enforcement, and relevant implementing rules. | Cybersecurity risk management, incident handling, continuity, supply-chain security, access, vulnerability handling, and evidence of management oversight. Check the [Commission overview](https://digital-strategy.ec.europa.eu/en/policies/nis2-directive) and [national transposition status](https://digital-strategy.ec.europa.eu/en/policies/nis-transposition). |
| **DORA and its delegated/implementing rules** | Determine whether the entity is an in-scope financial entity, an ICT supplier with relevant contractual duties, or a provider subject to designated critical-provider oversight. Resolve the interaction with NIS2 and national rules. | ICT risk governance, resilience testing, incident classification/reporting, ICT service registers, critical-function dependencies, contractual controls, concentration, and exit capability. Start from [Regulation (EU) 2022/2554](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022R2554). |
| **EU AI Act as amended** | Determine role, intended purpose, classification, exclusions, applicable provisions and transition dates. Enterprise use or an LLM label alone does not establish a high-risk classification. | AI inventory, documented operating boundaries, relevant transparency, oversight, technical documentation, monitoring, incident handling, and evidence. Use the [current Commission entry point](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) and the operative law. |
| **US financial-reporting controls and SOX-related requirements** | Ask Finance/Legal which registrants, financial processes, systems, and dependencies support in-scope internal control over financial reporting; check exemptions and attestation requirements. | Access, changes, processing integrity, job execution, reconciliations, and traceable control evidence for the identified financial-reporting scope. See [SEC guidance](https://www.sec.gov/rules-regulations/staff-guidance/compliance-disclosure-interpretations/managements-report-internal-control-over-financial-reporting-certification-disclosure-exchange-act). |
| **SEC cybersecurity disclosures** | Check registrant status, domestic versus foreign-private-issuer rules, materiality decisions, and applicable forms. Operational severity and securities-law materiality are different decisions. | Timely impact facts, decision timestamps, governance records, and escalation to the authorized disclosure process. Use the [SEC compliance guide](https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/cybersecurity-risk-management-strategy-governance-incident-disclosure) with the actual rules. |
| **Other country, industry, and customer requirements** | Add actual countries and sectors: privacy, critical infrastructure, financial services, healthcare, telecoms, public-sector hosting, records, employment, export restrictions, and contractual commitments as relevant. | Maintain country/entity overlays, permitted support locations, records schedules, supplier conditions, notification routes, and any local operational constraints. Retrieve the responsible authority's current primary source for each entry. |
| **PCI DSS** | Confirm payment-account-data flows, systems that can affect the cardholder-data environment, service-provider dependencies, and the validation program required by the payment brand/acquirer or other accepting entity. | Scope diagrams, segmentation evidence, access, logging, vulnerability/change controls, supplier responsibility, and required assessment evidence. See [PCI DSS scope](https://www.pcisecuritystandards.org/standards/pci-dss/) and [validation responsibilities](https://www.pcisecuritystandards.org/faqs/1473/). |
| **ISO/IEC 27001, ISO 22301, ISO/IEC 20000-1, ISO/IEC 42001** | Identify which management-system standards the organization has adopted or contractually committed to, the exact edition/amendments, and the defined certification or implementation scope. | Integrate information security, business continuity, service management, and AI management with operated controls, internal assessment, management review, and improvement. Consult the public scope pages listed below and the authorized full standards for detailed mappings. |
| **SOC 1 and SOC 2 assurance** | Identify the requested report, service/system boundary, selected criteria, examination period/date, exceptions, and intended users. | Supply accurate evidence and evaluate supplier reports within their scope. SOC 1 concerns controls relevant to user entities' financial reporting; SOC 2 addresses relevant trust-services criteria. These are examination reports, not generic certifications. See [AICPA's explanation](https://www.aicpa-cima.com/news/article/become-a-soc-er-player-and-win-at-risk-management). |
| **NIST CSF and RMF** | Determine whether they are voluntarily adopted, required by an applicable program, or incorporated into a contract or policy. | Use [CSF 2.0](https://csrc.nist.gov/pubs/cswp/29/the-nist-cybersecurity-framework-csf-20/final) for risk outcomes and communication; use [RMF](https://csrc.nist.gov/pubs/sp/800/37/r2/final) for a structured security/privacy risk lifecycle. A framework mapping does not itself establish regulatory compliance. |

## Translate requirements into operational controls

Maintain the chain **obligation → risk/control objective → implemented control → scoped evidence → assessment → remediation or authorized exception**. Distinguish a requirement from the chosen implementation: a particular cloud tool, ticketing system, change board, or SLO percentage is not automatically mandated by a general obligation.

For each mapped control, identify the local and inherited portions. A group security service may operate identity controls while a subsidiary remains responsible for its own user lifecycle, privileged roles, and exception handling. Verify the responsibilities retained by customers of outsourced services. Require evidence of the inherited service's relevant scope and operation, not simply its supplier's logo or assurance badge.

Keep regulatory thresholds, contractual promises, internal risk tolerances, SLOs, RTO/RPOs, and operational alert thresholds separately defined. Reconcile incompatible commitments through the accountable owners. An error budget cannot authorize breaching a legal requirement; a passed compliance assessment cannot establish that a service meets its user-facing reliability objectives.

Record unresolved conflicts between global and local requirements and route a concrete decision with facts, options, consequence, and urgency. Do not assume that copying the strictest rule everywhere is lawful, feasible, or sufficient. A global minimum can coexist with different regional implementations and evidence locations. Preserve the existing authorized change and emergency processes; a new mapping must not silently invent additional approval gates for routine work.

## Control data movement and evidence handling

Map production data, telemetry, traces, support bundles, backups, crash dumps, tickets, prompts, embeddings, model outputs, and audit exports. Record purpose, classification, legal-entity owner, location, permitted recipients, access path, retention, and deletion. Trace the actual data flows rather than inferring them from the application's advertised hosting region.

Keep **storage location**, **processing location**, **remote access**, and **international transfer** as separate questions. A support engineer's or supplier's access can matter even when storage stays in one region. Determine whether a transfer involves a separate controller or processor; not every employee's access from another country is automatically a Chapter V transfer. The [EDPB's transfer guidelines](https://www.edpb.europa.eu/documents/guideline/guidelines-052021-on-the-interplay-between-the-application-of-article-3-and-the_en) explain that distinction. Evaluate security and local-law implications independently of the transfer classification.

Have the appropriate privacy/legal owner confirm the transfer mechanism, recipient and onward-transfer conditions, applicable assessments, and supplementary safeguards where required. Do not infer a universal requirement that all EU personal data remain in the EU, or that an approved destination permits unrestricted reuse. Check residency commitments in contracts and sector/localization rules separately from general privacy-law transfer rules.

Define evidence minimization, masking, access, regional storage, and authorized audit export. Apply the actual retention schedule and lawful preservation holds; avoid both indefinite collection and premature deletion. Check employee-monitoring, communications interception, works-council/consultation, and labor-law constraints before introducing relevant recording or session-monitoring practices. Record local determinations rather than assuming one global consent or employee policy settles them. Follow [audit-evidence.md](audit-evidence.md) for preservation and access controls.

## Maintain separate notification obligations

Maintain a verified notification playbook per applicable obligation and entity. One incident may create security, privacy, resilience, market-disclosure, contractual, customer, insurance, or local reporting duties with different triggers. Do not use one universal reporting deadline or wait for a completed postmortem before escalating a possible obligation.

For each route, record:

- The triggering event, threshold, relevant awareness/materiality/classification decision, accountable decision owner, and source provision.
- The original event and awareness timestamps, timezone, uncertainty, due-time calculation, calendar/business-day treatment, and any staged updates or final report.
- Required recipients and content, approved submission channel, recipient-verification method, backup contact, permitted submitter, and proof of delivery.
- Whether delegated reporting is permitted, the retained entity accountability, information still missing, and the process for correcting or supplementing a notice.

Keep the clocks distinct. The [Commission's breach guidance](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/obligations_en) distinguishes controller and processor handling, while the [SEC guide](https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/cybersecurity-risk-management-strategy-governance-incident-disclosure) distinguishes materiality-based domestic reporting from foreign-private-issuer disclosures. Retrieve the applicable rules and playbook before calculating a specific deadline. Route uncertainty promptly to the designated function; do not invent a classification or treat missing facts as proof that no reporting duty exists.

Prepare factual drafts and an evidence timeline within existing authorization. Send only when explicitly authorized, through the confirmed route. Preserve the distinction between a draft, an approved statement, a submitted notice, and verified receipt. Limit disclosure to the necessary authorized information.

## Interpret assurance accurately

Separate **control design**, **implementation**, **operation over a period**, and **independent assurance**. State the assessed entity, service, system boundary, population, period, criteria/version, tests, exclusions, exceptions, and opinion or conclusion. Do not extrapolate a subsidiary's certificate or a supplier's report to an entire multinational estate.

For supplier reports, inspect scope, service locations, report type and period, qualifications, complementary user-entity controls, subservice-organization treatment, and gaps since the covered period. Confirm which customer responsibilities are actually implemented. A bridge letter or management assertion is additional context, not automatically the same assurance as a fresh examination.

Use precise language: **mapped to**, **implemented**, **tested**, **evidence pending**, **examined within the stated scope**, or **certified within the stated scope**. Do not call a skill, a checklist, or a generated control mapping ISO-certified, SOC 2-certified, regulator-approved, or universally compliant. ISO explains that [external certification bodies perform certification](https://www.iso.org/management-system-standards.html); implementation and certification are distinct decisions.

## Maintain the register and sources

Assign an actual owner and a risk-based review cadence. Reassess on acquisitions, new entities/countries, changed products or customers, new subprocessors, data-location changes, AI role/use changes, material incidents, contractual changes, and legislation or standards updates. Keep the previous determination, source snapshot, new interpretation, affected controls, and implementation decision traceable.

Primary-source review date: **3 November 2026**. Recheck at use time. The Commission's [AI Omnibus entry-into-force notice](https://digital-strategy.ec.europa.eu/en/news/ai-omnibus-enters-force) and indexed [Regulation (EU) 2026/1744](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX%3A32026R1744) show why original AI Act schedules can be stale. Direct full-text retrieval of some EUR-Lex pages was blocked during this review; verified indexed passages and official explanations support this source map, not a claim to have reviewed every operative provision. Obtain the current full text for final legal interpretation. Treat proposals separately from enacted amendments.

| Public primary reference | Use and limit |
| --- | --- |
| [ISO/IEC 27001](https://www.iso.org/standard/27001) | Information-security management-system scope. |
| [ISO 22301](https://www.iso.org/standard/75106.html) | Business-continuity management-system scope. |
| [ISO/IEC 20000-1](https://www.iso.org/standard/70636.html) | Service-management-system scope and service lifecycle. |
| [ISO/IEC 42001](https://www.iso.org/standard/42001) | AI-management-system scope. |
| [AICPA Trust Services Criteria](https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022) | Verify the criteria used by the actual examination; do not assume every category was included. |
| [PCI SSC's role](https://www.pcisecuritystandards.org/about_us/) | The Council maintains standards; the applicable compliance program determines validation obligations. |

Use licensed or otherwise authorized full standards for detailed clause mappings. Do not invent clause numbers or reconstruct unavailable copyrighted standards from summaries. Preserve the distinction between public source descriptions, organizational implementation choices, and legally validated obligations.
