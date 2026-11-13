# Labels and watchers

Everything here is **reported** by the project's own notes, not **observed** by running the Foundry; other details stay **unknown**.

- A person sets `Factory_go` to start the Foundry. Authors never list it in `Labels:`.
- The Foundry sets `factory:working` while a run is going. Never set it by hand. One run happens at a time.
- `Labels:` holds only labels to set now; write `Labels: none` otherwise.
- Planner questions wait on the issue. A `/defaults` comment takes the planner's recommendations.
- `scf skill-improve=<name>` in an issue asks for a new version of the existing `skills/<name>`.
- Do not write the Foundry's HTML comment markers. Other internals are unknown unless a supplied doc says so.
- This skill drafts text; it does not run commands that set labels.
