#!/usr/bin/env python3
"""Canary statistics: one-sided Wilson/Newcombe bounds, exact bounds, bake volume.

Standard library only, offline. Copy the formulas into the project; do not
import this file from project code.

  canary_stats.py bound   ERRORS N [--z 1.645] [--exact]
  canary_stats.py compare CANARY_ERRORS CANARY_N CONTROL_ERRORS CONTROL_N --margin 0.001 [--z 1.645]
  canary_stats.py volume  --limit 0.001 [--z 1.645] [--exact]
  canary_stats.py bake    --limit 0.001 --rpm 6000 --weight 0.01 [--warmup 5] [--floor 10] [--z 1.645] [--exact]
  canary_stats.py wald    ERRORS N [--z 1.645]     (shows why Wald is wrong)

Default z = 1.645: one-sided 95%. For two-sided 95% pass --z 1.96 everywhere.
"""
import argparse
import math

Z = 1.645


def wilson(e, n, z=Z):
    """Wilson score interval (lo, hi) for e errors in n requests."""
    if n <= 0:
        return 0.0, 1.0
    p = e / n
    z2 = z * z
    centre = p + z2 / (2 * n)
    spread = z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n))
    d = 1 + z2 / n
    return max(0.0, (centre - spread) / d), min(1.0, (centre + spread) / d)


def wald(e, n, z=Z):
    if n <= 0:
        return 0.0, 1.0
    p = e / n
    h = z * math.sqrt(p * (1 - p) / n)
    return max(0.0, p - h), min(1.0, p + h)


def _cdf(k, n, p):
    """P(X <= k) for X ~ Binomial(n, p), 0 < p < 1."""
    if k < 0:
        return 0.0
    total = 0.0
    lp, lq = math.log(p), math.log1p(-p)
    for i in range(0, min(k, n) + 1):
        lc = math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1)
        total += math.exp(lc + i * lp + (n - i) * lq)
    return min(1.0, total)


def alpha_of(z):
    """One-sided tail probability for z (z=1.645 -> 0.05)."""
    from statistics import NormalDist
    return 1 - NormalDist().cdf(z)


def exact(e, n, z=Z):
    """Clopper-Pearson (lo, hi) at the same one-sided level as z."""
    if n <= 0:
        return 0.0, 1.0
    a = 0.05 if abs(z - 1.645) < 0.001 else alpha_of(z)
    if e == 0:
        hi = 1 - a ** (1.0 / n)
    elif e >= n:
        hi = 1.0
    else:
        lo_p, hi_p = 0.0, 1.0
        for _ in range(100):
            mid = (lo_p + hi_p) / 2
            if _cdf(e, n, mid) > a:
                lo_p = mid
            else:
                hi_p = mid
        hi = (lo_p + hi_p) / 2
    if e == 0:
        lo = 0.0
    else:
        lo_p, hi_p = 0.0, 1.0
        for _ in range(100):
            mid = (lo_p + hi_p) / 2
            if 1 - _cdf(e - 1, n, mid) < a:
                lo_p = mid
            else:
                hi_p = mid
        lo = (lo_p + hi_p) / 2
    return lo, hi


def newcombe(e1, n1, e2, n2, z=Z, interval=wilson):
    """Bounds (lower, d, upper) for d = p1 - p2, p1 = canary, p2 = control."""
    p1 = e1 / n1
    p2 = e2 / n2
    l1, u1 = interval(e1, n1, z)
    l2, u2 = interval(e2, n2, z)
    d = p1 - p2
    upper = d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    lower = d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    return lower, d, upper


def verdict(lower, upper, margin):
    if upper <= margin:
        return "PASS"
    if lower > margin:
        return "FAIL"
    return "INCONCLUSIVE"


def min_volume(limit, z=Z, use_exact=False):
    """Smallest n for which 0 errors in n requests passes (upper <= limit)."""
    if use_exact:
        a = 0.05 if abs(z - 1.645) < 0.001 else alpha_of(z)
        return math.ceil(math.log(a) / math.log1p(-limit) - 1e-9)
    return math.ceil(z * z * (1 - limit) / limit - 1e-9)


def pct(x):
    return "%.3f%%" % (100 * x)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("bound", "wald"):
        s = sub.add_parser(name)
        s.add_argument("errors", type=int)
        s.add_argument("n", type=int)
        s.add_argument("--z", type=float, default=Z)
        if name == "bound":
            s.add_argument("--exact", action="store_true")
    c = sub.add_parser("compare")
    for a in ("e1", "n1", "e2", "n2"):
        c.add_argument(a, type=int)
    c.add_argument("--margin", type=float, required=True)
    c.add_argument("--z", type=float, default=Z)
    c.add_argument("--exact", action="store_true", help="use exact bounds inside the Newcombe formula")
    v = sub.add_parser("volume")
    v.add_argument("--limit", type=float, required=True)
    v.add_argument("--z", type=float, default=Z)
    v.add_argument("--exact", action="store_true")
    b = sub.add_parser("bake")
    b.add_argument("--limit", type=float, required=True)
    b.add_argument("--rpm", type=float, required=True, help="total requests per minute")
    b.add_argument("--weight", type=float, required=True, help="canary share of traffic, 0..1")
    b.add_argument("--warmup", type=float, default=5)
    b.add_argument("--floor", type=float, default=10)
    b.add_argument("--z", type=float, default=Z)
    b.add_argument("--exact", action="store_true")
    a = ap.parse_args()

    if a.cmd == "bound":
        lo, hi = (exact if a.exact else wilson)(a.errors, a.n, a.z)
        print("rate %s  lower %s  upper %s" % (pct(a.errors / a.n if a.n else 0), pct(lo), pct(hi)))
    elif a.cmd == "wald":
        lo, hi = wald(a.errors, a.n, a.z)
        print("WALD (do not use) lower %s  upper %s" % (pct(lo), pct(hi)))
    elif a.cmd == "compare":
        if a.n1 <= 0 or a.n2 <= 0:
            print("INCONCLUSIVE (no requests in one sample)")
            return
        interval = exact if a.exact else wilson
        lo, d, hi = newcombe(a.e1, a.n1, a.e2, a.n2, a.z, interval)
        print("d %s  lower %s  upper %s  margin %s -> %s" % (
            pct(d), pct(lo), pct(hi), pct(a.margin), verdict(lo, hi, a.margin)))
    elif a.cmd == "volume":
        print(min_volume(a.limit, a.z, a.exact))
    elif a.cmd == "bake":
        n = min_volume(a.limit, a.z, a.exact)
        per_min = a.rpm * a.weight
        minutes = a.warmup + math.ceil(n / per_min - 1e-9)
        print("min requests %d; canary rpm %.1f; bake minutes %d (floor %d)" % (
            n, per_min, max(minutes, a.floor), a.floor))


if __name__ == "__main__":
    main()
