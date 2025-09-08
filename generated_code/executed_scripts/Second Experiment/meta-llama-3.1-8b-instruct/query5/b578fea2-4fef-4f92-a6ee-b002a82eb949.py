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
            
            # Check if the JSON file contains login information
            if "login_and_profile_creation" in data and "login_activity.json" in data["login_and_profile_creation"]:
                # Open the login activity JSON file
                with open(os.path.join(root_dir, "login_and_profile_creation", "login_activity.json"), 'r') as login_file:
                    # Load the login activity JSON data
                    login_data = json.load(login_file)
                    
                    # Iterate over the login history
                    for login in login_data["account_history_login_history"]:
                        # Extract the device ID and login time
                        device_id = login["string_map_data"]["User Agent"]["value"]
                        login_time = login["string_map_data"]["Time"]["value"]
                        
                        # Add the device ID and login time to the lists
                        device_ids.append(device_id)
                        login_times.append(login_time)

# Create a CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create a CSV writer object
    writer = csv.writer(csvfile)
    
    # Write the column headers
    writer.writerow(["Device ID", "Login Time"])
    
    # Write the device IDs and login times
    for device_id, login_time in zip(device_ids, login_times):
        writer.writerow([device_id, login_time])