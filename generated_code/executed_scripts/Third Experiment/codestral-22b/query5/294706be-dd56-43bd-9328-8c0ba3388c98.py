import os
import json
import csv
from datetime import datetime

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the results
results = []

# Define the path to the login_activity.json file
login_activity_path = os.path.join(root_dir, "your_instagram_activity", "login_activity.json")

# Check if the login_activity.json file exists
if os.path.exists(login_activity_path):
    # Open the login_activity.json file
    with open(login_activity_path, 'r') as f:
        # Load the JSON data
        data = json.load(f)

        # Check if the 'account_history_login_history' key exists in the data
        if 'account_history_login_history' in data['structure']:
            # Iterate over the login history
            for login in data['structure']['account_history_login_history']:
                # Check if the 'string_map_data' key exists in the login data
                if 'string_map_data' in login:
                    # Extract the device ID and login time
                    device_id = login['string_map_data'].get('Device', {}).get('value', '')
                    login_time = login['string_map_data'].get('Time', {}).get('value', '')

                    # Convert the login time to the desired format
                    if login_time:
                        login_time = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')

                    # Append the results to the list
                    results.append([device_id, login_time])

# Define the path to the results.csv file
results_path = "query_responses/results.csv"

# Write the results to the results.csv file
with open(results_path, 'w', newline='') as f:
    # Create a CSV writer object
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(['Device ID', 'Login Time'])

    # Write the results
    writer.writerows(results)