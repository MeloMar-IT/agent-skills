import csv

rows = list(csv.DictReader(open("data.csv")))
print(len(rows))
print(sum(float(r["amount"]) for r in rows))
