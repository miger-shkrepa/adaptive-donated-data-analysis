import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the results
results = []

# Iterate over the devices.json file
devices_file = os.path.join(root_dir, "personal_information", "device_information", "devices.json")
if os.path.exists(devices_file):
    with open(devices_file, 'r') as f:
        devices_data = json.load(f)
        if "devices_devices" in devices_data:
            for device in devices_data["devices_devices"]:
                login_time = device.get("string_map_data", {}).get("Last Login", {}).get("value", "")
                login_timestamp = device.get("string_map_data", {}).get("Last Login", {}).get("timestamp", "")
                results.append([login_time, login_timestamp])
else:
    # If the devices.json file does not exist, treat its contribution as 0
    results.append(["", ""])

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Device ID", "Login Time"])
    writer.writerows(results)