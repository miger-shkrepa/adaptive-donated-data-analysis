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

# Define the path to the account information file
account_info_path = os.path.join(root_dir, "logged_information", "account_information.json")

# Check if the account information file exists
if os.path.exists(account_info_path):
    # Load the account information
    with open(account_info_path, "r") as f:
        account_info = json.load(f)

    # Extract the changes
    for change in account_info["structure"]["account_information"]:
        changes.append({
            "Changed": change["changed_field"],
            "New Value": change["new_value"],
            "Change Date": datetime.fromtimestamp(change["timestamp"]).strftime('%Y-%m-%d')
        })

# Define the path to the output file
output_path = "query_responses/results.csv"

# Write the changes to a CSV file
with open(output_path, "w", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["Changed", "New Value", "Change Date"])
    writer.writeheader()
    writer.writerows(changes)