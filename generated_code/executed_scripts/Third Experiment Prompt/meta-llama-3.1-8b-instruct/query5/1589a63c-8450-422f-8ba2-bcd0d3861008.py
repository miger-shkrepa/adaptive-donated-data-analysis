import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the results
results = []

# Iterate over the devices.json file in the device_information directory
for device_file in os.listdir(os.path.join(root_dir, "personal_information", "device_information")):
    if device_file == "devices.json":
        # Open the devices.json file
        with open(os.path.join(root_dir, "personal_information", "device_information", device_file), "r") as f:
            # Load the JSON data
            device_data = json.load(f)
            # Iterate over the devices_devices list
            for device in device_data["devices_devices"]:
                # Extract the device ID and last login time
                device_id = device["string_map_data"]["User Agent"]["value"]
                login_time = device["string_map_data"]["Last Login"]["value"]
                # Append the result to the list
                results.append([device_id, login_time])

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Device ID", "Login Time"])
    writer.writerows(results)