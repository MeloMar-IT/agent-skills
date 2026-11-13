import csv
from collections import defaultdict

totals = defaultdict(float)
with open("data.csv") as fh:
    for row in csv.DictReader(fh):
        totals[row["name"]] += float(row["amount"])
for name, total in sorted(totals.items()):
    print(name, total)
