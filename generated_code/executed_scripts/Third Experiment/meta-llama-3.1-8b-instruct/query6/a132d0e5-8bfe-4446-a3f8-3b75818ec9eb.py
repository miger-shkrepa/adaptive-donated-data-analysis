import csv
import os
import json

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
            if 'policy_updates_and_permissions' in data and 'notification_of_privacy_policy_updates.json' in data['policy_updates_and_permissions']:
                # Iterate over the policy updates and permissions
                for update in data['policy_updates_and_permissions']['notification_of_privacy_policy_updates.json']['structure']['policy_updates_and_permissions_notification_of_privacy_policy_updates']:
                    # Check if the update contains the required information
                    if 'string_map_data' in update and 'Consent Status' in update['string_map_data'] and 'Impression Time' in update['string_map_data']:
                        # Extract the consent status and impression time
                        consent_status = update['string_map_data']['Consent Status']['value']
                        impression_time = update['string_map_data']['Impression Time']['value']
                        
                        # Add the change to the list
                        changes.append([consent_status, impression_time, impression_time])

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Changed', 'New Value', 'Change Date'])  # Write the column headers
    writer.writerows(changes)