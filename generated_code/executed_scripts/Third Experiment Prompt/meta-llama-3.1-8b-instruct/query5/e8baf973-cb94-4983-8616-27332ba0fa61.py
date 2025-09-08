import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list of devices and login times
devices = []
login_times = []

# Iterate over the subdirectories in the root directory
for dirpath, dirnames, filenames in os.walk(root_dir):
    # Check if the subdirectory is 'device_information'
    if dirnames and dirnames[0] == 'device_information':
        # Iterate over the files in the subdirectory
        for filename in filenames:
            # Check if the file is 'devices.json'
            if filename == 'devices.json':
                # Open the file and read its contents
                with open(os.path.join(dirpath, filename), 'r') as f:
                    data = f.read()
                    # Parse the JSON data
                    import json
                    data = json.loads(data)
                    # Iterate over the devices in the data
                    for device in data['devices_devices']:
                        # Extract the device ID and login time
                        device_id = device['string_map_data']['User Agent']['value']
                        login_time = device['string_map_data']['Last Login']['value']
                        # Add the device ID and login time to the lists
                        devices.append(device_id)
                        login_times.append(login_time)

# Create the CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(['Device ID', 'Login Time'])
    # Write the data
    for device, login_time in zip(devices, login_times):
        writer.writerow([device, login_time])