# Deterministic verification

A check is one command, from the repo root, offline, exit 0 only when the story is done. The same input always gives the same result.

## Banned
- `sleep`, `date`, any wall-clock dependence
- `curl`, `wget`, CI or dashboard URLs, package downloads
- unseeded randomness (seed it, or do not use it)
- "check that it looks right", manual or visual steps

## Grep trap
A pattern beginning with `-` is read as an option and grep exits 2.
- Wrong: `grep -c "--quality" README.md`
- Right: `grep -q -e "--quality" README.md` or `grep -q -- "--quality" README.md`
- `grep -q` carries the result in the exit code; `grep -c` exits 0 whenever there is at least one match and prints a count you would have to compare.

## Fail first
For new behaviour, run the command against today's code (or reason it through): it must exit non-zero. A check that already passes proves nothing. Regression checks ("old output unchanged") may pass today; mark them as regression checks.

## Exact output
- `python3 -m src.resize in.png --quality 50 | grep -x -e "wrote out.jpg"` matches a whole line.
- `test "$(python3 -m src.tool --count)" = "3"` compares exactly.
- Exit-code checks: `python3 -m src.tool --count -1; test $? -eq 2`.
- Prefer calling the CLI, grep, or the project's test runner. Do not add new test files unless the story's Scope lists them.

## Mapping
One bullet per criterion, same order, so a reader sees which check proves which criterion.
