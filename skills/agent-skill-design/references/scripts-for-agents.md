# Scripts for agents

An agent runs a script without a terminal and reads what it prints. Design for that.

## Rules

- Never prompt: no `input()`, no "[y/N]". Stdin may be closed.
- Use `argparse` so `--help` works and bad usage exits 2.
- A destructive action is a preview by default. It acts only with an explicit flag such as `--apply` or `--yes`. The preview lists what would happen.
- Offer `--json` for machine output; print one JSON document on stdout.
- Errors go to stderr, with stdout left empty. Use distinct non-zero exit codes: 2 usage, 3 input not found, 4 partial failure.
- No ANSI colour unless `sys.stdout.isatty()`.
- Running twice is safe (idempotent): a second `--apply` finds nothing left to do and exits 0.
- Standard library only, or declare dependencies in the skill.
- Find bundled files with `Path(__file__).resolve().parent`.
- Keep an existing call form working. If users run `tool.py A B`, positional arguments `A B` stay; add flags beside them.
- Every function the skeleton calls is defined, and the file ends with `if __name__ == "__main__":`.

## Skeleton: log rotation

Call form: `rotate_logs.py DIR --keep N --max-mb M [--apply] [--json]`.

```python
#!/usr/bin/env python3
"""Rotate *.log files in DIR: keep the newest N, drop those over M megabytes."""
import argparse, json, sys
from pathlib import Path

def plan(directory, keep, max_mb):
    logs = sorted(directory.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    doomed = logs[keep:] + [p for p in logs[:keep] if p.stat().st_size > max_mb * 1024 * 1024]
    return sorted(set(doomed))

def main(argv=None):
    ap = argparse.ArgumentParser(description="Rotate log files; preview unless --apply.")
    ap.add_argument("dir")
    ap.add_argument("--keep", type=int, default=5, help="newest files to keep")
    ap.add_argument("--max-mb", type=float, default=50, help="size limit in megabytes")
    ap.add_argument("--apply", action="store_true", help="really delete (default: preview)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    try:
        args = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    directory = Path(args.dir)
    if not directory.is_dir():
        print(f"error: {directory} is not a directory", file=sys.stderr)
        return 3
    doomed = plan(directory, args.keep, args.max_mb)
    if args.apply:
        for p in doomed:
            p.unlink()
    if args.json:
        print(json.dumps({"applied": args.apply, "files": [p.name for p in doomed]}))
    else:
        verb = "deleted" if args.apply else "would delete"
        for p in doomed:
            print(f"{verb} {p.name}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Checklist

- `--help` exits 0 and describes every argument.
- No flag: preview, nothing changed, exit 0.
- `--json`: valid JSON naming the affected items and nothing else.
- Missing input: message on stderr, nothing on stdout, non-zero exit.
- Bad value (a word where a number belongs): non-zero exit, message on stderr.
- Second run with the apply flag: exit 0, no error.
