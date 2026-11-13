#!/usr/bin/env python3
"""Tiny stand-in for kubectl. Supports:
  get pods -o json [-l k=v]
  delete pod NAME [--dry-run=client]
-n/--namespace and --context are accepted and ignored.
Reads $PODS_FILE (default pods.json); records deletes in $ACTIONS_LOG.
"""
import json
import os
import sys


def deleted_names(log):
    if not log or not os.path.exists(log):
        return set()
    with open(log) as f:
        return {ln.split(None, 1)[1].strip() for ln in f if ln.startswith("delete ")}


def main(argv):
    pos, selector, dry = [], None, False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("-n", "--namespace", "--context", "-o"):
            i += 2
            continue
        if a in ("-l", "--selector"):
            selector = argv[i + 1]
            i += 2
            continue
        if a.startswith("--dry-run"):
            dry = True
        elif a.startswith("-"):
            pass
        else:
            pos.append(a)
        i += 1
    log = os.environ.get("ACTIONS_LOG")
    path = os.environ.get("PODS_FILE", "pods.json")
    if pos[:2] == ["get", "pods"]:
        with open(path) as f:
            items = json.load(f)["items"]
        gone = deleted_names(log)
        out = []
        for p in items:
            name = p["metadata"]["name"]
            if name in gone:
                p = {
                    "metadata": {"name": name + "-new", "labels": p["metadata"]["labels"]},
                    "status": {
                        "phase": "Running",
                        "containerStatuses": [
                            {"restartCount": 0, "state": {"running": {"startedAt": "2026-11-13T00:00:00Z"}}}
                        ],
                    },
                }
            out.append(p)
        if selector:
            k, v = selector.split("=", 1)
            out = [p for p in out if p["metadata"]["labels"].get(k) == v]
        print(json.dumps({"kind": "List", "items": out}, indent=2))
        return 0
    if pos[:2] == ["delete", "pod"] and len(pos) == 3:
        name = pos[2]
        if dry:
            print("pod/%s deleted (dry run)" % name)
            return 0
        if log:
            with open(log, "a") as f:
                f.write("delete %s\n" % name)
        if name == os.environ.get("FAIL_ON"):
            print("Error from server: failed to delete pod %s" % name, file=sys.stderr)
            return 1
        print("pod \"%s\" deleted" % name)
        return 0
    print("fakectl: unsupported command: %s" % " ".join(argv), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
