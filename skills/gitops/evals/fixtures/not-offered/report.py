import csv
from collections import defaultdict

totals = defaultdict(float)
with open("sales.csv") as f:
    for row in csv.DictReader(f):
        totals[row["region"]] += float(row["amount"])
for region, total in sorted(totals.items()):
    print(region, total)
