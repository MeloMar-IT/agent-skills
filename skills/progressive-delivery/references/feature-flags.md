# Percentage rollout and feature flags

## Bucketing

- Bucket = stable hash of `flag_key:salt:unit_id` (for example sha256, first 8 bytes as an integer), modulo 10000.
- Never use Python's `hash()` (differs between processes) or per-request randomness (users flip).
- On means `bucket < round(percent * 10000)`, or integer basis points. `percent * 100` has float errors: 0.07 × 100 = 7.000000000000001 serves 8%. Clamp percent to 0..1; 0 means nobody, 1 means everyone with an id.
- Salt each flag separately: two independent 50% flags then overlap by about 25%. Share a salt only on purpose (mutually exclusive tests).
- Raising the percentage only adds users; lowering it removes the most recently added. Never change the salt or the bucketing unit during a rollout.
- A missing unit id (None or "") is never hashed. It gets the documented fallback, normally the old behaviour, even at 100%. Never fall back to another unit (an org flag with no org id does not bucket by user id): that changes the bucketing unit.

## Flag hygiene

- Every flag has a type (release, kill switch, experiment, permission), an owner and a removal ticket.
- The code default is what is served when the flag system cannot answer: choose the safe one.
- Never reuse a key.

## Two-phase cleanup

Needed exactly when production serves a value that differs from what a missing key evaluates to. Example: a flag fully on while missing keys evaluate to off.

- Phase 1: code stops reading the flag and hard-codes the served behaviour (including every other reader, e.g. batch jobs); the definition stays, so old instances still read it.
- Phase 2: delete the definition once every reader runs phase-1 code. Readers include other regions, batch jobs that keep the old version until restart, and old mobile clients. List phase 2 in the follow-up file or ticket.
- When the served value equals the missing-key value (a killed flag that is off, where missing means off), remove code and definition in one change.
- Find every reference: other services, jobs, templates, and keys built from strings.
