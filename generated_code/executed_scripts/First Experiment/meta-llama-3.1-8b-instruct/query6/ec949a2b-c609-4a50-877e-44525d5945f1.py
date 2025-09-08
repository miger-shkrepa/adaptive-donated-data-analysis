import os
import csv
import json
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the changes
changes = []

# Iterate over the JSON files in the directory
for filename in os.listdir(root_dir):
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            data = json.load(file)
            
            # Check if the JSON file contains Instagram account changes
            if "instagram_profile_information.json" in str(data):
                # Iterate over the Instagram account changes
                for change in data["instagram_profile_information.json"]["structure"]["profile_account_insights"]:
                    # Extract the change date, new value, and changed field
                    change_date = datetime.strptime(change["string_map_data"]["Last Login"]["timestamp"], "%Y-%m-%d").strftime("%Y-%m-%d")
                    new_value = change["string_map_data"]["Last Login"]["value"]
                    changed_field = "Last Login"
                    
                    # Append the change to the list
                    changes.append([changed_field, new_value, change_date])

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Changed", "New Value", "Change Date"])  # header
    writer.writerows(changes)