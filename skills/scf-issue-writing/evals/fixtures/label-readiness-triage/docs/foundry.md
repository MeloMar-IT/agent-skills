# Foundry house rules

A person sets the `Factory_go` label. Ready means the issue text is complete; a person still reviews and sets the label.

## Template

Sections: ## Context, ## Scope, ## Out of scope, ## Acceptance criteria, ## Verification, ## Unknowns. Closing lines: `Depends on:`, `Risk:`, `Approval:`, `Labels:`.

## Rules

- A story lists at most 3 files under Scope.
- Each Verification entry is one command that exits 0 only when the story is done, and gives the same result on every run.
- Approval for a high-risk story must come from the owner of the affected system, listed below.
- A high-risk story records its approval on the issue as `Approval: given by <owner> on <date>`.

## Owners

- orders database: Marta Ruiz
- build system: Jonas Weber
