#!/usr/bin/env python3
import os
import sys
import pinglib

def is_file(path):
    return os.path.isfile(path)

def process_input(target):
    print("IP, TimeToPing (ms)")
    if is_file(target):
        with open(target, 'r') as file:
            for line in file:
                ip_or_domain = line.strip()
                result = pinglib.pingthis(ip_or_domain)
                print(f"{result[0]},{result[1]}")
    else:
        result = pinglib.pingthis(target)
        print(f"{result[0]},{result[1]}")

def main():
    if len(sys.argv) != 2:
        print("Usage: pingany.py <filename | IP | Domainname>")
        sys.exit(1)

    input_target = sys.argv[1]
    process_input(input_target)

if __name__ == "__main__":
    main()
