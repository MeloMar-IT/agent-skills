import argparse
import sys

F = {
    ("km", "mi"): 0.621371,
    ("mi", "km"): 1.609344,
    ("km", "m"): 1000.0,
    ("m", "km"): 0.001,
    ("mi", "m"): 1609.344,
    ("m", "mi"): 0.000621371,
}


def convert(v, s, d):
    return round(v * F[(s, d)], 6)


argv = sys.argv[1:]
p = argparse.ArgumentParser()
p.add_argument("value", type=float)
p.add_argument("src")
p.add_argument("dst")
a = p.parse_args(argv)
print(convert(a.value, a.src, a.dst))
