#!/usr/bin/env python3
import os
import sys
import csv
import pinglib

def ping_target(target):
    result = pinglib.pingthis(target)
    print(f"{result[0]},{result[1]}")
    return result

def ping_from_file(filename):
    results = []
    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    with open(filename, 'r') as file:
        for line in file:
            target = line.strip()
            if target:
                result = ping_target(target)
                results.append(result)
    return results

def write_csv(results, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["IP", "TimeToPing (ms)"])
        writer.writerows(results)

def main():
    if len(sys.argv) < 2:
        print("Usage: pingcsv.py <filename | IP | Domainname> [output_filename.csv]")
        sys.exit(1)

    input_arg = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) == 3 else None

    print("IP, TimeToPing (ms)")

    # Determine if input_arg is a file or a single IP/Domain
    if os.path.isfile(input_arg):
        results = ping_from_file(input_arg)
    else:
        results = [ping_target(input_arg)]

    if output_file:
        write_csv(results, output_file)

if __name__ == "__main__":
    main()

