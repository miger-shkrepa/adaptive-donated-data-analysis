import os
import json
import csv
from datetime import datetime

# Declare the root directory
root_dir = "root_dir"

# Define the path to the JSON file
json_file_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")

# Initialize an empty list to store the results
results = []

# Check if the JSON file exists
if os.path.exists(json_file_path):
    try:
        # Open the JSON file
        with open(json_file_path, 'r') as f:
            # Load the JSON data
            data = json.load(f)

        # Iterate over the devices
        for device in data.get("devices_devices", []):
            # Extract the device ID and login time
            device_id = device["string_map_data"].get("User Agent", {}).get("value", "")
            login_time = device["string_map_data"].get("Last Login", {}).get("timestamp", 0)

            # Convert the login time to a datetime object
            login_time = datetime.fromtimestamp(login_time)

            # Format the login time as a string
            login_time = login_time.strftime('%Y-%m-%d %H:%M:%S')

            # Add the results to the list
            results.append({"Device ID": device_id, "Login Time": login_time})

    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")

else:
    raise FileNotFoundError("Error: The JSON file does not exist.")

# Define the path to the CSV file
csv_file_path = "query_responses/results.csv"

# Write the results to a CSV file
with open(csv_file_path, 'w', newline='') as f:
    # Create a CSV writer
    writer = csv.DictWriter(f, fieldnames=["Device ID", "Login Time"])

    # Write the header
    writer.writeheader()

    # Write the rows
    writer.writerows(results)