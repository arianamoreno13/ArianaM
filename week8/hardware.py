#!/usr/bin/env python3
import os
import sys
import sqlcipher3
from datetime import datetime
import shutil
import psutil
import socket

DB_NAME = "monitor.db"
TABLE_NAME = "hardware"
DB_KEY = "mysecret123"

# Get system hostname
hostname = socket.gethostname()

def connect_db():
    conn = sqlcipher3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA key = '{DB_KEY}';")
    return conn, cursor

def get_alert_levels():
    conn, cursor = connect_db()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            cpuload_alert REAL DEFAULT -1,
            memory_alert INTEGER DEFAULT -1,
            diskfree_alert REAL DEFAULT -1
        );
    """)
    conn.commit()

    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME};")
    if cursor.fetchone()[0] == 0:
        cursor.execute(f"""
            INSERT INTO {TABLE_NAME} (cpuload_alert, memory_alert, diskfree_alert)
            VALUES (2.0, 500, 2.0);
        """)
        conn.commit()

    cursor.execute(f"SELECT cpuload_alert, memory_alert, diskfree_alert FROM {TABLE_NAME} LIMIT 1;")
    row = cursor.fetchone()
    conn.close()
    return row

def set_alert(cmd, value):
    conn, cursor = connect_db()
    column = {
        "cpu-alert": "cpuload_alert",
        "memory-alert": "memory_alert",
        "diskfree-alert": "diskfree_alert"
    }[cmd]
    cursor.execute(f"UPDATE {TABLE_NAME} SET {column} = ?;", (float(value),))
    conn.commit()
    conn.close()

def log_message(message, logfile=None):
    timestamp = datetime.now().isoformat(timespec='seconds')
    log_line = f"{timestamp} {hostname}: {message}"
    if logfile:
        with open(logfile, 'a') as f:
            f.write(log_line + "\n")
    else:
        print(log_line)

def check_system(logfile=None):
    cpuload_alert, memory_alert, diskfree_alert = get_alert_levels()

    # CPU
    cpu_1m_load = os.getloadavg()[0]
    if cpuload_alert != -1 and cpu_1m_load > cpuload_alert:
        log_message(f"ERROR: cpu 1m load of {cpu_1m_load:.2f} is above alert level of {cpuload_alert}", logfile)
    else:
        log_message(f"OK: cpu 1m load is {cpu_1m_load:.2f}", logfile)

    # Memory
    free_memory = psutil.virtual_memory().available // (1024 * 1024)
    if memory_alert != -1 and free_memory < memory_alert:
        log_message(f"ERROR: free memory of {free_memory}MB is less than alert level of {memory_alert}MB", logfile)
    else:
        log_message(f"OK: free memory is {free_memory}MB", logfile)

    # Disk
    free_disk = shutil.disk_usage("/").free // (1024 ** 3)
    if diskfree_alert != -1 and free_disk < diskfree_alert:
        log_message(f"ERROR: disk free of {free_disk}GB is less than alert level of {diskfree_alert}GB", logfile)
    else:
        log_message(f"OK: disk free is {free_disk}GB", logfile)

def main():
    if len(sys.argv) < 2:
        print("Usage: ./hardware.py <cmd> <value|logfile>")
        return

    cmd = sys.argv[1]

    if cmd in ["cpu-alert", "memory-alert", "diskfree-alert"]:
        if len(sys.argv) != 3:
            print(f"Usage: ./hardware.py {cmd} <value>")
            return
        set_alert(cmd, sys.argv[2])

    elif cmd == "check":
        logfile = sys.argv[2] if len(sys.argv) == 3 else None
        check_system(logfile)
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
