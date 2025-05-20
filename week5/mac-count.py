#!/usr/bin/env python3
import sys
import re
import csv
from collections import defaultdict

if len(sys.argv) != 2:
    print("Usage: mac-count.py <filename>")
    sys.exit(1)

filename = sys.argv[1]
pattern = re.compile(r"DHCPACK on (\d+\.\d+\.\d+\.\d+) to ([0-9a-fA-F:]+)")

# Dictionary to track counts with (MAC, IP) as key
ack_counts = defaultdict(int)

with open(filename, 'r') as file:
    for line in file:
        match = pattern.search(line)
        if match:
            ip = match.group(1)
            mac = match.group(2).lower()
            ack_counts[(mac, ip)] += 1

# Write to mac-count.csv
with open("mac-count.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Macs', 'IPs', 'ACKs'])
    for (mac, ip), count in ack_counts.items():
        writer.writerow([mac, ip, count])

# Identify top 2 offenders
top_offenders = sorted(ack_counts.items(), key=lambda x: x[1], reverse=True)[:2]

# Write to problem-macs.csv
with open("problem-macs.csv", 'w', newline='') as probfile:
    writer = csv.writer(probfile)
    writer.writerow(['Macs', 'IPs', 'ACKs'])
    for (mac, ip), count in top_offenders:
        writer.writerow([mac, ip, count])
