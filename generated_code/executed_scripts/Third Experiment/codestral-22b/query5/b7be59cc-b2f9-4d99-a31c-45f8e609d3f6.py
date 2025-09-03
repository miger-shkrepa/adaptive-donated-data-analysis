import os
import json
import csv
from datetime import datetime

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the results
results = []

# Traverse the directory structure
for foldername, subfolders, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename == "login_activity.json":
            file_path = os.path.join(foldername, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                for entry in data["login_activity_sessions"]:
                    device_id = entry["string_map_data"]["Device ID"]["value"]
                    login_time = datetime.fromtimestamp(entry["creation_timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
                    results.append([device_id, login_time])

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Device ID", "Login Time"])
    writer.writerows(results)