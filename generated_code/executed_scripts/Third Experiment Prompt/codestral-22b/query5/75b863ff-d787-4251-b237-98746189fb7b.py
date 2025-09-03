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
login_activity_file = os.path.join(root_dir, "security_and_login_information", "login_and_profile_creation", "login_activity.json")

# Check if the login activity file exists
if os.path.exists(login_activity_file):
    # Open the login activity file
    with open(login_activity_file, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Check if the data has the expected structure
        if "account_history_login_history" in data:
            # Iterate over the login history
            for login in data["account_history_login_history"]:
                # Check if the login has the expected structure
                if "string_map_data" in login and "Device ID" in login["string_map_data"] and "Time" in login["string_map_data"]:
                    # Extract the device ID and login time
                    device_id = login["string_map_data"]["Device ID"]["value"]
                    login_time = datetime.fromtimestamp(login["string_map_data"]["Time"]["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")

                    # Add the result to the list
                    results.append([device_id, login_time])

# Write the results to a CSV file
with open(output_file, "w", newline="") as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the header
    writer.writerow(["Device ID", "Login Time"])

    # Write the results
    writer.writerows(results)