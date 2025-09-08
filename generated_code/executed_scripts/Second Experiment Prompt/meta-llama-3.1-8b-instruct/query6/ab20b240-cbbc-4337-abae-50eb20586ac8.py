import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Changed', 'New Value', 'Change Date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Iterate over the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == 'profile_changes.json':
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r') as file:
                    data = json.load(file)
                    for item in data['profile_profile_change']:
                        changed = item['Changed']
                        new_value = item['New Value']
                        change_date = item['Change Date']
                        writer.writerow({'Changed': changed, 'New Value': new_value, 'Change Date': change_date})