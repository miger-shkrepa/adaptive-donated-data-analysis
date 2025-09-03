import os
import json
import csv
from datetime import datetime

def parse_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON file.")

def extract_changes(root_dir):
    changes = []

    # Define the paths to the relevant JSON files
    profile_info_path = os.path.join(root_dir, 'personal_information', 'instagram_profile_information.json')

    try:
        profile_info = parse_json_file(profile_info_path)
        for entry in profile_info.get('profile_account_insights', []):
            string_map_data = entry.get('string_map_data', {})
            for key, value in string_map_data.items():
                if key in ['Contact Syncing', 'First Close Friends Story Time', 'First Country Code', 'First Story Time', 'Has Shared Live Video', 'Last Login', 'Last Logout', 'Last Story Time']:
                    timestamp = value.get('timestamp')
                    if timestamp:
                        change_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                        changes.append({
                            'Changed': key,
                            'New Value': value.get('value'),
                            'Change Date': change_date
                        })
    except FileNotFoundError:
        # If the file is not found, continue with an empty changes list
        pass

    return changes

def write_csv(changes, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for change in changes:
                writer.writerow(change)
    except Exception as e:
        raise ValueError(f"Error: ValueError: Failed to write CSV file. {str(e)}")

def main():
    root_dir = "root_dir"
    output_path = 'query_responses/results.csv'

    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: FileNotFoundError: The root directory does not exist.")

    changes = extract_changes(root_dir)
    write_csv(changes, output_path)

if __name__ == "__main__":
    main()