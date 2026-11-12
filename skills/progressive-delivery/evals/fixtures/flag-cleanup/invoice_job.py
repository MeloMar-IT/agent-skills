from flagclient import is_on
from pricing import price

PRICING_FLAG = "new-" + "pricing"


def footer():
    if is_on(PRICING_FLAG):
        return "Loyalty discount applied"
    return ""


def invoice_line(t):
    return f"{price(t):.2f} {footer()}".strip()
