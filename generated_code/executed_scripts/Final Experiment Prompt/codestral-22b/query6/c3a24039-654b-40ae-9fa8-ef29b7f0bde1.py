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
    with open(profile_changes_file, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Iterate over the profile changes
        for change in data["profile_changes"]:
            # Extract the change data
            changed = change["changed"]
            new_value = change["new_value"]
            change_date = datetime.fromtimestamp(change["change_date"]).strftime("%Y-%m-%d")

            # Add the change to the list
            changes.append([changed, new_value, change_date])

# Define the path to the results file
results_file = "query_responses/results.csv"

# Open the results file
with open(results_file, "w", newline="") as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["Changed", "New Value", "Change Date"])

    # Write the changes
    writer.writerows(changes)