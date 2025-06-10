#!/usr/bin/env python3
import sys
import sqlite3
from datetime import datetime
from pinglib import ping  # Week 4 assignment
import os

DB_NAME = 'monitor.db'
TABLE_NAME = 'devices'

def setup_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            dns_ip TEXT PRIMARY KEY,
            warn_level INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def add_device(ip_or_dns, warn_level):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute(f'INSERT INTO {TABLE_NAME} (dns_ip, warn_level) VALUES (?, ?)', (ip_or_dns, int(warn_level)))
        conn.commit()
        print(f"Added {ip_or_dns} with warn level {warn_level}ms.")
    except sqlite3.IntegrityError:
        print(f"Device {ip_or_dns} already exists.")
    conn.close()

def delete_device(ip_or_dns):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f'DELETE FROM {TABLE_NAME} WHERE dns_ip = ?', (ip_or_dns,))
    conn.commit()
    print(f"Deleted {ip_or_dns} if it existed.")
    conn.close()

def list_devices():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f'SELECT * FROM {TABLE_NAME}')
    rows = c.fetchall()
    if rows:
        for row in rows:
            print(f"{row[0]} - Warn Level: {row[1]}ms")
    else:
        print("No devices found.")
    conn.close()

def log_message(status, message, logfile=None):
    timestamp = datetime.now().isoformat(timespec='seconds')
    full_message = f"{timestamp} mido: {status}: {message}"
    if logfile:
        try:
            with open(logfile, 'a') as f:
                f.write(full_message + "\n")
        except Exception as e:
            print(f"Could not write to log: {e}")
    else:
        print(full_message)

def check_devices(logfile=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f'SELECT * FROM {TABLE_NAME}')
    devices = c.fetchall()
    conn.close()

    for device, warn_level in devices:
        result = ping(device)

        if result is None:
            log_message("ERROR", f"Device {device} is down", logfile)
        elif result > warn_level:
            log_message("WARNING", f"Device {device} ping time is {result}ms, warn level set to {warn_level}ms", logfile)
        else:
            log_message("OK", f"Device {device} ping time is {result}ms", logfile)

def main():
    setup_db()

    if len(sys.argv) < 2:
        print("Usage: ./pingdevice.py <add|delete|list|check> [options]")
        sys.exit(1)

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

if __name__ == "__main__":
    main()
