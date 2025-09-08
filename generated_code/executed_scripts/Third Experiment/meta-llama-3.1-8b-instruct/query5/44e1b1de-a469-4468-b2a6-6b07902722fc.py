import csv
import os
import datetime

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
            data = file.read()
            # Parse the JSON data
            import json
            parsed_data = json.loads(data)
            # Check if the JSON data contains the required information
            if 'logged_information' in parsed_data and 'policy_updates_and_permissions' in parsed_data['logged_information'] and 'notification_of_privacy_policy_updates.json' in parsed_data['logged_information']['policy_updates_and_permissions']:
                # Extract the device IDs and login times from the JSON data
                for item in parsed_data['logged_information']['policy_updates_and_permissions']['notification_of_privacy_policy_updates.json']['structure']['policy_updates_and_permissions_notification_of_privacy_policy_updates']:
                    for key, value in item['string_map_data'].items():
                        if key == 'Impression Time':
                            login_time = datetime.datetime.strptime(value['value'], '%Y-%m-%d %H:%M:%S')
                            login_times.append(login_time.strftime('%Y-%m-%d %H:%M:%S'))
                        elif key == 'Consent Status':
                            device_ids.append(value['value'])
            else:
                # If the JSON data does not contain the required information, treat its contribution as 0
                pass

# Create a CSV file with the device IDs and login times
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Device ID', 'Login Time'])
    for device_id, login_time in zip(device_ids, login_times):
        writer.writerow([device_id, login_time])