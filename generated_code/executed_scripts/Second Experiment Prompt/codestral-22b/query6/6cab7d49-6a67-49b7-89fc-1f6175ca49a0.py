import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"
output_file = "query_responses/results.csv"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the changes
changes = []

# Define the path to the profile changes file
profile_changes_file = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

# Check if the profile changes file exists
if os.path.exists(profile_changes_file):
    # Open the profile changes file
    with open(profile_changes_file, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Check if the data is a list
        if isinstance(data, list):
            # Iterate over the list
            for item in data:
                # Check if the item is a dictionary
                if isinstance(item, dict):
                    # Check if the item contains the "profile_profile_change" key
                    if "profile_profile_change" in item:
                        # Iterate over the list of changes
                        for change in item["profile_profile_change"]:
                            # Check if the change is a dictionary
                            if isinstance(change, dict):
                                # Check if the change contains the "string_map_data" key
                                if "string_map_data" in change:
                                    # Extract the relevant data
                                    changed = change["string_map_data"].get("Changed", {}).get("value", "")
                                    new_value = change["string_map_data"].get("New Value", {}).get("value", "")
                                    change_date = change["string_map_data"].get("Change Date", {}).get("value", "")

                                    # Convert the change date to the desired format
                                    try:
                                        change_date = datetime.fromtimestamp(int(change_date)).strftime("%Y-%m-%d")
                                    except ValueError:
                                        change_date = ""

                                    # Append the data to the changes list
                                    changes.append([changed, new_value, change_date])

# Write the changes to a CSV file
with open(output_file, "w", newline="") as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["Changed", "New Value", "Change Date"])

    # Write the data rows
    writer.writerows(changes)