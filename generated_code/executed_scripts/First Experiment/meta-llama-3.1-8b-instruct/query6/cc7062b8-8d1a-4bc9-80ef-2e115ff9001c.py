import os
import csv
import json
from datetime import datetime

# Declare the variable referring to the file input
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
            
            # Check if the JSON file contains the required information
            if 'personal_information' in data and 'instagram_profile_information.json' in data['personal_information']:
                # Extract the changes from the JSON file
                for change in data['personal_information']['instagram_profile_information.json']['structure']['profile_account_insights']:
                    changes.append({
                        'Changed': change['string_map_data']['First Close Friends Story Time']['value'],
                        'New Value': change['string_map_data']['Last Story Time']['value'],
                        'Change Date': datetime.fromtimestamp(change['string_map_data']['Last Story Time']['timestamp']).strftime('%Y-%m-%d')
                    })

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Changed', 'New Value', 'Change Date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write the header
    writer.writeheader()
    
    # Write the changes
    for change in changes:
        writer.writerow(change)