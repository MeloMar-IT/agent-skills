from flagclient import is_on


def export_rows(rows):
    if is_on("legacy-export"):
        return [",".join(str(c) for c in r) for r in rows]
    return [list(r) for r in rows]
