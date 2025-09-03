import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the output CSV file
output_file = "query_responses/results.csv"

# Define the CSV writer
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['Changed', 'New Value', 'Change Date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Iterate over the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == 'profile_changes.json':
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r') as file:
                        data = json.load(file)
                        for item in data['profile_profile_change']:
                            changed = item['string_map_data'].get('Changed', {}).get('value', '')
                            new_value = item['string_map_data'].get('New Value', {}).get('value', '')
                            change_date = item['string_map_data'].get('Change Date', {}).get('value', '')
                            writer.writerow({'Changed': changed, 'New Value': new_value, 'Change Date': change_date})
                except FileNotFoundError:
                    print(f"Error: The file '{filename}' does not exist.")
                except json.JSONDecodeError:
                    print(f"Error: The file '{filename}' is not a valid JSON file.")
                except KeyError:
                    print(f"Error: The file '{filename}' is missing required keys.")