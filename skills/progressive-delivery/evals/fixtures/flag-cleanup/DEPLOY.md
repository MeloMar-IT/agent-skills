# Deploying

- Rolling deploy: old and new code serve side by side for up to 30 minutes.
- The nightly invoice job keeps running the old version until its next start.
- `flags.json` is not deployed with the code: the flag service pushes it to every running instance (old and new) within seconds of merge.
- `is_on(key, default=False)` returns `default` for a key missing from `flags.json`.
- One merge is one release.
