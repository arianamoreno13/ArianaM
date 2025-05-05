#!/usr/bin/env python3

import sys
import csv
import json
import serverinfo  # Make sure serverinfo.py is in the same directory

def gather_info():
    return {
        "Hostname": serverinfo.get_hostname(),
        "CPU (count)": serverinfo.get_cpu_count(),
        "RAM (GB)": serverinfo.get_ram_gb(),
        "OSType": serverinfo.get_os_type(),
        "OSVersion": serverinfo.get_os_version(),
        "OS disk size (GB)": serverinfo.get_disk_size_gb(),
        "OS disk free (GB)": serverinfo.get_disk_free_gb(),
        "Primary IP": serverinfo.get_primary_ip(),
        "Primary Mac": serverinfo.get_primary_mac()
    }

def output_screen(info):
    for key, value in info.items():
        print(f"{key}: {value}")

def output_csv(info, filename="serverinfo.csv"):
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Field", "Value"])
        for key, value in info.items():
            writer.writerow([key, value])

def output_json(info, filename="serverinfo.json"):
    with open(filename, "w") as jsonfile:
        json.dump(info, jsonfile, indent=4)

def main():
    if len(sys.argv) != 2:
        print("Usage: server2file.py [screen|csv|json]")
        sys.exit(1)

    output_type = sys.argv[1].lower()
    info = gather_info()

    if output_type == "screen":
        output_screen(info)
    elif output_type == "csv":
        output_csv(info)
    elif output_type == "json":
        output_json(info)
    else:
        print("Invalid argument. Use: screen, csv, or json.")
        sys.exit(1)

if __name__ == "__main__":
    main()
