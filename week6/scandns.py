#!/usr/bin/env python3
import sys
import csv
import nmap3

def main():
    if len(sys.argv) != 3:
        print("Usage: ./scandns.py <domainname> <outputfile>")
        sys.exit(1)

    domain = sys.argv[1]
    outputfile = sys.argv[2]

    try:
        nmap = nmap3.Nmap()
        print(f"Running DNS brute-force scan on {domain}...")

        result = nmap.nmap_dns_brute_script(domain)

        if not result:
            print("No results found.")
            sys.exit(1)

        with open(outputfile, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["DNS", "IP"])

            for entry in result:
                hostname = entry.get("hostname")
                addresses = entry.get("address", [])

                # Skip IPv6 addresses and entries without valid hostname
                if hostname and addresses:
                    ipv4_addresses = [addr for addr in addresses if ":" not in addr]
                    for ip in ipv4_addresses:
                        writer.writerow([hostname, ip])

        print(f"Scan complete. Results saved to {outputfile}")

    except Exception as e:
        print(f"Error during DNS scan: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
