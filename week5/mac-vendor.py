#!/usr/bin/env python3
import sys
import re
import requests
import csv

if len(sys.argv) != 3:
    print("Usage: mac-vendor.py <IPs.txt> <dhcpd.log>")
    sys.exit(1)

ips_file = sys.argv[1]
log_file = sys.argv[2]
pattern = re.compile(r"DHCPACK on (\d+\.\d+\.\d+\.\d+) to ([0-9a-fA-F:]+)")

#Load IPs from IPs.txt
with open(ips_file, 'r') as f:
    ip_list = [line.strip() for line in f if line.strip()]

#Parse log file for matching IPs and extract MACs
ip_mac_map = {}

with open(log_file, 'r') as f:
    for line in f:
        match = pattern.search(line)
        if match:
            ip = match.group(1)
            mac = match.group(2).lower()
            if ip in ip_list:
                ip_mac_map[ip] = mac

#Query MAC Vendors API
results = []

for ip, mac in ip_mac_map.items():
    try:
        response = requests.get(f"https://api.macvendors.com/{mac}")
        vendor = response.text.strip()
    except Exception as e:
        vendor = "Unknown"
    results.append((ip, mac, vendor))

#Write to mac-vendor.csv
with open("mac-vendor.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['IP', 'Mac Address', 'Vendor'])
    for row in results:
        writer.writerow(row)
