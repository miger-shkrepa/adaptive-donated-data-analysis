import os
import json
import csv

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
except FileNotFoundError as e:
    print(f"Error: {e}")
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Device ID', 'Login Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    exit()

device_info = []

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file == 'devices.json':
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    for device in data['devices_devices']:
                        device_id = device['string_map_data'].get('Last Login', {}).get('value')
                        login_time = device['string_map_data'].get('User Agent', {}).get('timestamp')
                        if device_id and login_time:
                            device_info.append({
                                'Device ID': device_id,
                                'Login Time': login_time
                            })
            except json.JSONDecodeError as e:
                raise ValueError("Error: Failed to parse JSON file.")
            except KeyError as e:
                raise ValueError("Error: Missing key in JSON file.")

if not device_info:
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Device ID', 'Login Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
else:
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Device ID', 'Login Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for device in device_info:
            writer.writerow(device)