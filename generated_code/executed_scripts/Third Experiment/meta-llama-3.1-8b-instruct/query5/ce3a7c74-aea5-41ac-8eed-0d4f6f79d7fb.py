import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize lists to store device IDs and login times
device_ids = []
login_times = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = json.load(file)
            
            # Check if the JSON file contains the required structure
            if 'devices.json' in data and 'devices_devices' in data['devices.json'] and 'string_map_data' in data['devices.json']['devices_devices'][0] and 'Last Login' in data['devices.json']['devices_devices'][0]['string_map_data']:
                # Extract the device ID and login time from the JSON data
                device_id = data['devices.json']['devices_devices'][0]['title']
                login_time = data['devices.json']['devices_devices'][0]['string_map_data']['Last Login']['value']
                
                # Add the device ID and login time to the lists
                device_ids.append(device_id)
                login_times.append(login_time)

# Create a CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create a CSV writer object
    writer = csv.writer(csvfile)
    
    # Write the column headers
    writer.writerow(['Device ID', 'Login Time'])
    
    # Write the device IDs and login times to the CSV file
    for device_id, login_time in zip(device_ids, login_times):
        writer.writerow([device_id, login_time])