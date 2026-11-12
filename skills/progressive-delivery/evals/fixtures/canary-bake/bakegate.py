import math

LIMIT = 0.001
Z = 1.645


def verdict(errors, requests):
    if requests == 0:
        return "INCONCLUSIVE"
    p = errors / requests
    h = Z * math.sqrt(p * (1 - p) / requests)
    if p - h > LIMIT:
        return "FAIL"
    if p + h <= LIMIT:
        return "PASS"
    return "INCONCLUSIVE"


def decide(checkpoints, bake_minutes, extended=False):
    """checkpoints: {minute: {route: (errors, requests)}}, cumulative since the step started.

    Returns "promote", "wait", "extend", "hold" or "rollback".
    """
    raise NotImplementedError
