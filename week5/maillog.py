#!/usr/bin/env python3

import sys
import re
import csv

def main():
    if len(sys.argv) != 2:
        print("Usage: maillog.py <mail log file>")
        sys.exit(1)

    filename = sys.argv[1]
    servers = extract_servers(filename)
    write_csv(servers)
    print("servers.csv has been created.")

def extract_servers(filename):
    # Match lines that indicate an actual connection
    pattern = re.compile(r'connect from\s+([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\[(\d{1,3}(?:\.\d{1,3}){3})\]')
    found = set()

    try:
        with open(filename, 'r') as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    server_name = match.group(1)
                    ip = match.group(2)
                    found.add((server_name, ip))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    return sorted(found)

def write_csv(servers):
    with open('servers.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Server Name', 'IP'])
        for server_name, ip in servers:
            writer.writerow([server_name, ip])

if __name__ == '__main__':
    main()
