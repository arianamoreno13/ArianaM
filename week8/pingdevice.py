#!/usr/bin/env python3
from pinglib import ping
import sys
import sqlite3
from datetime import datetime

DB_NAME = 'monitor.db'
TABLE_NAME = 'devices'

def main():
    setup_db()

    if len(sys.argv) < 2:
        print("Usage: ./pingdevice.py <add|delete|list|check> [options]")
        sys.exit(1)

    cmd = sys.argv[1].lower()

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

def setup_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(f'''
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                dns_ip TEXT PRIMARY KEY,
                warn_level INTEGER
            )
        ''')

def add_device(dns_ip, warn_level):
    try:
        warn_level = int(warn_level)
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute(f'INSERT OR REPLACE INTO {TABLE_NAME} (dns_ip, warn_level) VALUES (?, ?)', (dns_ip, warn_level))
        print(f"Added {dns_ip} with warn level {warn_level}ms.")
    except ValueError:
        print("Warning level must be an integer.")

def delete_device(dns_ip):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(f'DELETE FROM {TABLE_NAME} WHERE dns_ip = ?', (dns_ip,))
    print(f"Deleted {dns_ip} if it existed.")

def list_devices():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute(f'SELECT * FROM {TABLE_NAME}')
        rows = cursor.fetchall()
        if rows:
            for dns_ip, warn_level in rows:
                print(f"{dns_ip} - Warn Level: {warn_level}ms")
        else:
            print("No devices found.")

def log_message(level, message, logfile=None):
    timestamp = datetime.now().isoformat(timespec='seconds')
    output = f"{timestamp} mido: {level}: {message}"
    if logfile:
        try:
            with open(logfile, 'a') as f:
                f.write(output + '\n')
        except Exception as e:
            print(f"Failed to write log: {e}")
    else:
        print(output)

def check_devices(logfile=None):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute(f'SELECT * FROM {TABLE_NAME}')
        for dns_ip, warn_level in cursor.fetchall():
            result = ping(dns_ip)
            if result is None:
                log_message("ERROR", f"Device {dns_ip} is down", logfile)
            elif result > warn_level:
                log_message("WARNING", f"Device {dns_ip} ping time is {result}ms, warn level set to {warn_level}ms", logfile)
            else:
                log_message("OK", f"Device {dns_ip} ping time is {result}ms", logfile)

if __name__ == "__main__":
    main()

