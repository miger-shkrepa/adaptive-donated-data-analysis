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

# Define the path to the devices.json file
devices_file = os.path.join(root_dir, "personal_information", "device_information", "devices.json")

# Check if the devices.json file exists
if not os.path.exists(devices_file):
    raise FileNotFoundError("FileNotFoundError: The devices.json file does not exist.")

# Load the data from the devices.json file
with open(devices_file, "r") as f:
    data = json.load(f)

# Extract the relevant information from the data
for device in data["devices_devices"]:
    device_id = device["string_map_data"].get("GerÃ¤te-ID", {}).get("value", "")
    login_time = device["string_map_data"].get("Last Login", {}).get("value", "")

    # Convert the login time to the desired format
    if login_time:
        login_time = datetime.fromtimestamp(int(login_time)).strftime("%Y-%m-%d %H:%M:%S")

    results.append([device_id, login_time])

# Define the path to the output CSV file
output_file = "query_responses/results.csv"

# Write the results to the output CSV file
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Device ID", "Login Time"])
    writer.writerows(results)