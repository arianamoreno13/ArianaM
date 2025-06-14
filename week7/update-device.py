#!/usr/bin/env python3
import sqlcipher3
import serverinfo

import sys
sys.path.append('/git/ArianaM/week3/serverinfo.py')

# Constants
database = 'etest.db'
password = 'mysecret123'
table = 'devices'

def main():
    # Get system info from serverinfo.py
    name = serverinfo.get_name()
    os = serverinfo.get_os()
    uptime = serverinfo.get_uptime()
    cpu = serverinfo.get_cpu()
    memory = serverinfo.get_memory()

    # Connect to encrypted database
    conn = sqlcipher3.connect(database)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA key='{password}';")

    # Optional: Create table if it doesn't exist
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table} (
            name TEXT PRIMARY KEY,
            os TEXT,
            uptime TEXT,
            cpu TEXT,
            memory TEXT
        );
    ''')

    # Insert or replace the device info
    try:
        cursor.execute(f'''
            INSERT OR REPLACE INTO {table} (name, os, uptime, cpu, memory)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, os, uptime, cpu, memory))
        conn.commit()
        print(f"Device '{name}' updated successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()

