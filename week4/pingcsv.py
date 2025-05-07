#!/usr/bin/env python3
import os
import sys
import csv
import pinglib

def is_file(path):
    return os.path.isfile(path)

def ping_targets(input_target):
    results = []
    if is_file(input_target):
        with open(input_target, 'r') as file:
            for line in file:
                ip_or_domain = line.strip()
                result = pinglib.pingthis(ip_or_domain)
                results.append(result)
    else:
        result = pinglib.pingthis(input_target)
        results.append(result)
    return results

def write_to_csv(results, output_filename):
    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["IP", "TimeToPing (ms)"])
        for result in results:
            writer.writerow(result)

def main():
    if len(sys.argv) < 2:
        print("Usage: pingcsv.py <filename | IP | Domainname> [output_filename]")
        sys.exit(1)

    input_target = sys.argv[1]
    output_filename = sys.argv[2] if len(sys.argv) == 3 else None

    results = ping_targets(input_target)

    print("IP, TimeToPing (ms)")
    for result in results:
        print(f"{result[0]},{result[1]}")

    if output_filename:
        write_to_csv(results, output_filename)

if __name__ == "__main__":
    main()

