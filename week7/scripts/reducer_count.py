#!/usr/bin/env python3
"""Sum counts for Hadoop Streaming key/value pairs."""

import sys


def main() -> None:
    current_key = None
    current_total = 0

    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue

        try:
            key, value = line.split("\t", 1)
            count = int(value)
        except ValueError:
            continue

        if key == current_key:
            current_total += count
        else:
            if current_key is not None:
                print("{}\t{}".format(current_key, current_total))
            current_key = key
            current_total = count

    if current_key is not None:
        print("{}\t{}".format(current_key, current_total))


if __name__ == "__main__":
    main()
