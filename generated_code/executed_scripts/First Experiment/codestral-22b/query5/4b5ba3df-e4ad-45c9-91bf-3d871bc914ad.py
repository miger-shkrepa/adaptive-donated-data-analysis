import os
import csv
import json
from datetime import datetime

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the results
results = []

# Traverse the directory structure
for foldername, subfolders, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename == "devices.json":
            filepath = os.path.join(foldername, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                for device in data["devices_devices"]:
                    if "Last Login" in device["string_map_data"]:
                        device_id = device["title"]
                        login_time = datetime.fromtimestamp(device["string_map_data"]["Last Login"]["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
                        results.append([device_id, login_time])

# Save the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Device ID", "Login Time"])
    writer.writerows(results)