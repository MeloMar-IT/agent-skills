import argparse
import json


def render(rows, fmt):
    if fmt == "text":
        return "\n".join(f"{r['id']} {r['customer']} {r['total']}" for r in rows)
    raise ValueError(fmt)


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--format", choices=["text"], default="text")
    p.add_argument("--data", default="data/invoices.json")
    a = p.parse_args(argv)
    with open(a.data) as fh:
        rows = json.load(fh)
    print(render(rows, a.format))


if __name__ == "__main__":
    main()
