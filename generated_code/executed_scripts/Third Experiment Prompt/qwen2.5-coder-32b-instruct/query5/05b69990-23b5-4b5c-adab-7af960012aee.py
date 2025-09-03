import os
import csv
import json
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the path to the output CSV file
output_csv_path = "query_responses/results.csv"

# Function to convert timestamp to a readable date format
def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a list to store the results
results = []

# Define the path to the devices.json file
devices_json_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")

# Check if the devices.json file exists
if os.path.exists(devices_json_path):
    try:
        # Open and read the devices.json file
        with open(devices_json_path, 'r', encoding='utf-8') as file:
            devices_data = json.load(file)
        
        # Extract the device information
        if "devices_devices" in devices_data:
            for device in devices_data["devices_devices"]:
                if "string_map_data" in device:
                    device_id = device["string_map_data"].get("User Agent", {}).get("value", "")
                    login_time_timestamp = device["string_map_data"].get("Last Login", {}).get("timestamp", 0)
                    login_time = timestamp_to_datetime(login_time_timestamp)
                    results.append((device_id, login_time))
    except (json.JSONDecodeError, KeyError) as e:
        raise ValueError(f"ValueError: Error parsing devices.json - {str(e)}")

# Write the results to the CSV file
try:
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Device ID", "Login Time"])
        csvwriter.writerows(results)
except IOError as e:
    raise IOError(f"IOError: Error writing to CSV file - {str(e)}")