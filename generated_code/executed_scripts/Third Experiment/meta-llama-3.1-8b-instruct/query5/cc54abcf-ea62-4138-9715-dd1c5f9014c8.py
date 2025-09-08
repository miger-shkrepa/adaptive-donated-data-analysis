import csv
import os
import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the device IDs and login times
device_login_times = []

# Iterate over each file in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = file.read()
            # Parse the JSON data
            json_data = eval(data)
            # Check if the JSON data contains the required information
            if 'creation_timestamp' in json_data and 'device_id' in json_data['media_metadata']['photo_metadata']['exif_data'][0]:
                # Extract the device ID and login time
                device_id = json_data['media_metadata']['photo_metadata']['exif_data'][0]['device_id']
                login_time = datetime.datetime.fromtimestamp(int(json_data['creation_timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
                # Append the device ID and login time to the list
                device_login_times.append([device_id, login_time])

# Write the device IDs and login times to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(['Device ID', 'Login Time'])
    # Write the device IDs and login times
    writer.writerows(device_login_times)