import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the results
results = []

# Iterate over the subdirectories in the root directory
for dir_name in os.listdir(root_dir):
    dir_path = os.path.join(root_dir, dir_name)
    if os.path.isdir(dir_path):
        # Iterate over the files in the subdirectory
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            if file_name.endswith(".json"):
                # Open the JSON file and parse it
                with open(file_path, "r") as f:
                    data = json.load(f)
                # Check if the file contains the required data
                if "devices" in data and "devices_devices" in data["devices"]:
                    # Iterate over the devices in the file
                    for device in data["devices"]["devices_devices"]:
                        # Extract the device ID and login time
                        device_id = device["string_map_data"]["User Agent"]["value"]
                        login_time = device["string_map_data"]["Last Login"]["value"]
                        # Add the result to the list
                        results.append((device_id, login_time))

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Device ID", "Login Time"])
    writer.writerows(results)