#!/usr/bin/env python3

import sys
import subprocess
import re

def pingthis(ipordns):
    try:
        # Run ping command (1 packet, quiet output)
        result = subprocess.run(
            ['ping', '-c', '1', ipordns],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # If ping failed (host not found, etc.)
        if result.returncode != 0:
            return [ipordns, 'NotFound']

        # Search for the time=XX ms part in the output
        match = re.search(r'time[=<](\d+\.?\d*)\s*ms', result.stdout)
        if match:
            time_ms = round(float(match.group(1)), 2)
            return [ipordns, str(time_ms)]
        else:
            return [ipordns, 'NotFound']

    except Exception as e:
        return [ipordns, 'NotFound']

def main():
    if len(sys.argv) != 2:
        print("Usage: pinglib.py <IP | Domainname>")
        sys.exit(1)

    ipordns = sys.argv[1]
    result = pingthis(ipordns)
    print("IP, TimeToPing(ms)")
    print(f"{result[0]},{result[1]}")

if __name__ == "__main__":
    main()

