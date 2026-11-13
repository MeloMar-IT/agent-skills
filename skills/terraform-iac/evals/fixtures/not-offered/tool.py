import os
import sys

d = sys.argv[1]
for name in os.listdir(d):
    if name.endswith(".tmp"):
        os.remove(os.path.join(d, name))
