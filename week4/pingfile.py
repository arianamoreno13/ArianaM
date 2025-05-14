#!/usr/bin/env python3

import sys
import os
import pinglib

def main():
    if len(sys.argv) != 2:
        print("Usage: pingfile.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' not found in current directory.")
        sys.exit(1)

    print("IP, TimeToPing (ms)")

    with open(filename, 'r') as f:
        for line in f:
            ip_or_domain = line.strip()
            if ip_or_domain:
                result = pinglib.pingthis(ip_or_domain)
                print(f"{result[0]}, {result[1]}")

if __name__ == "__main__":
    main()

