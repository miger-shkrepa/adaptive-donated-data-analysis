import csv
import os
import json

# Declare the file input variable
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Device ID", "Login Time"])

    # Iterate through the JSON files in the directory
    for filename in os.listdir(root_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(root_dir, filename)
            with open(filepath, 'r') as json_file:
                data = json.load(json_file)

                # Check if the JSON file contains the required structure
                if 'account_history_login_history' in data['structure']:
                    for item in data['structure']['account_history_login_history']:
                        if 'string_map_data' in item and 'IP Address' in item['string_map_data']:
                            device_id = item['string_map_data']['IP Address']['value']
                            timestamp = item['string_map_data']['Time']['timestamp']
                            login_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                            writer.writerow([device_id, login_time])

                # Check if the JSON file contains the required structure for login history
                elif 'account_history_registration_info' in data['structure']:
                    for item in data['structure']['account_history_registration_info']:
                        if 'string_map_data' in item and 'Device' in item['string_map_data']:
                            device_id = item['string_map_data']['Device']['value']
                            timestamp = item['string_map_data']['Time']['timestamp']
                            login_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                            writer.writerow([device_id, login_time])

                # If the required structure is not found, write the column headers only
                else:
                    writer.writerow(["Device ID", "Login Time"])