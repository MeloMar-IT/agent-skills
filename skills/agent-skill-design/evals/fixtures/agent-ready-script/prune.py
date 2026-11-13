import os
import sys
import time

d = sys.argv[1]
days = int(sys.argv[2])
cutoff = time.time() - days * 86400
old = []
for name in sorted(os.listdir(d)):
    p = os.path.join(d, name)
    if os.path.isfile(p) and os.path.getmtime(p) < cutoff:
        old.append(p)
for p in old:
    print("\033[33m" + p + "\033[0m")
ans = input("Delete %d files? [y/N] " % len(old))
if ans.lower() == "y":
    for p in old:
        os.remove(p)
        print("\033[31mdeleted " + p + "\033[0m")
if not os.path.isdir(d):
    print("no such dir")
sys.exit(0)
