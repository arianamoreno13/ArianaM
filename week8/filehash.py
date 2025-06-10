#!/usr/bin/env python3
import hashlib
import sqlite3
import sys
import os
from datetime import datetime

DB_NAME = "monitor.db"
TABLE_NAME = "files"

def setup_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            timestamp TEXT,
            path TEXT PRIMARY KEY,
            hash TEXT
        )
    """)
    conn.commit()
    return conn

def get_md5(filepath):
    if not os.path.isfile(filepath):
        return None
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def log_message(msg, logfile=None):
    timestamp = datetime.utcnow().isoformat()
    full_msg = f"{timestamp} mido: {msg}"
    if logfile:
        with open(logfile, "a") as f:
            f.write(full_msg + "\n")
    else:
        print(full_msg)

def update_file(conn, filepath):
    md5 = get_md5(filepath)
    if md5 is None:
        print(f"File not found: {filepath}")
        return
    timestamp = datetime.utcnow().isoformat()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE path = ?", (filepath,))
    if cursor.fetchone():
        cursor.execute(f"UPDATE {TABLE_NAME} SET timestamp = ?, hash = ? WHERE path = ?",
                       (timestamp, md5, filepath))
    else:
        cursor.execute(f"INSERT INTO {TABLE_NAME} (timestamp, path, hash) VALUES (?, ?, ?)",
                       (timestamp, filepath, md5))
    conn.commit()
    print(f"Updated hash for {filepath}")

def delete_file(conn, filepath):
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE path = ?", (filepath,))
    conn.commit()
    print(f"Deleted {filepath} from database.")

def list_files(conn):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    for row in cursor.fetchall():
        print(row)

def check_files(conn, logfile=None):
    cursor = conn.cursor()
    cursor.execute(f"SELECT path, hash FROM {TABLE_NAME}")
    for path, stored_hash in cursor.fetchall():
        current_hash = get_md5(path)
        if current_hash is None:
            log_message(f"ERROR: {path} not found", logfile)
        elif current_hash != stored_hash:
            log_message(f"ERROR: {path} hash mismatch, possible attack", logfile)
        else:
            log_message(f"OK: {path} hash matches", logfile)

def main():
    if len(sys.argv) < 2:
        print("Usage: ./filehash.py <cmd> <options>")
        sys.exit(1)

    cmd = sys.argv[1]
    option = sys.argv[2] if len(sys.argv) > 2 else None

    conn = setup_db()

    if cmd == "update" and option:
        update_file(conn, option)
    elif cmd == "delete" and option:
        delete_file(conn, option)
    elif cmd == "list":
        list_files(conn)
    elif cmd == "check":
        check_files(conn, option)
    else:
        print("Invalid command or missing options.")

    conn.close()

if __name__ == "__main__":
    main()
