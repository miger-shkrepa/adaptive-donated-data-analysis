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

# Define the path to the profile changes file
profile_changes_path = os.path.join(root_dir, "personal_information", "profile_changes.json")

# Check if the profile changes file exists
if os.path.exists(profile_changes_path):
    # Load the profile changes data
    with open(profile_changes_path, 'r') as f:
        profile_changes = json.load(f)

    # Extract the relevant data
    for change in profile_changes["structure"]["profile_profile_change"]:
        changed = change["string_map_data"]["Changed"]["value"]
        new_value = change["string_map_data"]["New Value"]["value"]
        change_date = datetime.fromtimestamp(change["string_map_data"]["Change Date"]["timestamp"]).strftime('%Y-%m-%d')
        changes.append([changed, new_value, change_date])

# Define the output file path
output_file = "query_responses/results.csv"

# Write the changes to a CSV file
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(changes)