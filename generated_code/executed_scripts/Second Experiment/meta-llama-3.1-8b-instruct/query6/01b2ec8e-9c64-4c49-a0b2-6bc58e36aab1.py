import csv
import os
import json
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the changes
changes = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = json.load(file)
            
            # Check if the JSON data contains the required information
            if 'instagram_profile_information.json' in str(data):
                # Iterate over the Instagram profile information
                for profile in data['instagram_profile_information.json']['structure']['profile_account_insights']:
                    # Extract the changes
                    for key, value in profile['string_map_data'].items():
                        if key in ['Contact Syncing', 'First Close Friends Story Time', 'First Country Code', 'First Story Time', 'Has Shared Live Video', 'Last Login', 'Last Logout', 'Last Story Time']:
                            changes.append([key, value['value'], datetime.fromtimestamp(value['timestamp']).strftime('%Y-%m-%d')])
            
            # Check if the JSON data contains the required information
            if 'personal_information.json' in str(data):
                # Iterate over the personal information
                for profile in data['personal_information.json']['structure']['profile_user']:
                    # Extract the changes
                    for key, value in profile['string_map_data'].items():
                        if key in ['Bio', 'Date of birth', 'Time']:
                            changes.append([key, value['value'], datetime.fromtimestamp(value['timestamp']).strftime('%Y-%m-%d')])

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Changed', 'New Value', 'Change Date'])
    writer.writerows(changes)