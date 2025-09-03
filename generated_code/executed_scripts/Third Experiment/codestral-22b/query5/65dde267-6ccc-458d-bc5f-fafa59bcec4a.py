import os
import json
import csv
from datetime import datetime

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the login data
login_data = []

# Define the path to the login activity file
login_file_path = os.path.join(root_dir, "security_and_login_information", "login_activity.json")

# Check if the login activity file exists
if os.path.exists(login_file_path):
    # Open the login activity file
    with open(login_file_path, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Extract the login history
        login_history = data["structure"]["account_history_login_history"]

        # Iterate over the login history
        for login in login_history:
            # Extract the device ID and login time
            device_id = login["string_map_data"]["IP-Adresse"]["value"]
            login_time = login["string_map_data"]["Zeit"]["value"]

            # Convert the login time to the desired format
            login_time = datetime.fromtimestamp(int(login_time)).strftime("%Y-%m-%d %H:%M:%S")

            # Append the data to the login data list
            login_data.append([device_id, login_time])

# Define the path to the output CSV file
output_file_path = "query_responses/results.csv"

# Open the output CSV file
with open(output_file_path, "w", newline="") as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["Device ID", "Login Time"])

    # Write the login data
    writer.writerows(login_data)