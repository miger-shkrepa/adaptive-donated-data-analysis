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

# Define the path to the logged_information directory
logged_info_dir = os.path.join(root_dir, "logged_information")

# Check if the logged_information directory exists
if not os.path.exists(logged_info_dir):
    print("Warning: The logged_information directory does not exist. Skipping this part of the analysis.")
else:
    # Define the path to the account_information directory
    account_info_dir = os.path.join(logged_info_dir, "account_information")

    # Check if the account_information directory exists
    if not os.path.exists(account_info_dir):
        print("Warning: The account_information directory does not exist. Skipping this part of the analysis.")
    else:
        # Define the path to the account_data.json file
        account_data_file = os.path.join(account_info_dir, "account_data.json")

        # Check if the account_data.json file exists
        if not os.path.exists(account_data_file):
            print("Warning: The account_data.json file does not exist. Skipping this part of the analysis.")
        else:
            # Load the account data
            with open(account_data_file, 'r') as f:
                account_data = json.load(f)

            # Extract the relevant data
            for data in account_data["string_map_data"]:
                changes.append([data["title"], data["value"], datetime.fromtimestamp(data["timestamp"]).strftime('%Y-%m-%d')])

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(changes)