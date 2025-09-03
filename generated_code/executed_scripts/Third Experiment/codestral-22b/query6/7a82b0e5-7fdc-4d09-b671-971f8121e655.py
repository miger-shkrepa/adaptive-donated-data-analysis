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

# Define the path to the account history registration info
account_history_path = os.path.join(root_dir, "account_history_registration_info")

# Check if the account history directory exists
if not os.path.exists(account_history_path):
    print("Warning: The account history directory does not exist.")
else:
    # Loop through each file in the account history directory
    for filename in os.listdir(account_history_path):
        if filename.endswith(".json"):
            file_path = os.path.join(account_history_path, filename)

            # Open the file and load the JSON data
            with open(file_path, 'r') as f:
                data = json.load(f)

            # Extract the string map data
            string_map_data = data.get("string_map_data", {})

            # Loop through each key in the string map data
            for key, value in string_map_data.items():
                # Extract the new value and change date
                new_value = value.get("value", "")
                change_date = datetime.fromtimestamp(value.get("timestamp", 0)).strftime('%Y-%m-%d')

                # Add the change to the list
                changes.append([key, new_value, change_date])

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(changes)