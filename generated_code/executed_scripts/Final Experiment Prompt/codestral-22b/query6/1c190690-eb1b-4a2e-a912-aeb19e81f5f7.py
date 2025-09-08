import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output file path
output_file = "query_responses/results.csv"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Define the path to the profile changes file
profile_changes_file = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

# Initialize an empty list to store the changes
changes = []

# Check if the profile changes file exists
if os.path.exists(profile_changes_file):
    # Open the profile changes file
    with open(profile_changes_file, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Check if the data is a list
        if isinstance(data, list):
            # Iterate over the changes
            for change in data:
                # Extract the changed field, new value, and change date
                changed = change["string_map_data"]["Changed"]["value"]
                new_value = change["string_map_data"]["New Value"]["value"]
                change_date = datetime.fromtimestamp(change["string_map_data"]["Change Date"]["timestamp"]).strftime("%Y-%m-%d")

                # Add the change to the list
                changes.append([changed, new_value, change_date])

# Open the output file
with open(output_file, "w", newline="") as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["Changed", "New Value", "Change Date"])

    # Write the changes
    writer.writerows(changes)