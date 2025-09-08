import csv
import os

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
            data = eval(file.read())

            # Check if the JSON data contains the required structure
            if 'profile_profile_change' in data['profile_changes']['profile_profile_change']:
                # Iterate over the changes
                for change in data['profile_changes']['profile_profile_change']:
                    # Extract the changed, new value, and change date
                    changed = change['string_map_data']['Changed']['value']
                    new_value = change['string_map_data']['New Value']['value']
                    change_date = change['string_map_data']['Change Date']['value']

                    # Add the change to the list
                    changes.append([changed, new_value, change_date])

# Check if any changes were found
if not changes:
    # If no changes were found, write the column headers to the CSV file
    with open('query_responses/results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Changed', 'New Value', 'Change Date'])
else:
    # If changes were found, write them to the CSV file
    with open('query_responses/results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Changed', 'New Value', 'Change Date'])
        writer.writerows(changes)