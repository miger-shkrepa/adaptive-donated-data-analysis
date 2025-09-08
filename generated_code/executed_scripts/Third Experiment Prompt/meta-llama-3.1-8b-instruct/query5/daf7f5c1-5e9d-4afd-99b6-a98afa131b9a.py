import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Device ID", "Login Time"])

    # Iterate over the subdirectories
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check if the subdirectory is 'security_and_login_information'
        if dirpath.endswith('security_and_login_information'):
            # Iterate over the files in the subdirectory
            for filename in filenames:
                # Check if the file is 'login_activity.json'
                if filename == 'login_activity.json':
                    # Open the file and load the JSON data
                    with open(os.path.join(dirpath, filename), 'r') as f:
                        data = eval(f.read())
                    # Iterate over the login history
                    for login in data['account_history_login_history']:
                        # Extract the device ID and login time
                        device_id = login['string_map_data']['User Agent']['value']
                        login_time = login['string_map_data']['Zeit']['value']
                        # Write the data to the CSV file
                        writer.writerow([device_id, login_time])
                # Check if the file is 'last_known_location.json'
                elif filename == 'last_known_location.json':
                    # Open the file and load the JSON data
                    with open(os.path.join(dirpath, filename), 'r') as f:
                        data = eval(f.read())
                    # Iterate over the last known location
                    for location in data['account_history_imprecise_last_known_location']:
                        # Extract the device ID and login time
                        device_id = location['string_map_data']['Ungenauer Breitengrad']['value']
                        login_time = location['string_map_data']['Upload-Zeitpunkt']['value']
                        # Write the data to the CSV file
                        writer.writerow([device_id, login_time])
                # If the file is not 'login_activity.json' or 'last_known_location.json', skip it
                else:
                    continue
        # If the subdirectory is not 'security_and_login_information', skip it
        else:
            continue