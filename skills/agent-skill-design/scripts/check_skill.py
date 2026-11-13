#!/usr/bin/env python3
"""Lint one agent skill folder. Output: LEVEL CODE path:line message.

Exit codes: 0 no ERROR, 1 at least one ERROR, 2 usage error.
Standard library only.
"""
import argparse
import json
import re
import sys
from pathlib import Path

PORTABLE_KEYS = {"name", "description", "license", "compatibility", "metadata"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
VERB_RE = re.compile(r"^[A-Z][a-z]+s\b")
PERSON_RE = re.compile(r"\bI\b|\bI'm\b|\b(you|your|my)\b", re.I)
PARENT_RE = re.compile(r"\.\./")
ABS_RE = re.compile("/Us" + "ers/|/ho" + "me/|(?<![\\w.])" + "~" + "/")
SYS_RE = re.compile(r"(?<![\w.])/(etc|var|usr|opt)/")
LINK_RE = re.compile(r"\]\(([^)\s#]+)")
TEXT_SUFFIXES = {".md", ".py", ".sh", ".json", ".yaml", ".yml", ".txt", ".tmpl", ".toml"}


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return json.loads(value)
        except ValueError:
            return value[1:-1].replace('\\"', '"')
    return value


def parse_frontmatter(lines):
    """Return (fields {key: (value, line)}, body_start_index) or (None, 0)."""
    if not lines or lines[0].strip() != "---":
        return None, 0
    fields, block, i = {}, None, 1
    while i < len(lines) and lines[i].strip() != "---":
        line = lines[i]
        m = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if m:
            key, raw = m.group(1), m.group(2)
            if raw.strip() in (">", "|", ">-", "|-"):
                fields[key] = ("", i + 1)
                block = key
            else:
                fields[key] = (unquote(raw), i + 1)
                block = None
        elif block and line.startswith((" ", "\t")):
            fields[block] = ((fields[block][0] + " " + line.strip()).strip(), fields[block][1])
        i += 1
    if i >= len(lines):
        return None, 0
    return fields, i + 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="Lint an agent skill folder.")
    ap.add_argument("skill", help="path to the skill folder (holds SKILL.md)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--portable", action="store_true",
                    help="treat client-only frontmatter keys as ERROR (use when porting)")
    ap.add_argument("--max-desc", type=int, default=1024, help="description limit (default 1024)")
    ap.add_argument("--max-body-lines", type=int, default=500, help="BODY-LONG threshold")
    try:
        args = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    skill = Path(args.skill)
    sk = skill / "SKILL.md"
    out = []

    def add(level, code, path, line, msg):
        out.append({"level": level, "code": code, "path": str(path), "line": line, "message": msg})

    if not sk.is_file():
        print(f"error: no SKILL.md in {skill}", file=sys.stderr)
        return 2
    lines = sk.read_text(encoding="utf-8", errors="replace").splitlines()
    fields, body_at = parse_frontmatter(lines)
    if fields is None:
        add("ERROR", "FM-MISSING", sk, 1, "SKILL.md has no closed frontmatter block")
        fields = {}
    name = fields.get("name", ("", 1))
    if name[0] != skill.resolve().name:
        add("ERROR", "NAME-MISMATCH", sk, name[1], f"name '{name[0]}' differs from folder '{skill.resolve().name}'")
    if not NAME_RE.match(name[0]) or len(name[0]) > 64:
        add("ERROR", "NAME-FORMAT", sk, name[1], "name must be lower-case letters, digits, single hyphens, at most 64")
    desc, dline = fields.get("description", ("", 1))
    if len(desc) > args.max_desc:
        add("ERROR", "DESC-LONG", sk, dline, f"description has {len(desc)} chars, limit {args.max_desc}")
    if PERSON_RE.search(desc):
        add("ERROR", "DESC-PERSON", sk, dline, "description must be third person (no I, you, my)")
    if not VERB_RE.match(desc) or "Use when" not in desc:
        add("ERROR", "DESC-FORM", sk, dline, "description must start with a verb ('Fills ...') and contain 'Use when'")
    if not re.search(r"\bnot\b", desc, re.I):
        add("WARN", "DESC-NEIGHBOUR", sk, dline, "no 'not for ... (use <neighbour>)' clause naming the nearest skill")
    for k, (_, ln) in fields.items():
        if k not in PORTABLE_KEYS:
            hint = "experimental in the open spec" if k == "allowed-tools" else "client-only key"
            add("ERROR" if args.portable else "WARN", "KEY-CLIENT", sk, ln,
                f"'{k}' is {hint}; keep it only while the skill stays on that client, else move its intent into the body")
    body = lines[body_at:]
    if len(body) > args.max_body_lines:
        add("WARN", "BODY-LONG", sk, body_at + 1, f"body has {len(body)} lines; move lookups into references/")

    linked = set()
    for n, line in enumerate(lines, 1):
        for target in LINK_RE.findall(line):
            if re.match(r"^[a-z]+:", target):
                continue
            linked.add((skill / target).resolve())
            if not (skill / target).exists():
                add("ERROR", "REF-BROKEN", sk, n, f"link target '{target}' does not exist")
    refs = skill / "references"
    if refs.is_dir():
        for r in sorted(refs.rglob("*.md")):
            if r.resolve() not in linked:
                add("WARN", "REF-ORPHAN", r, 1, "reference is not linked from SKILL.md")
            for n, line in enumerate(r.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                for target in LINK_RE.findall(line):
                    if target.endswith(".md") and not re.match(r"^[a-z]+:", target):
                        add("WARN", "REF-NESTED", r, n, f"reference links to '{target}'; keep references one level deep")

    for f in sorted(skill.rglob("*")):
        if not f.is_file() or f.suffix not in TEXT_SUFFIXES:
            continue
        parts = f.relative_to(skill).parts
        if "evals" in parts or "fixtures" in parts:
            continue
        for n, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if PARENT_RE.search(line):
                add("ERROR", "PATH-PARENT", f, n, "parent-directory path escapes the skill folder")
            if ABS_RE.search(line):
                add("ERROR", "PATH-ABS", f, n, "absolute or home path; use paths relative to the skill root")
            if SYS_RE.search(line):
                add("WARN", "SYSDIR", f, n, "system directory path; fine only if the path is the subject, not a dependency")

    trig = skill / "evals" / "triggers.json"
    if trig.is_file():
        try:
            data = json.loads(trig.read_text(encoding="utf-8"))
        except ValueError as e:
            data = None
            add("ERROR", "TRIG-SHAPE", trig, 1, f"invalid JSON: {e}")
        if data is not None and not isinstance(data, list):
            add("ERROR", "TRIG-SHAPE", trig, 1, "top level must be a list")
        elif data is not None:
            pos = neg = 0
            seen = set()
            for i, e in enumerate(data):
                if not isinstance(e, dict):
                    add("ERROR", "TRIG-SHAPE", trig, 1, f"entry {i} is not an object")
                    continue
                q, s = e.get("query"), e.get("should_trigger")
                if not isinstance(q, str) or not q.strip():
                    add("ERROR", "TRIG-SHAPE", trig, 1, f"entry {i} has no string 'query'")
                elif q.lower() in seen:
                    add("WARN", "TRIG-DUP", trig, 1, f"entry {i} duplicates an earlier query")
                else:
                    seen.add(q.lower())
                if not isinstance(s, bool):
                    add("ERROR", "TRIG-SHAPE", trig, 1, f"entry {i} has no boolean 'should_trigger'")
                elif s:
                    pos += 1
                else:
                    neg += 1
            if pos == 0 or neg == 0 or max(pos, neg) > 2 * min(pos, neg):
                add("WARN", "TRIG-BALANCE", trig, 1, f"{pos} positives vs {neg} negatives; keep them roughly balanced")

    if args.json:
        print(json.dumps(out, indent=2))
    else:
        for o in out:
            print(f"{o['level']} {o['code']} {o['path']}:{o['line']} {o['message']}")
        if not out:
            print("OK no findings")
    return 1 if any(o["level"] == "ERROR" for o in out) else 0


if __name__ == "__main__":
    sys.exit(main())
