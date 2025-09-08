import os
import json
import csv
from datetime import datetime

# Declare the root directory
root_dir = "root_dir"

# Define the path to the JSON file
json_file_path = os.path.join(root_dir, "personal_information/personal_information/profile_changes.json")

# Initialize an empty list to store the results
results = []

# Check if the JSON file exists
if os.path.exists(json_file_path):
    try:
        # Open the JSON file
        with open(json_file_path, 'r') as f:
            # Load the JSON data
            data = json.load(f)

        # Iterate over the profile changes
        for change in data.get("profile_profile_change", []):
            # Extract the required data
            changed = change["string_map_data"]["Changed"]["value"]
            new_value = change["string_map_data"]["New Value"]["value"]
            change_date = datetime.fromtimestamp(change["string_map_data"]["Change Date"]["timestamp"]).strftime('%Y-%m-%d')

            # Append the data to the results list
            results.append([changed, new_value, change_date])

    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")

# Define the path to the CSV file
csv_file_path = "query_responses/results.csv"

# Write the results to a CSV file
with open(csv_file_path, 'w', newline='') as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the header
    writer.writerow(["Changed", "New Value", "Change Date"])

    # Write the results
    writer.writerows(results)