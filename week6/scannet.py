#!/usr/bin/env python3
import sys
import csv
import nmap3
#from nmap import PortScanner
#from nmap.nmap import NmapScanTechniques

def main():
    if len(sys.argv) != 3:
        print("Usage: sudo ./scannet.py <subnet> <outputfile>")
        sys.exit(1)

    subnet = sys.argv[1]
    outputfile = sys.argv[2]

    try:
        scanner = nmap3.NmapScanTechniques()
        print(f"Scanning subnet {subnet} with SYN scan. This may take a few minutes...")

        result = scanner.nmap_syn_scan(subnet)

        if not result:
            print("No scan results found.")
            sys.exit(1)

        with open(outputfile, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["IP", "Open Ports"])

            for ip, data in result.items():
                open_ports = []

                if data['state']['state']=='up':
                    for port_data in data['ports']:
                        if port_data['state'] == 'open':
                            open_ports.append(str(port_data['portid']))

                if open_ports:
                    writer.writerow([ip, ' '.join(open_ports)])

        print(f"Scan complete. Results saved to {outputfile}")

    except Exception as e:
        print(f"Error during scanning: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
