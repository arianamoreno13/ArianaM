#!/usr/bin/env python3

import sys
import os
import pinglib

def main():
    if len(sys.argv) != 2:
        print("Usage: pingany.py <filename | IP | Domainname>")
        sys.exit(1)

    input_arg = sys.argv[1]

    if os.path.isfile(input_arg):
        ping_file(input_arg)
    else:
        ping_single(input_arg)

def ping_single(ip_or_domain):
    result = pinglib.pingthis(ip_or_domain)
    print("IP, TimeToPing (ms)")
    print(f"{result[0]}, {result[1]}")

def ping_file(filename):
    try:
        with open(filename, 'r') as f:
            print("IP, TimeToPing (ms)")
            for line in f:
                ip_or_domain = line.strip()
                if ip_or_domain:
                    result = pinglib.pingthis(ip_or_domain)
                    print(f"{result[0]}, {result[1]}")
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    main()

