import json
import sys

MARGIN = 0.001


def route_verdict(ce, cn, ke, kn):
    return "PASS" if ce / cn <= (ke / kn) * 1.1 else "FAIL"


def release_verdict(metrics):
    out = []
    for r in metrics["routes"].values():
        c, k = r["canary"], r["control"]
        out.append(route_verdict(c["errors"], c["requests"], k["errors"], k["requests"]))
    return "FAIL" if "FAIL" in out else "PASS"


if __name__ == "__main__":
    print(release_verdict(json.load(open(sys.argv[1]))))
