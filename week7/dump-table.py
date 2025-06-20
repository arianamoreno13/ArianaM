#!/usr/bin/env python3
import sys
import csv
import json
import sqlcipher3

# Constants
DB_NAME = 'etest.db'
DB_KEY = 'mysecret123'
TABLE_NAME = 'devices'

# Validate arguments
if len(sys.argv) < 2 or sys.argv[1] not in ['screen', 'csv', 'json']:
    print("Usage: dump-table.py <screen|csv|json> [outputfile]")
    sys.exit(1)

mode = sys.argv[1]
output_file = sys.argv[2] if len(sys.argv) == 3 else None

# Connect to encrypted database and fetch data
try:
    conn = sqlcipher3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA key = '{DB_KEY}';")

    # Fetch data
    result = cursor.execute(f"SELECT * FROM {TABLE_NAME};")
    rows = result.fetchall()
    headers = [description[0] for description in result.description]

    # Output to screen
    if mode == 'screen':
        for row in rows:
            print(dict(zip(headers, row)))

    # Output to CSV
    elif mode == 'csv':
        if not output_file:
            print("Output file required for CSV mode.")
            sys.exit(1)
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

    # Output to JSON
    elif mode == 'json':
        if not output_file:
            print("Output file required for JSON mode.")
            sys.exit(1)
        with open(output_file, 'w') as f:
            json_data = [dict(zip(headers, row)) for row in rows]
            json.dump(json_data, f, indent=2)

except Exception as e:
    print(f"[!] Error: {e}")
    sys.exit(1)

finally:
    conn.close()

