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

# Iterate over the 'security_and_login_information' directory
for login_info in os.listdir(root_dir):
    if login_info.startswith("login_activity"):
        # Open the JSON file
        with open(os.path.join(root_dir, login_info), 'r') as f:
            data = json.load(f)
            # Iterate over the login history
            for login in data['account_history_login_history']:
                # Extract the device ID and login time
                device_id = login['string_map_data']['Name des Cookies']['value']
                login_time = login['string_map_data']['Zeit']['value']
                # Append the device ID and login time to the lists
                device_ids.append(device_id)
                login_times.append(login_time)

# Create a CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(['Device ID', 'Login Time'])
    # Write the device IDs and login times
    for device_id, login_time in zip(device_ids, login_times):
        writer.writerow([device_id, login_time])