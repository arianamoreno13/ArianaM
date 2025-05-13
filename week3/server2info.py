#!/usr/bin/python3
# Script returns information about the machine.
# Licensed under the MIT License (https://opensource.org/license/mit)
# ARI-20130930
import subprocess
import psutil
import socket
import uuid
import distro
import shutil
import platform
import json
import csv
import sys

def get_system_info():
    return {
        "Hostname": get_hostname(),
        "CPU_Count": get_cpu_count(),
        "RAM_GB": get_ram_gb(),
        "OSType": get_os_type(),
        "OSVersion": get_os_version(),
        "Disk_Total_GB": get_disk_size_gb(),
        "Disk_Free_GB": get_disk_free_gb(),
        "Primary_IP": get_primary_ip(),
        "Primary_MAC": get_primary_mac(),
    }

def get_hostname():
    return socket.gethostname()

def get_cpu_count():
    return psutil.cpu_count(logical=True)

def get_ram_gb():
    return round(psutil.virtual_memory().total / (1024 ** 3))

def get_os_type():
    return platform.system()

def get_os_version():
    return distro.name() + " " + distro.version()

def get_disk_size_gb():
    total, _, _ = shutil.disk_usage("/")
    return round(total / (1024 ** 3))

def get_disk_free_gb():
    _, _, free = shutil.disk_usage("/")
    return round(free / (1024 ** 3))

def get_primary_ip():
    return socket.gethostbyname(socket.gethostname())

def get_primary_mac():
    mac_num = hex(uuid.getnode()).replace('0x', '').zfill(12)
    return ':'.join(mac_num[i:i+2] for i in range(0, 12, 2))

def output_screen(info):
    for key, value in info.items():
        print(f"{key}: {value}")

def output_csv(info, filename="serverinfo.csv"):
    with open(filename, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(info.keys())
        writer.writerow(info.values())

def output_json(info, filename="serverinfo.json"):
    with open(filename, mode="w") as file:
        json.dump(info, file, indent=4)

def main():
    if len(sys.argv) != 2:
        print("Usage: python server2file.py [screen|csv|json]")
        sys.exit(1)

    output_type = sys.argv[1].lower()
    info = get_system_info()

    if output_type == "screen":
        output_screen(info)
    elif output_type == "csv":
        output_csv(info)
    elif output_type == "json":
        output_json(info)
    else:
        print("Invalid argument. Use 'screen', 'csv', or 'json'.")
        sys.exit(1)

if __name__ == "__main__":
    main()

