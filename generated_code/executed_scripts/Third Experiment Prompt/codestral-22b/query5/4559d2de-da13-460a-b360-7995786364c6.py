import os
import json
from datetime import datetime
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

results = []

device_info_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")

if os.path.exists(device_info_path):
    with open(device_info_path, 'r') as f:
        device_info = json.load(f)

    for device in device_info.get("devices_devices", []):
        string_map_data = device.get("string_map_data", {})
        last_login = string_map_data.get("Last Login", {})
        timestamp = last_login.get("timestamp", 0)
        if timestamp:
            login_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            device_id = string_map_data.get("User Agent", {}).get("value", "")
            results.append([device_id, login_time])

output_path = "query_responses/results.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Device ID", "Login Time"])
    writer.writerows(results)