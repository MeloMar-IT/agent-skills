# Flags

`is_enabled(flag, user_id)` says whether a user gets the new behaviour.

Rules:

- A user's answer is the same across requests, processes, restarts and machines while the percentage is unchanged.
- Raising a percentage only adds users.
- `percent` is the share of users: 0.07 means 7%, 0.29 means 29%. Percentages go down to 0.0001 (0.01%) in steps of 0.0001, and each step must matter: 0.0003 serves 0.03% of users.
- Flags are run as independent experiments: one flag says nothing about another.
- `unit` is `"user"` (default) or `"org"`. A flag with unit `"org"` is decided per organisation, so every user of an org gets the same answer; `org_id` is passed as the third argument.
- Logged-out requests pass `user_id=None` or `""` and always get the old behaviour (False), even at 1.0.
- A flag with unit `"org"` and no `org_id` (None or `""`) gets the old behaviour (False), even at 1.0.
- 0.0 means nobody; 1.0 means every logged-in user (with an org, for org flags).
- Standard library only.
