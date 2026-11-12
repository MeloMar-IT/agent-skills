from flagclient import is_on


def price(t):
    if is_on("new-pricing"):
        return round(t * 0.95, 2)
    return t
