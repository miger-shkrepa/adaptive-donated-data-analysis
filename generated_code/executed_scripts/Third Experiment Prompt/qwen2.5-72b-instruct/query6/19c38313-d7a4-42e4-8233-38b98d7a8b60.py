import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv_path = 'query_responses/results.csv'

# Create the output directory if it doesn't exist
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def get_account_changes(data):
    changes = []
    try:
        profile_changes = data['personal_information']['personal_information']['profile_changes.json']
        for change in profile_changes['structure']['profile_profile_change']:
            string_map_data = change['string_map_data']
            changed = string_map_data.get('Changed', {}).get('value', '')
            new_value = string_map_data.get('New Value', {}).get('value', '')
            change_date = string_map_data.get('Change Date', {}).get('value', '')
            if change_date:
                try:
                    change_date = datetime.strptime(change_date, '%Y-%m-%d').strftime('%Y-%m-%d')
                except ValueError:
                    change_date = ''
            changes.append([changed, new_value, change_date])
    except KeyError:
        pass  # If the file or keys are missing, just continue
    return changes

def write_to_csv(changes):
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Changed', 'New Value', 'Change Date'])
        if changes:
            writer.writerows(changes)

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        personal_info_path = os.path.join(root_dir, 'personal_information', 'personal_information', 'profile_changes.json')
        if not os.path.exists(personal_info_path):
            write_to_csv([])  # Write only headers if the file is missing
            return

        personal_info_data = load_json_file(personal_info_path)
        changes = get_account_changes(personal_info_data)
        write_to_csv(changes)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()