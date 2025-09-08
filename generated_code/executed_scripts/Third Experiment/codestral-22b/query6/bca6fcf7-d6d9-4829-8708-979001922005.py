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

# Define the path to the account details file
account_details_path = os.path.join(root_dir, "security_and_login_information", "login_and_profile_creation", "instagram_signup_details.json")

# Check if the account details file exists
if os.path.exists(account_details_path):
    # Open the account details file
    with open(account_details_path, 'r') as f:
        # Load the JSON data
        data = json.load(f)

    # Extract the account history registration info
    account_history = data["account_history_registration_info"][0]["string_map_data"]

    # Define the fields to track
    fields = ["Email", "Phone Number"]

    # Iterate over the fields
    for field in fields:
        # Check if the field exists in the account history
        if field in account_history:
            # Extract the value and timestamp
            value = account_history[field]["value"]
            timestamp = account_history[field]["timestamp"]

            # Convert the timestamp to a date
            date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

            # Add the change to the list
            changes.append(["Changed", value, date])
else:
    # If the account details file does not exist, add a header to the changes list
    changes.append(["Changed", "New Value", "Change Date"])

# Define the path to the results file
results_path = "query_responses/results.csv"

# Open the results file
with open(results_path, 'w', newline='') as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the changes to the file
    writer.writerows(changes)