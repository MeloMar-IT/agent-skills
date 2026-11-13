# Splitting

1. Read the file limit per story (CONTRIBUTING, docs). Count Scope paths.
2. Cut by outcome and code+test pair, not by layer. `src/X.py` and `tests/test_X.py` travel together.
3. Order by imports: if story B's code imports story A's code, B has `Depends on: A`. A story that wires shared glue depends on the stories whose functions it calls.
4. Docs (README) go in the story that adds the behaviour if room remains, else in a later story that depends on it.
5. No cycles. Each story's Verification must pass with only its dependencies done, and names its own test file.
6. Name files `NN-<slug>.md` so the order is visible.

## Example cut (limit 2 files)

Request: add `--quality` to a thumbnailer: parsing in `src/quality.py`, use in `src/resize.py`, tests in `tests/test_quality.py` and `tests/test_resize.py`.

- 01-quality: `src/quality.py`, `tests/test_quality.py`; `Depends on: none`
- 02-resize: `src/resize.py`, `tests/test_resize.py`; `Depends on: 01-quality`

Wrong cuts: "all source files" then "all tests"; a story that needs a later story's import.
