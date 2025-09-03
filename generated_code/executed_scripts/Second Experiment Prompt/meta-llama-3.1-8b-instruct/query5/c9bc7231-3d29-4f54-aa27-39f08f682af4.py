import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the results
results = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as f:
            # Load the JSON data
            data = json.load(f)

            # Check if the file contains the required data
            if "device_information" in data and "devices.json" in data["device_information"]:
                # Open the devices.json file
                with open(os.path.join(root_dir, "device_information", "devices.json"), 'r') as f:
                    # Load the JSON data
                    devices_data = json.load(f)

                    # Iterate over the devices
                    for device in devices_data["devices_devices"]:
                        # Extract the device ID and login time
                        device_id = device["string_map_data"]["Device ID"]["value"]
                        login_time = device["string_map_data"]["Last Login"]["value"]

                        # Add the result to the list
                        results.append([device_id, login_time])

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Device ID", "Login Time"])  # header
    writer.writerows(results)