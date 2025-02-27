#!/bin/python3
"""modify a bank statement, adding or subtracting a value from a column to/from a specific row
useful when money is somewhere else (like an Easy Saver) but otherwise still exists and wants to be on the graph
"""

import sys
import csv

if len(sys.argv) < 4:
    print("must specify file, how much to add/remove, and what row to begin/end")
    print('use: ./modify.sh file.csv "4000" 992 9999')
    sys.exit(1)

file = sys.argv[1]
add = sys.argv[2]
from_ = int(sys.argv[3])
to = int(sys.argv[4])

print(f"adding {add} to lines {from_}-{to} in {file}", file=sys.stderr)

with open(file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    lines = list(reader)

new_lines = []
for i, line in enumerate(lines):
    if from_ <= i < to:
        line["Balance (GBP)"] = round(float(line["Balance (GBP)"]) + float(add), 2)
    new_lines.append(line)

with open(file, "w", encoding="utf-8") as f:
    reader = csv.DictWriter(f, fieldnames)
    reader.writeheader()
    reader.writerows(new_lines)

print("done!", file=sys.stderr)
