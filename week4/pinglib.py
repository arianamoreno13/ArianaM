#!/usr/bin/env python3
import subprocess
import socket
import time

def pingthis(ipordns):
    try:
        # Try resolving to IP
        try:
            resolved_ip = socket.gethostbyname(ipordns)
        except Exception:
            resolved_ip = "Unknown"

        # Try reverse DNS (if it's an IP)
        try:
            resolved_dns = socket.gethostbyaddr(ipordns)[0]
        except Exception:
            resolved_dns = "Unknown"

        # Start ping timer
        start = time.time()
        result = subprocess.run(
            ['ping', '-c', '1', ipordns],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        end = time.time()

        if result.returncode == 0:
            ping_time = f"{(end - start):.3f}"
        else:
            ping_time = "Not Found"

        return [ipordns, resolved_dns, resolved_ip, ping_time]

    except Exception as e:
        return [ipordns, "Unknown", "Unknown", "Not Found"]


