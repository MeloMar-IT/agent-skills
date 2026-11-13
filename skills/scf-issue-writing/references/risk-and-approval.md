# Risk and approval

High risk: destructive or irreversible change; production data; truncating, dropping or deleting data; credential or permission changes.

A high-risk story contains:
1. `Risk: high`, with the environment named in Scope or Context.
2. A backup or restore step as a precondition, with its own verification.
3. The irreversibility stated in words ("cannot be undone after step 3").
4. Reversible steps (dry run, count, copy) kept separate from irreversible ones.
5. `Approval: <owner of the affected system, from the repo's owner file> - pending` until the owner's written approval is recorded on the issue. Only then: `Approval: given by <owner> on <date>`.
6. Unknowns for every unverified claim (for example "nothing reads this table").
7. `Labels: none`, plus a sentence that a person sets `Factory_go` after approval.

A requester asking for the Foundry to run does not count as owner approval. Never write "approved by" or "granted" unless a recorded approval exists.

## Example (other domain)

Request: "Drop the `old_carts` table in prod `shop`, it's dead. Just run it."
- Risk: high. Approval: owner of `shop` per the owner file - pending.
- Precondition: dump of `old_carts` restored into a scratch database and row counts compared.
- Reversible step: list queries referencing `old_carts`. Irreversible step: the drop.
- Unknowns: whether any report reads `old_carts`.
