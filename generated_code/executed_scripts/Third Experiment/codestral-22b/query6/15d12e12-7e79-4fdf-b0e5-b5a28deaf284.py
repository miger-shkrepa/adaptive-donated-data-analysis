import os
import json
import csv
from datetime import datetime

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the changes
changes = []

# Define the path to the signup_details.json file
signup_details_path = os.path.join(root_dir, "personal_information", "signup_details.json")

# Check if the signup_details.json file exists
if os.path.exists(signup_details_path):
    # Open the signup_details.json file
    with open(signup_details_path, 'r') as f:
        # Load the JSON data
        data = json.load(f)

    # Extract the relevant data
    for item in data["account_history_registration_info"]:
        for key, value in item["string_map_data"].items():
            # Convert the timestamp to a date
            date = datetime.fromtimestamp(value["timestamp"]).strftime('%Y-%m-%d')
            changes.append(["Signup " + key, value["value"], date])

# Define the path to the personal_information.json file
personal_info_path = os.path.join(root_dir, "personal_information", "personal_information.json")

# Check if the personal_information.json file exists
if os.path.exists(personal_info_path):
    # Open the personal_information.json file
    with open(personal_info_path, 'r') as f:
        # Load the JSON data
        data = json.load(f)

    # Extract the relevant data
    for item in data["profile_user"]:
        for key, value in item["string_map_data"].items():
            # Convert the timestamp to a date
            date = datetime.fromtimestamp(value["timestamp"]).strftime('%Y-%m-%d')
            changes.append([key, value["value"], date])

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(changes)