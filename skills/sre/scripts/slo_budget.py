#!/usr/bin/env python3
"""Calculate an event-based SLO budget from supplied counts, entirely offline.

Example:
    python3 slo_budget.py --slo-percent 99.9 --total 1000000 --bad 1500 \
        --window-total 10000 --window-bad 200

Use counts for the same eligible population and evaluation window. This is not
a downtime calculator, an alert evaluator, or a future-traffic forecast.
"""

import argparse
import json
from decimal import Decimal, InvalidOperation, ROUND_FLOOR, localcontext


def nonnegative_count(value):
    try:
        result = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("supply a whole number of events") from exc
    if result < 0:
        raise argparse.ArgumentTypeError("event counts cannot be negative")
    return result


def target_percent(value):
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError("supply a finite percentage, e.g. 99.9") from exc
    if not result.is_finite() or not Decimal(0) < result < Decimal(100):
        raise argparse.ArgumentTypeError(
            "SLO percentage must be greater than 0 and less than 100; "
            "a 100% target has no finite burn-rate budget"
        )
    if result.as_tuple().exponent < -18:
        raise argparse.ArgumentTypeError("use at most 18 decimal places for the percentage")
    return result


def decimal_text(value):
    """Serialize decimals without binary floating-point conversion."""
    if value is None:
        return None
    if value == 0:
        return "0"
    text = format(value, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def evaluate(total, bad, target):
    if bad > total:
        raise ValueError("bad events cannot exceed eligible events")
    if total == 0:
        return {
            "eligible_events": 0,
            "bad_events": 0,
            "good_events": 0,
            "status": "no_data",
            "success_percent": None,
            "error_ratio": None,
            "allowed_bad_events": None,
            "max_whole_bad_events": None,
            "budget_consumed_percent": None,
            "remaining_bad_events": None,
            "remaining_budget_percent": None,
        }
    n = Decimal(total)
    b = Decimal(bad)
    allowance = n * (Decimal(1) - target)
    consumed = b / allowance
    return {
        "eligible_events": total,
        "bad_events": bad,
        "good_events": total - bad,
        "status": "within_slo" if b <= allowance else "outside_slo",
        "success_percent": decimal_text((n - b) / n * 100),
        "error_ratio": decimal_text(b / n),
        "allowed_bad_events": decimal_text(allowance),
        "max_whole_bad_events": int(allowance.to_integral_value(rounding=ROUND_FLOOR)),
        "budget_consumed_percent": decimal_text(consumed * 100),
        "remaining_bad_events": decimal_text(allowance - b),
        "remaining_budget_percent": decimal_text((1 - consumed) * 100),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slo-percent", type=target_percent, required=True,
                        help="target in percent, for example 99.9 (not 0.999)")
    parser.add_argument("--total", type=nonnegative_count, required=True,
                        help="eligible events in the stated evaluation interval")
    parser.add_argument("--bad", type=nonnegative_count, required=True,
                        help="bad events in that same interval and population")
    parser.add_argument("--window-total", type=nonnegative_count,
                        help="optional eligible events in a shorter comparison window")
    parser.add_argument("--window-bad", type=nonnegative_count,
                        help="bad events in that same comparison window")
    args = parser.parse_args()
    if args.bad > args.total:
        parser.error("--bad cannot exceed --total")
    if (args.window_total is None) != (args.window_bad is None):
        parser.error("supply --window-total and --window-bad together")
    if args.window_total is not None and args.window_bad > args.window_total:
        parser.error("--window-bad cannot exceed --window-total")
    if args.window_total is not None:
        if args.window_total > args.total or args.window_bad > args.bad:
            parser.error("comparison window counts must be a subset of the evaluation counts")
        if args.window_total - args.window_bad > args.total - args.bad:
            parser.error("comparison window good events exceed evaluation good events")

    with localcontext() as ctx:
        ctx.prec = max(50, len(str(args.total)) + 40)
        target = args.slo_percent / 100
        result = {
            "schema_version": 1,
            "measurement_kind": "event_ratio",
            "slo_percent": decimal_text(args.slo_percent),
            "evaluation": evaluate(args.total, args.bad, target),
            "notes": [
                "Decimal results are serialized as strings; repeating ratios use decimal precision.",
                "Counts must use the same eligibility, retry and deduplication definition.",
                "Budget allowance uses the supplied evaluation count, not forecast future traffic.",
                "Negative remaining budget means the objective was missed for these observations.",
                "No downtime conversion, alert decision or exhaustion-time forecast is implied.",
            ],
        }
        if args.window_total is not None:
            burn = None
            if args.window_total:
                burn = ((Decimal(args.window_bad) / Decimal(args.window_total))
                        / (1 - target))
            result["comparison_window"] = {
                "eligible_events": args.window_total,
                "bad_events": args.window_bad,
                "status": "measured" if args.window_total else "no_data",
                "burn_rate": decimal_text(burn),
            }
        if args.total == 0 or args.window_total == 0:
            result["notes"].append("A no-data interval does not establish success or failure.")
        print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
