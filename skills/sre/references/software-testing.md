# Reliability testing and verification

Use this reference when implementing a fix, reviewing a release, designing a test strategy, validating automation, or investigating why existing checks missed a failure. Pair it with [coding.md](coding.md), [changes.md](changes.md), and [reliability-engineering.md](reliability-engineering.md). Select tests by the uncertainty they resolve and the consequence of failure.

## Contents

- [Define the evidence required](#define-the-evidence-required)
- [Choose the appropriate test layer](#choose-the-appropriate-test-layer)
- [Exercise operational failure modes](#exercise-operational-failure-modes)
- [Measure performance and recovery](#measure-performance-and-recovery)
- [Run within a truthful scope](#run-within-a-truthful-scope)
- [Maintain useful CI and regression evidence](#maintain-useful-ci-and-regression-evidence)
- [Report results and limits](#report-results-and-limits)
- [Sources and qualifications](#sources-and-qualifications)

## Define the evidence required

Start with the user outcome, changed behavior, and plausible failure mechanisms. Write the expected result independently of the implementation. For a payment retry, specify whether the ledger and customer receive one charge; do not assert only that a retry function was called. For a recovery test, require usable restored data and an application workflow, not merely a completed backup job.

Map each important risk to a test or another justified control. Prioritize irreversible effects, authorization boundaries, data integrity, concurrency, migrations, and changes with broad exposure. Avoid imposing every test type on every change. Do not add tests for reversible low-impact edits merely to satisfy a habit, or duplicate tests that cannot detect a distinct regression.

Establish a baseline and relevant versions. Inspect repository test commands, fixtures, environment variables, and external dependencies before running them. Confirm the actual interpreter/compiler, OS, database dialect, API/schema versions, feature flags, architecture, and build identity. Use documented flags for the installed tool, not remembered flags from another release.

## Choose the appropriate test layer

| Test type | Use it to establish | State the boundary |
|---|---|---|
| Static analysis, type checking, schema validation | Detect supported classes of syntax, type, API-shape, or policy defects early. | A parsed manifest, clean linter, or successful compilation does not demonstrate runtime behavior or safe deployment. |
| Unit and component tests | Verify local decisions, transformations, state transitions, and error paths with controlled inputs. | Mocks and stubs demonstrate behavior against the model supplied; they may encode the same wrong assumption as the implementation. |
| Property-based and fuzz testing | Explore invariants over generated inputs, sequences, encodings, or boundary conditions; retain minimized counterexamples. | State generator scope and resource bounds. Passing sampled cases does not prove all possible states. |
| Contract tests | Check producer/consumer expectations, protocol fields, compatibility, error semantics, and version transitions. | Validate contracts against authoritative specifications or real provider behavior where feasible; two matching mocks can share a defect. |
| Integration tests | Exercise actual interactions with the relevant database, queue, filesystem, network boundary, or API. | Identify which components are real, emulated, stubbed, or unavailable, and differences from production topology and policy. |
| End-to-end and smoke tests | Exercise selected critical user journeys across layers; use a small smoke set for rapid rollout feedback. | A smoke pass covers selected paths and cannot establish that major defects are absent. Include user-visible correctness, not only HTTP success. |
| Regression tests | Preserve an independently understood requirement or reproduce a prior defect. | Verify that the test would fail for the relevant defect when feasible; avoid snapshots that approve unintended behavior wholesale. |
| Performance and capacity tests | Measure behavior under specified load, duration, concurrency, and resource constraints. | State representativeness, bottlenecks, test-client limitations, and untested capacity assumptions. |
| Security and permission tests | Exercise tenant isolation, authentication, authorization, input handling, dependency/configuration checks, and secret exposure. | Match the authorized scope. Scanning or a clean test run cannot certify universal security or compliance. |
| Fault, resilience, and recovery tests | Exercise dependency failures, interrupted work, restore/failover paths, and monitoring or response controls. | Bound exposure and recovery; simulation does not establish behavior in a production failure. |

## Exercise operational failure modes

Select applicable cases from the actual risk model:

- **Input and selection:** absent, malformed, oversized, duplicate, out-of-order, unauthorized, cross-tenant, empty selector, unexpected broad selector, stale inventory, and incomplete pagination. Assert that failure cannot silently expand the target set.
- **Time and cancellation:** deadline expiry before and after remote acceptance, interrupted shutdown, cancelled parent work, slow consumers, time-zone and daylight-saving boundaries, and overlapping scheduled runs. Distinguish a cancellation request from verified termination.
- **Retry and partial completion:** transient failure, permanent rejection, throttling, exhausted budget, server delay, duplicate delivery, repeated idempotency key, and lost response after a committed write. Assert bounded attempts, consistent accounting, and truthful unknown outcomes.
- **Concurrency and resources:** duplicate workers, stale lease holder, conditional-write conflict, race, deadlock, queue saturation, connection exhaustion, disk-full behavior, and memory growth. Assert invariants across interleavings; sequential repeat tests alone do not establish concurrent safety.
- **Data and compatibility:** schema transitions, mixed application versions, encoding, null versus missing values, numeric boundaries, precision, retention, migration interruption, rollback compatibility, and reconciliation after replay. Verify totals, relationships, ownership, or checksums where relevant.
- **Diagnostics:** errors without secrets, bounded logs, useful failure codes, stable correlation identifiers, and signals that distinguish no traffic, missing telemetry, and healthy behavior. Verify alert routing or notification only within its authorized scope.

Use deterministic clocks, seeded randomness, controlled transports, and isolated fixtures where they help reproduce a failure. Do not replace the real dependency in every test of a dependency-specific problem. Test both safe rejection and useful successful work. Protect cleanup so it removes only resources created for the test; test cleanup failure when leaked resources materially matter.

## Measure performance and recovery

Choose **load** tests for expected traffic, **stress** tests for saturation and degradation, **spike** tests for abrupt changes, **soak** tests for accumulating leaks or backlog, and **scalability** tests for behavior as workload or capacity changes. Record request mix, payload sizes, concurrency, arrival pattern, cache state, data volume, dependency latency, and duration. Test relevant tenant and regional distributions.

Measure throughput, latency distributions, errors, timeouts, queue age, resource saturation, and business correctness together. Check whether a slow load generator hides demand or omits timed-out requests from latency statistics. Compare equivalent baselines and account for warmup, caching, and shared-environment noise. Stop when limits or abort criteria are reached; do not keep raising load until an uncontrolled outage occurs.

For resilience patterns, test the mechanism and its failure modes: bounded half-open circuit probes; bulkhead isolation under shared dependency saturation; safe retry after ambiguous completion; stale-writer rejection after failover; and capacity while replicas are unavailable. Verify that degradation preserves security and required data semantics. Check resumption after an automation process dies between two steps.

For backups and disaster recovery, measure recovery time and recovered-data age against the agreed RTO/RPO. Validate application use, permissions, keys, integrity, and outstanding work after restoration. Confirm failback or reconciliation where required. A successful restore command alone is incomplete evidence. Use [reliability-engineering.md](reliability-engineering.md) for the recovery plan and [incidents.md](incidents.md) if the experiment becomes an incident.

## Run within a truthful scope

Classify execution as local/isolated, staging, or live; name the actual target and identity. Check environment variables, connection strings, contexts, inventory, fixtures, hooks, and inherited credentials. Do not assume a command named `test`, a preview flag, or an emulated endpoint guarantees isolation.

Reuse authorization already granted. Ordinary local checks do not need repeated approval. For fault injection, penetration testing, destructive data fixtures, or live load, establish the applicable scope, owner, blast radius, monitoring, stop condition, and recovery capability. Complete preparatory code and plans before seeking any missing authorization. Never silently convert an offline request into a production experiment.

Keep fixtures sanitized and reproducible. Prevent accidental customer notifications, charges, writes to shared datasets, or credential leakage. State where synthetic data or emulators omit production behavior. Separate a dry-run assertion that no mutation occurred from a live assertion that a desired mutation worked.

## Maintain useful CI and regression evidence

Run fast checks early and place expensive integration, performance, or recovery checks where their risk justifies cost. Inspect CI secrets, permissions, dependencies, caches, and untrusted contributions. Preserve the identity of the tested artifact through promotion; rebuilding later creates another artifact to verify.

Treat failures as evidence to investigate. Distinguish a product defect from a test, fixture, runner, or dependency defect. Track flaky tests with an owner and bounded remediation; repeated reruns until green do not establish correctness. Keep required gates intact. Use incidents and escaped defects to improve the portfolio, including assumptions shared by implementation and tests.

Use coverage to find unexercised code, not to certify complete scenarios. When Go concurrency is relevant and the toolchain supports it, use the [race detector](https://go.dev/doc/articles/race_detector) with meaningful concurrent execution; it only detects races on executed paths. Apply analogous tools only after checking platform support, overhead, and what they actually detect.

## Report results and limits

Report: risk or invariant; test/command; artifact and versions; actual environment and dependency substitutions; expected and observed result; pass/fail/skipped status; evidence; and residual uncertainty. State when a test could not run and what remains unverified. Never label a mock-based test as a real cloud/database integration, or syntax validation as a successful deployment.

Stop expanding optional verification once the material risk is addressed and required gates pass. When a check fails, fix the defect or explain the concrete blocker rather than hiding it. Connect the final evidence to the requested outcome and the rollout observation still needed.

## Sources and qualifications

Adapted from the user-supplied *Essential SRE Articles* by Marcel Koert, chapter 10, with chapter 9's CI/CD context and chapter 12's reliability patterns. Retain its breadth while qualifying claims that coverage covers every scenario, mocks establish real integration, smoke tests exclude major defects, or chaos causes no user impact. Google's [Testing for Reliability](https://sre.google/sre-book/testing-reliability/) supplies the broader principle of reducing uncertainty through explicit tests; use the module's risk-specific evidence rules rather than treating any test suite as proof of future availability.
