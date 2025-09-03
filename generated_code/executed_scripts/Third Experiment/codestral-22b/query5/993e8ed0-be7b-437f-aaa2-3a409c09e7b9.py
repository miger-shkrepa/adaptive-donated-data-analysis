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

# Define the path to the login activity file
login_activity_file = os.path.join(root_dir, "security_and_login_information", "login_and_account_creation", "login_activity.json")

# Check if the login activity file exists
if os.path.exists(login_activity_file):
    # Open the login activity file
    with open(login_activity_file, 'r') as f:
        # Load the JSON data
        data = json.load(f)

        # Iterate over the login history
        for login in data["account_history_login_history"]:
            # Extract the device ID and login time
            device_id = login["string_map_data"]["Name des Cookies"]["value"]
            login_time = datetime.fromtimestamp(login["string_map_data"]["Zeit"]["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')

            # Append the results to the list
            results.append([device_id, login_time])

# Define the path to the output file
output_file = "query_responses/results.csv"

# Open the output file
with open(output_file, 'w', newline='') as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the header
    writer.writerow(["Device ID", "Login Time"])

    # Write the results
    writer.writerows(results)