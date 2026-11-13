# Self-contained skills

A skill folder may be copied into another repository's skills folder. It must work there.

## Rules

- Everything the skill reads or runs lives in its folder: `scripts/`, `references/`, `assets/`.
- Templates, themes and other files a script fills or copies go in `assets/`; documents the agent reads (style guides, rules) go in `references/` and are linked from SKILL.md.
- Say "run from the skill root" or give the path relative to it; never "from the repository root".
- Paths in SKILL.md and scripts are relative to the skill root, for example `scripts/export.py`, `assets/theme.json`.
- No parent-directory paths, no absolute or home paths, no path that only works from a repo root or one working directory.
- Scripts locate bundled files with `Path(__file__).resolve().parent` (then `.parent` once more to reach the skill root from `scripts/`), not with the current directory.
- Behaviour stays the same: the bundled script must give the same output as the original.
- Leave the originals where they are unless told to move them. Copy what the skill needs into its folder.
- Rules that live in repo docs (a style guide, a checklist) are copied into `references/` and linked from SKILL.md, so the agent can read them after the copy.
- Keep guards. A skill that stays on one client keeps its client-only keys; moving a skill is not porting.

## Worked example: a diagram-export skill

Before: the skill `diagram-export` runs `python3 tools/export.py diagram.src`, which opens `themes/dark.json` relative to the working directory, and its SKILL.md says "follow `docs/diagram-style.md`".

After:

```
diagram-export/
  SKILL.md                 # run: python3 scripts/export.py <file>
  scripts/export.py        # theme = Path(__file__).resolve().parent.parent / "assets" / "theme.json"
  assets/theme.json        # copy of themes/dark.json
  references/style.md      # copy of docs/diagram-style.md, linked from SKILL.md
```

In the script:

```python
from pathlib import Path
THEME = Path(__file__).resolve().parent.parent / "assets" / "theme.json"
```

The theme is still read from the file, not hard-coded, so editing `assets/theme.json` changes the output. The original `tools/export.py` and `themes/dark.json` stay in place.

## Verify

1. Run the original from its old location and save the output as the baseline.
2. Copy only the skill folder into a fresh `skills/` folder elsewhere.
3. Run the bundled script from a different working directory with an absolute input path; compare with the baseline.
4. Search the copy for parent-directory, absolute and home paths. Every backticked path in SKILL.md must exist inside the copy.
5. Run `python3 scripts/check_skill.py <skill-folder>`; PATH-PARENT and PATH-ABS must not appear.
