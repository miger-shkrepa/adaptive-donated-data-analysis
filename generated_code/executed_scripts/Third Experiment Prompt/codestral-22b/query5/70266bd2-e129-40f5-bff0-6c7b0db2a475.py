import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"
output_file = "query_responses/results.csv"

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
    with open(login_activity_file, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Extract the login activity data
        login_activity = data.get("account_history_login_history", [])

        # Iterate over the login activity data
        for activity in login_activity:
            # Extract the device ID and login time
            device_id = activity["string_map_data"].get("Name des Cookies", {}).get("value", "")
            login_time = activity["string_map_data"].get("Zeit", {}).get("value", "")

            # Check if the login time is empty
            if login_time:
                # Convert the login time to the desired format
                login_time = datetime.strptime(login_time, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d %H:%M:%S")

                # Add the result to the list
                results.append([device_id, login_time])

# Write the results to a CSV file
with open(output_file, "w", newline="") as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["Device ID", "Login Time"])

    # Write the results
    writer.writerows(results)