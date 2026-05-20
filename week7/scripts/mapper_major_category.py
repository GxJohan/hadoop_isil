#!/usr/bin/env python3
"""Emit one count per Major_Category from ai_student_impact_dataset.csv."""

import csv
import sys


def main() -> None:
    reader = csv.reader(sys.stdin)

    for row in reader:
        if not row or len(row) < 2:
            continue

        if row[0] == "Student_ID":
            continue

        major_category = row[1].strip()
        if major_category:
            print("{}\t1".format(major_category))


if __name__ == "__main__":
    main()
