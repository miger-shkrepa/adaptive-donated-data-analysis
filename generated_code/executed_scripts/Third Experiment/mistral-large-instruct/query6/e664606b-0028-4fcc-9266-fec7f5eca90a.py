import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# Function to parse the profile changes JSON file
def parse_profile_changes(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            changes = []
            for change in data['profile_profile_change']:
                change_date = datetime.fromtimestamp(change['string_map_data']['Change Date']['timestamp']).strftime('%Y-%m-%d')
                changed_field = change['string_map_data']['Changed']['value']
                new_value = change['string_map_data'].get('New Value', {}).get('value', '')
                changes.append((changed_field, new_value, change_date))
            return changes
    except FileNotFoundError:
        raise FileNotFoundError("Error: The profile changes file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The profile changes file is not a valid JSON.")

# Function to write the results to a CSV file
def write_to_csv(changes, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Changed', 'New Value', 'Change Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for change in changes:
            writer.writerow(dict(zip(fieldnames, change)))

# Main function to process the directory and extract changes
def main():
    profile_changes_file = os.path.join(root_dir, 'personal_information', 'profile_changes.json')
    if not os.path.exists(profile_changes_file):
        # If the file does not exist, create a CSV with only the column headers
        write_to_csv([], output_csv)
        return

    try:
        changes = parse_profile_changes(profile_changes_file)
        write_to_csv(changes, output_csv)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()