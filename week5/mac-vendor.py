mac-vendor.py                             
#!/usr/bin/env python3
import sys
import re
import requests
import csv

if len(sys.argv) != 3:
    print("Usage: mac-vendor.py <IPs.txt> <dhcpd.log>")
    sys.exit(1)

ip_list = [line.strip() for line in open(sys.argv[1]) if line.strip()]
pattern = re.compile(r"DHCPACK on (\d+\.\d+\.\d+\.\d+) to ([0-9a-fA-F:]+)")
ip_mac_map = {}

with open(sys.argv[2]) as f:
    for line in f:
        match = pattern.search(line)
        if match:
            ip, mac = match.group(1), match.group(2).lower()
            if ip in ip_list:
                ip_mac_map[ip] = mac

with open("mac-vendor.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['IP', 'Mac Address', 'Vendor'])
    for ip, mac in ip_mac_map.items():
        try:
            resp = requests.get(f"https://api.macvendors.com/{mac}", timeou>            vendor = resp.text.strip()
            if vendor.startswith("{"):
                vendor = "Unknown"
        except:
            vendor = "Unknown"
        writer.writerow([ip, mac, vendor])
