#!/usr/bin/env python3
import sys
import csv
import nmap

def main():
    if len(sys.argv) != 3:
        print("Usage: sudo ./osdiscover.py <input_csv_file> <output_csv_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(input_file, newline='') as infile, open(output_file, mode='w', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            writer.writerow(['IP', 'Open Ports', 'OS'])

            next(reader)
            for row in reader:
                ip = row[0]
                ports = row[1] if len(row) > 1 else ''
                os_name = detect_os(ip)
                writer.writerow([ip, ports, os_name])
                print(f"Scanned {ip}: OS = {os_name}")

    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def detect_os(ip):
    scanner = nmap.PortScanner()
    try:
        scanner.scan(ip, arguments='-O')
        if 'osmatch' in scanner[ip]:
            os_matches = scanner[ip]['osmatch']
            if os_matches:
                return os_matches[0]['name']
        return "Unknown"
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    main()
