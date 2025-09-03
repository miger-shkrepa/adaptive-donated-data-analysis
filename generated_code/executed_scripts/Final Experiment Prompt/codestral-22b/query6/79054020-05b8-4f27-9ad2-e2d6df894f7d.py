import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the path to the profile changes file
profile_changes_file = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

# Initialize an empty list to store the changes
changes = []

# Check if the file exists
if os.path.exists(profile_changes_file):
    # Open the file and load the JSON data
    with open(profile_changes_file, "r") as f:
        data = json.load(f)

    # Extract the profile changes
    for change in data["profile_profile_change"]:
        # Extract the change details
        changed = change["string_map_data"]["Changed"]["value"]
        new_value = change["string_map_data"]["New Value"]["value"]
        change_date = datetime.fromtimestamp(change["string_map_data"]["Change Date"]["timestamp"]).strftime("%Y-%m-%d")

        # Add the change to the list
        changes.append([changed, new_value, change_date])

# Define the path to the output file
output_file = "query_responses/results.csv"

# Write the changes to the output file
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["Changed", "New Value", "Change Date"])

    # Write the changes
    writer.writerows(changes)