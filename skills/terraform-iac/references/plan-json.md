# Plan JSON

Fields of `resource_changes[]`: `address`, `previous_address`, `deposed`, `mode`, `action_reason`, and `change` with `actions`, `before`, `after`, `after_unknown`, `before_sensitive`, `after_sensitive`, `replace_paths`, `importing`.

Classification:
- `["no-op"]` + `importing` is an import; + `previous_address` is a move; otherwise skip.
- Both orders of create and delete are a replace (the order tells create-before-destroy).
- `["read"]` with `mode: data` is a data read.
- Unknown combination or top-level `errored: true`: fail closed (non-zero exit).

Redaction: a sensitivity tree is `true`, `false`, or a dict/list that mirrors the value. Redact at every leaf where the tree says true, in both before and after. Output changes carry a plain boolean. Never print `variables`, `prior_state` or `planned_values`. Treat plan files as secrets.

```python
MASK = "(sensitive value)"

def redact(val, sens, unknown=None):
    if unknown is True:
        return "(known after apply)"
    if sens is True:
        return MASK
    if isinstance(val, dict):
        s = sens if isinstance(sens, dict) else {}
        u = unknown if isinstance(unknown, dict) else {}
        return {k: redact(v, s.get(k), u.get(k)) for k, v in val.items()}
    if isinstance(val, list):
        s = sens if isinstance(sens, list) else []
        u = unknown if isinstance(unknown, list) else []
        return [redact(v, s[i] if i < len(s) else None, u[i] if i < len(u) else None)
                for i, v in enumerate(val)]
    return val

def classify(rc):
    ch = rc["change"]
    a = ch.get("actions", [])
    if a in (["delete", "create"], ["create", "delete"]):
        return "replace"
    if a == ["no-op"]:
        if ch.get("importing"):
            return "import"
        return "move" if rc.get("previous_address") else None
    if a in (["create"], ["update"], ["delete"], ["read"], ["forget"]):
        return a[0]
    raise SystemExit("unknown action combination: %r" % (a,))
```

Flatten nested attributes to dotted paths and find the changed paths by comparing the raw `before` and `after`, never the redacted copies (both sides of a sensitive attribute read the same mask, so a password rotation would vanish). Redact only what you print. For a changed sensitive path, list the name and say "(sensitive value) changed", never the value. Unknown attributes are absent from `after`; also walk the keys of `after_unknown` and print "(known after apply)" for them. A `["update"]` that also has `previous_address` or `importing` is still a move or import: mention both. Terraform 1.7+ records a `removed` block with `destroy = false` as a `forget` action: report it as "removed from state, not destroyed" instead of failing closed.
