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

# Iterate over the subdirectories
for dirpath, dirnames, filenames in os.walk(root_dir):
    # Check if the subdirectory is 'device_information'
    if dirpath.endswith('device_information'):
        # Iterate over the files in the subdirectory
        for filename in filenames:
            # Check if the file is 'devices.json'
            if filename == 'devices.json':
                # Open the file and read its contents
                with open(os.path.join(dirpath, filename), 'r') as f:
                    data = f.read()
                    # Parse the JSON data
                    data = json.loads(data)
                    # Iterate over the devices
                    for device in data.get('devices_devices', []):
                        # Extract the device ID and login time
                        device_id = device.get('string_map_data', {}).get('Device ID', {}).get('value')
                        login_time = device.get('string_map_data', {}).get('Last Login', {}).get('value')
                        # Append the result to the list
                        results.append([device_id, login_time])

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(['Device ID', 'Login Time'])
    # Write the results
    writer.writerows(results)