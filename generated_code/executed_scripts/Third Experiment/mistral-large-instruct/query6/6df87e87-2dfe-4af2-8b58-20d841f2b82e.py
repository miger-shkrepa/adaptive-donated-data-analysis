import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to parse the profile changes JSON file
def parse_profile_changes(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            changes = []
            for change in data['profile_profile_change']:
                change_date = datetime.fromtimestamp(change['string_map_data']['Change Date']['timestamp']).strftime('%Y-%m-%d')
                new_value = change['string_map_data']['New Value']['value']
                changed = change['string_map_data']['Changed']['value']
                changes.append((changed, new_value, change_date))
            return changes
    except FileNotFoundError:
        raise FileNotFoundError("Error: The profile changes file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The profile changes file is not a valid JSON.")

# Function to write the results to a CSV file
def write_to_csv(changes, output_file):
    try:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Changed', 'New Value', 'Change Date'])
            for change in changes:
                writer.writerow(change)
    except Exception as e:
        raise ValueError(f"Error: Failed to write to CSV file. {str(e)}")

# Main function to process the directory and extract changes
def main():
    profile_changes_file = os.path.join(root_dir, 'personal_information', 'profile_changes.json')

    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    if not os.path.exists(profile_changes_file):
        # If the profile changes file does not exist, create a CSV with only headers
        write_to_csv([], output_csv)
        return

    changes = parse_profile_changes(profile_changes_file)
    write_to_csv(changes, output_csv)

if __name__ == "__main__":
    main()