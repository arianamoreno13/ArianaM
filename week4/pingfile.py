#!/usr/bin/env python3

import os
import sys
import pinglib

def ping_from_file(filename):
    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    print("IP, TimeToPing (ms)")

    with open(filename, 'r') as file:
        for line in file:
            target = line.strip()
            if target:  # skip blank lines
                result = pinglib.pingthis(target)
                print(f"{result[0]},{result[1]}")

def main():
    if len(sys.argv) != 2:
        print("Usage: pingfile.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    ping_from_file(filename)

if __name__ == "__main__":
    main()
