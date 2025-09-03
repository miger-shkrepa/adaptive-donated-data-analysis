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
for dirpath, dirnames, filenames in os.walk(root_dir):
    # Check if the current directory is 'personal_information'
    if dirpath.endswith('personal_information'):
        # Iterate over the files in the 'personal_information' directory
        for filename in filenames:
            # Check if the file is 'profile_changes.json'
            if filename == 'profile_changes.json':
                # Open the file and read its contents
                try:
                    with open(os.path.join(dirpath, filename), 'r') as f:
                        data = json.load(f)
                        # Iterate over the changes in the file
                        for change in data['profile_profile_change']:
                            # Extract the changed, new value, and change date
                            changed = change['string_map_data'].get('Changed', {}).get('value', '')
                            new_value = change['string_map_data'].get('New Value', {}).get('value', '')
                            change_date = change['string_map_data'].get('Change Date', {}).get('value', '')
                            # Append the change to the list of changes
                            changes.append([changed, new_value, change_date])
                except FileNotFoundError:
                    print(f"Error: The file '{os.path.join(dirpath, filename)}' does not exist.")
                except json.JSONDecodeError:
                    print(f"Error: The file '{os.path.join(dirpath, filename)}' is not a valid JSON file.")

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Changed', 'New Value', 'Change Date'])
    writer.writerows(changes)