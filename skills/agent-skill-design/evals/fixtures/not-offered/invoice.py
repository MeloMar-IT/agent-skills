"""Tiny invoice calculator."""


def total(items):
    return sum(qty * price for qty, price in items)


def render(items):
    return "Total: %.2f" % total(items)


if __name__ == "__main__":
    print(render([(2, 9.5), (1, 20.0)]))
