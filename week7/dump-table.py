#!/usr/bin/env python3

import sys
import csv
import json
import sqlcipher3

database = 'etest.db'
table = 'devices'
password = 'mysecret123'

# Check Arguments
if len(sys.argv) < 2 or sys.argv[1] not in ['screen', 'csv', 'json']:
    print("Usage: dump-table.py <screen|csv|json> [outputfile]")
    sys.exit(1)

mode = sys.argv[1]
output_file = sys.argv[2] if len(sys.argv) == 3 else None

# Connect to Encrypted Database
conn = sqlcipher3.connect(database)
cursor = conn.cursor()
cursor.execute(f"PRAGMA key='{password}';")

# Get Data
try:
    result = cursor.execute(f"SELECT * FROM {table};")
    rows = result.fetchall()
    headers = [description[0] for description in result.description]
except Exception as e:
    print("Error querying database:", e)
    conn.close()
    sys.exit(1)

# Output to Screen
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

# Cleanup
conn.close()
