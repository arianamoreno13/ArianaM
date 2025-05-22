#!/usr/bin/env python3

import sys
import re
from collections import defaultdict

def main():
    if len(sys.argv) != 2:
        print("Usage: authlog.py <auth.log file>")
        sys.exit(1)

    filename = sys.argv[1]
    ip_counts = extract_failed_ips(filename)

# Sort IPs by number of failed attempts, descending
    sorted_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)

    for ip, count in sorted_ips:
        print(f"{ip}, {count}")

def extract_failed_ips(filename):
# Common failure messages include: "Failed password", "Invalid user", etc.
    fail_patterns = [
        r'Failed password.*from (\b\d{1,3}(?:\.\d{1,3}){3}\b)',
        r'Invalid user .* from (\b\d{1,3}(?:\.\d{1,3}){3}\b)',
        r'authentication failure.*rhost=(\b\d{1,3}(?:\.\d{1,3}){3}\b)',
        r'Failed publickey.*from (\b\d{1,3}(?:\.\d{1,3}){3}\b)'
    ]

    ip_counts = defaultdict(int)

    try:
# Avoid double-counting the same line
        with open(filename, 'r') as f:
            for line in f:
                for pattern in fail_patterns:
                    match = re.search(pattern, line)
                    if match:
                        ip = match.group(1)
                        ip_counts[ip] += 1
                        break
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    return ip_counts

if __name__ == '__main__':
    main()
