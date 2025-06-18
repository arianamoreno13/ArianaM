#!/usr/bin/env python3
import sys
import subprocess
import re
import subprocess
import platform

def main():
    if len(sys.argv) != 2:
        print("Usage: pinglib.py <IP or Domainname>")
        sys.exit(1)

    ipordns = sys.argv[1]
    ping_time = ping(ipordns)
    if ping_time is not None:
        print(f"{ipordns} responded in {ping_time} ms")
    else:
        print(f"{ipordns} is unreachable")

def ping(ipordns):
    try:
        result = subprocess.run(
            ['ping', '-c', '1', ipordns],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            #return [ipordns, 'NotFound']
            return None

        #match = re.search(r'time[=<](\d+\.?\d*)\s*ms', result.stdout)
        match = re.search(r'time[=<]\s*(\d+\.?\d*)\s*ms', result.stdout)
        if match:
            time_ms = round(float(match.group(1)), 2)
            #return [ipordns, str(time_ms)]
            return time_ms
        else:
            return None
            #return [ipordns, 'NotFound']

    except Exception as e:
        #return [ipordns, 'NotFound']
        return None

#def main():
    #if len(sys.argv) != 2:
        #print("Usage: pinglib.py <IP | Domainname>")
        #sys.exit(1)

    #ipordns = sys.argv[1]
    #result = pingthis(ipordns)
    #print("IP, TimeToPing(ms)")
    #print(f"{result[0]},{result[1]}")

if __name__ == "__main__":
    main()

