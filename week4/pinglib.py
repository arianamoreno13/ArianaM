#!/usr/bin/env python3

import subprocess
import re
import sys

def pingthis(ipordns):
    try:
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "1000", ipordns],  # Windows syntax
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            return [ipordns, 'NotFound']

        # Use regex to find "time=XXms" or "time<1ms"
        match = re.search(r'time[=<]\s*(\d+)', result.stdout.lower())
        if match:
            return [ipordns, f"{match.group(1)}"]
        else:
            return [ipordns, 'NotFound']
    except Exception:
        return [ipordns, 'NotFound']

def main():
    if len(sys.argv) != 2:
        print("Usage: pinglib.py <IP | Domainname>")
        sys.exit(1)

    target = sys.argv[1]
    result = pingthis(target)

    print("IP, TimeToPing(ms)")
    print(f"{result[0]},{result[1]}")

if __name__ == "__main__":
    main()

