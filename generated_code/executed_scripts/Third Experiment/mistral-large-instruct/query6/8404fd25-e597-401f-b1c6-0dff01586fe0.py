import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to parse JSON files and extract relevant information
def parse_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

# Function to extract account changes
def extract_account_changes(root_dir):
    changes = []

    # Define the paths to the relevant JSON files
    account_changes_files = [
        os.path.join(root_dir, 'logged_information', 'policy_updates_and_permissions', 'notification_of_privacy_policy_updates.json'),
        # Add other relevant file paths here if needed
    ]

    for file_path in account_changes_files:
        if not os.path.exists(file_path):
            continue

        data = parse_json_file(file_path)

        # Extract changes from the JSON data
        for item in data.get('policy_updates_and_permissions_notification_of_privacy_policy_updates', []):
            string_map_data = item.get('string_map_data', {})
            consent_status = string_map_data.get('Consent Status', {}).get('value', '')
            impression_time = string_map_data.get('Impression Time', {}).get('value', '')

            if consent_status and impression_time:
                changes.append({
                    'Changed': 'Consent Status',
                    'New Value': consent_status,
                    'Change Date': impression_time
                })

    return changes

# Function to write changes to a CSV file
def write_changes_to_csv(changes, output_csv):
    try:
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for change in changes:
                writer.writerow(change)
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

# Main function to execute the script
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    changes = extract_account_changes(root_dir)

    if not changes:
        # Write only the column headers if no changes are found
        changes = [{'Changed': '', 'New Value': '', 'Change Date': ''}]

    write_changes_to_csv(changes, output_csv)

if __name__ == "__main__":
    main()