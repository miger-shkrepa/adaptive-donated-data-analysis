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

# Define the path to the profile_changes.json file
profile_changes_path = os.path.join(root_dir, "personal_information", "profile_changes.json")

# Check if the profile_changes.json file exists
if os.path.exists(profile_changes_path):
    # Open the profile_changes.json file
    with open(profile_changes_path, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Extract the profile_profile_change data
        profile_changes = data["structure"]["profile_profile_change"]

        # Iterate over the profile changes
        for change in profile_changes:
            # Extract the changed field, new value, and change date
            changed = change["string_map_data"]["Changed"]["value"]
            new_value = change["string_map_data"]["New Value"]["value"]
            change_date = change["string_map_data"]["Change Date"]["value"]

            # Convert the change date to the desired format
            change_date = datetime.fromtimestamp(int(change_date)).strftime("%Y-%m-%d")

            # Append the change to the changes list
            changes.append([changed, new_value, change_date])

# Define the path to the output CSV file
output_path = "query_responses/results.csv"

# Create the directory if it does not exist
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Write the changes to the output CSV file
with open(output_path, "w", newline="") as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["Changed", "New Value", "Change Date"])

    # Write the changes
    writer.writerows(changes)