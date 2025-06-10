#!/usr/bin/env python3
import sys
import csv
import requests
import time

def main():
    if len(sys.argv) != 3:
        print("Usage: ./scanlocation.py <input_csv> <output_csv>")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_csv = sys.argv[2]

    try:
        with open(input_csv, mode='r') as infile, open(output_csv, mode='w', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            # Read and skip original header, then write new header
            next(reader)
            writer.writerow(["DNS", "IP", "Country", "RegionName", "City", "Zipcode", "ISP"])

            for row in reader:
                if len(row) < 2:
                    continue

                dns, ip = row[0], row[1]
                if ':' in ip:
                    continue  # Skip IPv6

                location_data = get_ip_info(ip)
                writer.writerow([dns, ip] + location_data)

                time.sleep(1)  # Respect API rate limits

        print(f"Location scan complete. Results saved to {output_csv}")

    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

def get_ip_info(ip):
    url = f"http://ip-api.com/json/{ip}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if data['status'] == 'success':
            return [
                data.get('country', ''),
                data.get('regionName', ''),
                data.get('city', ''),
                data.get('zip', ''),
                data.get('isp', '')
            ]
        else:
            return ['N/A'] * 5
    except requests.RequestException:
        return ['N/A'] * 5

if __name__ == "__main__":
    main()

