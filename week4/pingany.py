#!/usr/bin/env python3
import os
import sys
import pinglib

def ping_from_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.read().splitlines()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    print("IP, TimeToPing (ms)")
    for line in lines:
        line = line.strip()
        if line:
            result = ping(line)
            print(f"{line}, {result}")

def ping_single_target(target):
    print("IP, TimeToPing (ms)")
    result = ping(target)
    print(f"{target}, {result}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python pingany.py <filename | IP | Domainname>")
        sys.exit(1)

    arg = sys.argv[1]

    if os.path.isfile(arg):
        ping_from_file(arg)
    else:
        ping_single_target(arg)

if __name__ == "__main__":
    main()

