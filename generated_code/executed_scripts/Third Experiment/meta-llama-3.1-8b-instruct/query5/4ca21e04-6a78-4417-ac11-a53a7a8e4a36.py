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
for dir in os.listdir(root_dir):
    # Construct the full path to the subdirectory
    dir_path = os.path.join(root_dir, dir)

    # Check if the subdirectory is a directory
    if os.path.isdir(dir_path):
        # Iterate over the files in the subdirectory
        for file in os.listdir(dir_path):
            # Construct the full path to the file
            file_path = os.path.join(dir_path, file)

            # Check if the file is a JSON file
            if file.endswith(".json"):
                try:
                    # Open the JSON file and load its contents
                    with open(file_path, 'r') as f:
                        data = json.load(f)

                    # Check if the JSON file contains the required structure
                    if 'login_and_profile_creation' in data and 'login_activity.json' in data['login_and_profile_creation']:
                        # Open the login activity JSON file and load its contents
                        with open(os.path.join(dir_path, 'login_activity.json'), 'r') as f:
                            login_activity = json.load(f)

                        # Extract the device ID and login time from the login activity data
                        for item in login_activity['structure']['account_history_login_history']:
                            device_id = item['string_map_data']['Cookie Name']['value']
                            login_time = item['string_map_data']['Time']['value']

                            # Append the result to the list
                            results.append([device_id, login_time])
                except json.JSONDecodeError:
                    # Raise an error if the JSON file is not valid
                    raise ValueError("ValueError: The JSON file is not valid.")

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Device ID", "Login Time"])  # Write the header
    writer.writerows(results)  # Write the results