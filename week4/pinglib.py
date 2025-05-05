#!/usr/bin/env python3

import sys
import subprocess
import re

def pingthis(ipordns):
    try:
        # Run a single ping, capture output
        result = subprocess.run(['ping', '-c', '1', ipordns], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            return [ipordns, 'NotFound']

        # Extract time from ping output using regex
        match = re.search(r'time=([\d.]+)', result.stdout)
        if match:
            ping_time = round(float(match.group(1)), 2)
            return [ipordns, str(ping_time)]
        else:
            return [ipordns, 'NotFound']
    except Exception:
        return [ipordns, 'NotFound']

def main():
    if len(sys.argv) != 2:
        print("Usage: pinglib.py <IP | DomainName>")
        sys.exit(1)

    ipordns = sys.argv[1]
    result = pingthis(ipordns)
    print("IP, TimeToPing(ms)")
    print(f"{result[0]},{result[1]}")

if __name__ == "__main__":
    main()
