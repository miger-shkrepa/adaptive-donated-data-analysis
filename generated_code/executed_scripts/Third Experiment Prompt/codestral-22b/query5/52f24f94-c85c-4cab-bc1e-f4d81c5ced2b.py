import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"
output_file = "query_responses/results.csv"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the results
results = []

# Define the path to the devices.json file
devices_file = os.path.join(root_dir, "personal_information", "device_information", "devices.json")

# Check if the devices.json file exists
if os.path.exists(devices_file):
    # Open the devices.json file
    with open(devices_file, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Check if the data has the expected structure
        if "devices_devices" in data:
            # Iterate over the devices
            for device in data["devices_devices"]:
                # Check if the device has a "string_map_data" field
                if "string_map_data" in device:
                    # Extract the device ID and login time
                    device_id = device["string_map_data"].get("User Agent", {}).get("value", "")
                    login_time = device["string_map_data"].get("Last Login", {}).get("value", "")

                    # Convert the login time to the desired format
                    if login_time:
                        login_time = datetime.fromtimestamp(int(login_time)).strftime("%Y-%m-%d %H:%M:%S")

                    # Add the result to the list
                    results.append([device_id, login_time])

# Write the results to a CSV file
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Device ID", "Login Time"])
    writer.writerows(results)