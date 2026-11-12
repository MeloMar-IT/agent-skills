import json
from pathlib import Path


def is_on(key, default=False):
    flags = json.loads((Path(__file__).parent / "flags.json").read_text())
    return bool(flags.get(key, default))
