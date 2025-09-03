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

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Construct the full path to the file
    filepath = os.path.join(root_dir, filename)

    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(filepath, 'r') as file:
            # Load the JSON data
            data = json.load(file)

            # Check if the JSON data contains the required structure
            if 'devices.json' in data and 'devices_devices' in data['devices.json']['structure']:
                # Iterate over the devices
                for device in data['devices.json']['structure']['devices_devices']:
                    # Check if the device has the required information
                    if 'Last Login' in device['string_map_data']:
                        # Extract the login time
                        login_time = device['string_map_data']['Last Login']['value']

                        # Extract the device ID
                        device_id = device['string_map_data']['Last Login']['href']

                        # Append the result to the list
                        results.append([device_id, login_time])

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Device ID', 'Login Time'])  # Write the header
    writer.writerows(results)  # Write the results