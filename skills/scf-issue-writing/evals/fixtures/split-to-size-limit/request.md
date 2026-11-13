# Request: --since

Add `--since YYYY-MM-DD|last` to the CLI.

- `by_date` goes in `src/filter.py`.
- `last_run` and `save_run` go in `src/state.py`.
- Wire it in `src/cli.py`, which already does `from src import filter, state`.
- Add tests in `tests/test_filter.py`, `tests/test_state.py` and `tests/test_cli.py`.
- Document it in `README.md`.
