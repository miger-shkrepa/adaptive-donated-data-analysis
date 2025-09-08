import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list of changes
changes = []

# Iterate over the directory structure
for dir, _, files in os.walk(root_dir):
    # Check if the directory contains the 'personal_information' folder
    if 'personal_information' in dir:
        # Iterate over the files in the 'personal_information' folder
        for file in files:
            # Check if the file is a JSON file
            if file.endswith('.json'):
                # Open the file and read its contents
                with open(os.path.join(dir, file), 'r') as f:
                    data = json.load(f)
                    # Check if the file contains the 'profile_user' key
                    if 'profile_user' in data:
                        # Iterate over the 'profile_user' key
                        for item in data['profile_user']:
                            # Check if the item contains the 'string_map_data' key
                            if 'string_map_data' in item:
                                # Iterate over the 'string_map_data' key
                                for key, value in item['string_map_data'].items():
                                    # Check if the key is one of the expected changes (name, phone, email)
                                    if key in ['Name', 'Phone Number', 'Email']:
                                        # Add the change to the list
                                        changes.append({
                                            'Changed': key,
                                            'New Value': value['value'],
                                            'Change Date': value['timestamp']
                                        })

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['Changed', 'New Value', 'Change Date'])
    writer.writeheader()
    writer.writerows(changes)