import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = "query_responses/results.csv"

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# Initialize the CSV writer
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Device ID", "Login Time"])

    # Define the path to the devices.json file
    devices_file_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")

    # Check if the devices.json file exists
    if not os.path.exists(devices_file_path):
        raise FileNotFoundError("FileNotFoundError: The devices.json file does not exist.")

    # Read the devices.json file
    try:
        with open(devices_file_path, 'r') as devices_file:
            devices_data = json.load(devices_file)
    except json.JSONDecodeError:
        raise ValueError("ValueError: The devices.json file is not a valid JSON.")

    # Extract device IDs and login times
    try:
        for device in devices_data.get("devices_devices", []):
            string_map_data = device.get("string_map_data", {})
            device_id = string_map_data.get("Device ID", {}).get("value")
            last_login_timestamp = string_map_data.get("Last Login", {}).get("timestamp")

            if device_id and last_login_timestamp:
                login_time = datetime.fromtimestamp(last_login_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow([device_id, login_time])
    except KeyError as e:
        raise ValueError(f"ValueError: Missing key in devices.json: {e}")

print(f"Results have been written to {output_csv}")