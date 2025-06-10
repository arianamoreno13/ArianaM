#!/usr/bin/env python3
import os
import sys
from datetime import datetime

def log_message(username, status, file_path, logfile=None):
    timestamp = datetime.now().isoformat(timespec='seconds')
    message = f"{timestamp} {username}: {status}: {file_path}"
    
    if logfile:
        try:
            with open(logfile, 'a') as log:
                log.write(message + "\n")
        except Exception as e:
            print(f"Failed to write to log: {e}")
    else:
        print(message)

def check_dotfiles(logfile=None):
    home_dir = os.path.expanduser("~")
    user = os.path.basename(home_dir)

    for item in os.listdir(home_dir):
        if item.startswith("."):
            path = os.path.join(home_dir, item)
            if os.path.isfile(path):
                size_kb = os.path.getsize(path) / 1024
                if size_kb > 50:
                    log_message(user, "ERROR", f"{item} is larger than 50KB", logfile)
                else:
                    log_message(user, "OK", f"{item} is less than 50KB", logfile)

def main():
    if len(sys.argv) < 2 or sys.argv[1] != "check":
        print("Usage: ./dotfiles.py check [logfile]")
        sys.exit(1)

    logfile = sys.argv[2] if len(sys.argv) == 3 else None
    check_dotfiles(logfile)

if __name__ == "__main__":
    main()
