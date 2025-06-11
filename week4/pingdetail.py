#!/usr/bin/env python3
import sys
import os
import csv
from pinglib import pingthis

def process_targets(targets):
    results = []
    for target in targets:
        target = target.strip()
        if target:
            results.append(pingthis(target))
    return results

def main():
    argc = len(sys.argv)
    if argc < 2 or argc > 3:
        print("Usage: pingdetail.py <filename | IP | Domainname> [outputfile]")
        sys.exit(1)

    input_arg = sys.argv[1]
    output_file = sys.argv[2] if argc == 3 else None

    # Determine if input_arg is a file
    if os.path.isfile(input_arg):
        with open(input_arg, 'r') as f:
            targets = f.readlines()
    else:
        targets = [input_arg]

    results = process_targets(targets)

    # Print header
    header = ['Pinged IP/Name', 'DNS', 'IP', 'TimeToPing (ms)']
    print(', '.join(header))

    # Print all results to screen
    for row in results:
        print(', '.join(row))

    # If output file provided, write CSV
    if output_file:
        try:
            with open(output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(header)
                writer.writerows(results)
        except Exception as e:
            print(f"Error writing to file {output_file}: {e}")

if __name__ == "__main__":
    main()
