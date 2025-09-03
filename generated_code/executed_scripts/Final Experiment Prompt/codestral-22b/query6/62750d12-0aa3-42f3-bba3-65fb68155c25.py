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

# Check if the profile changes file exists
if os.path.exists(profile_changes_file):
    # Open the profile changes file
    with open(profile_changes_file, 'r') as f:
        # Load the JSON data
        data = json.load(f)

        # Iterate over the changes
        for change in data:
            # Extract the change date
            change_date = datetime.fromtimestamp(change['timestamp']).strftime('%Y-%m-%d')

            # Extract the changed field and the new value
            changed_field = change['changed_field']
            new_value = change['new_value']

            # Add the change to the list
            changes.append([changed_field, new_value, change_date])
else:
    # If the file does not exist, print a message and continue
    print("Warning: The profile changes file does not exist.")

# Define the path to the output file
output_file = "query_responses/results.csv"

# Open the output file
with open(output_file, 'w', newline='') as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["Changed", "New Value", "Change Date"])

    # Write the changes
    writer.writerows(changes)