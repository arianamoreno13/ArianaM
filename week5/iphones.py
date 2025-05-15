#!/usr/bin/env python3

import sys
import re

def main():
    if len(sys.argv) != 2:
        print("Usage: iphones.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    iphone_macs = set()

    try:
        with open(filename, 'r') as file:
            for line in file:
                # Check if it's a DHCPACK line and mentions iPhone
                if "DHCPACK" in line and re.search(r"iPhone", line, re.IGNORECASE):
                    # Find the MAC address using regex
                    mac_match = re.search(r'([0-9A-Fa-f]{2}[:\-]){5}([0-9A-Fa-f]{2})', line)
                    if mac_match:
                        iphone_macs.add(mac_match.group(0).lower())

        for mac in iphone_macs:
            print(mac)
        print(f"Count = {len(iphone_macs)}")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
