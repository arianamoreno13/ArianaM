#!/usr/bin/env python3

import sys
import os
import csv
import pinglib

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: pingcsv.py <filename | IP | Domainname> [output_filename]")
        sys.exit(1)

    input_arg = sys.argv[1]
    output_filename = sys.argv[2] if len(sys.argv) == 3 else None

    # Determine if input is file or single IP/domain
    if os.path.isfile(input_arg):
        results = ping_file(input_arg)
    else:
        results = ping_single(input_arg)

    # If output filename provided, write to CSV
    if output_filename:
        write_csv(results, output_filename)

def ping_single(ip_or_domain):
    result = pinglib.pingthis(ip_or_domain)
    print("IP, TimeToPing (ms)")
    print(f"{result[0]}, {result[1]}")
    return [result]

def ping_file(filename):
    results = []
    try:
        with open(filename, 'r') as f:
            print("IP, TimeToPing (ms)")
            for line in f:
                ip_or_domain = line.strip()
                if ip_or_domain:
                    result = pinglib.pingthis(ip_or_domain)
                    print(f"{result[0]}, {result[1]}")
                    results.append(result)
    except Exception as e:
        print(f"Error reading file: {e}")
    return results

def write_csv(results, output_filename):
    try:
        with open(output_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["IP", "TimeToPing (ms)"])
            writer.writerows(results)
        print(f"\nResults written to {output_filename}")
    except Exception as e:
        print(f"Error writing CSV: {e}")

if __name__ == "__main__":
    main()

