## Context
Users want to control how many decimals the converter prints.

## Scope
- src/units.py
- README.md

## Out of scope
- New units

## Acceptance criteria
1. `python3 -m src.units 1 km mi --precision 2` prints exactly `0.62`.
2. `--precision 0` prints `1`.
3. Without the flag the output stays `0.621371`.
4. A negative precision exits 2.
5. The README documents `--precision`.

## Verification
- check the numbers look right
- `sleep 2 && date +%s`
- `curl -s https://ci.example.com/job/units/lastBuild/api/json`
- `grep -c "--precision" README.md`
- a `random.random()` spot check

## Unknowns
- none

Depends on: none
Risk: low
Approval: not required
Labels: none
