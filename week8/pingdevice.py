#!/usr/bin/env python3
import sys
import sqlcipher3
import socket
from datetime import datetime
from pinglib import ping

DB_NAME = 'monitor.db'
TABLE_NAME = 'devices'
DB_KEY = "mysecret123"

hostname = socket.gethostname()

def main():
    setup_db()

    if len(sys.argv) < 2:
        print("Usage: ./pingdevice.py <add|delete|list|check> [options]")
        return

    cmd = sys.argv[1]

    if cmd == "add" and len(sys.argv) == 4:
        add_device(sys.argv[2], sys.argv[3])
    elif cmd == "delete" and len(sys.argv) == 3:
        delete_device(sys.argv[2])
    elif cmd == "list":
        list_devices()
    elif cmd == "check":
        logfile = sys.argv[2] if len(sys.argv) == 3 else None
        check_devices(logfile)
    else:
        print("Invalid command or missing arguments.")

def connect_db():
    conn = sqlcipher3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA key = '{DB_KEY}';")
    return conn, cursor

def setup_table():
    conn, cursor = connect_db()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            dns_ip TEXT NOT NULL,
            warn_level INTEGER NOT NULL
        );
    """)
    conn.commit()
    conn.close()

def add_device(ip, warn_ms):
    conn, cursor = connect_db()
    cursor.execute(f"INSERT INTO {TABLE_NAME} (dns_ip, warn_level) VALUES (?, ?);", (ip, int(warn_ms)))
    conn.commit()
    conn.close()

def delete_device(ip):
    conn, cursor = connect_db()
    cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE dns_ip = ?;", (ip,))
    conn.commit()
    conn.close()

def list_devices():
    conn, cursor = connect_db()
    cursor.execute(f"SELECT dns_ip, warn_level FROM {TABLE_NAME};")
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        print(f"{row[0]} (warn level: {row[1]}ms)")

def log_message(message, logfile=None):
    timestamp = datetime.now().isoformat(timespec='seconds')
    line = f"{timestamp} {hostname}: {message}"
    if logfile:
        with open(logfile, 'a') as f:
            f.write(line + "\n")
    else:
        print(line)

def check_devices(logfile=None):
    conn, cursor = connect_db()
    cursor.execute(f"SELECT dns_ip, warn_level FROM {TABLE_NAME};")
    devices = cursor.fetchall()
    conn.close()

    for ip, warn_ms in devices:
        success, ping_time = ping(ip)
        if not success:
            log_message(f"ERROR: Device {ip} is down", logfile)
        elif ping_time > warn_ms:
            log_message(f"WARNING: Device {ip} ping time is {ping_time}ms, warn level set to {warn_ms}ms", logfile)
        else:
            log_message(f"OK: Device {ip} ping time is {ping_time}ms", logfile)

if __name__ == "__main__":
    main()

