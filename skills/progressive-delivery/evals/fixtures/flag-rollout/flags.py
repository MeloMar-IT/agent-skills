from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Flag:
    key: str
    percent: float
    unit: str = "user"


def is_enabled(flag: Flag, user_id: str | None, org_id: str | None = None) -> bool:
    return random.random() < flag.percent
