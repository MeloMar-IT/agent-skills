import csv
import sys


def export(rows, out):
    w = csv.writer(out)
    for r in rows:
        w.writerow(r)


if __name__ == "__main__":
    export([["a", 1], ["b", 2]], sys.stdout)
