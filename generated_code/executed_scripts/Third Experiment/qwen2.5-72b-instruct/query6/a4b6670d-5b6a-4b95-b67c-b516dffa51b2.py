import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")

def get_instagram_changes():
    try:
        signup_details_path = os.path.join(root_dir, "personal_information", "signup_details.json")
        personal_info_path = os.path.join(root_dir, "personal_information", "personal_information.json")

        signup_details = load_json(signup_details_path) if os.path.exists(signup_details_path) else {}
        personal_info = load_json(personal_info_path) if os.path.exists(personal_info_path) else {}

        changes = []

        if 'account_history_registration_info' in signup_details:
            for entry in signup_details['account_history_registration_info']:
                string_map_data = entry.get('string_map_data', {})
                timestamp = string_map_data.get('Time', {}).get('timestamp')
                if timestamp:
                    change_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                    for key, value in string_map_data.items():
                        if key in ['Email', 'Phone Number', 'Username']:
                            changes.append([key, value.get('value'), change_date])

        if 'profile_user' in personal_info:
            for entry in personal_info['profile_user']:
                string_map_data = entry.get('string_map_data', {})
                for key, value in string_map_data.items():
                    if key in ['Bio', 'Date of birth']:
                        timestamp = value.get('timestamp')
                        if timestamp:
                            change_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                            changes.append([key, value.get('value'), change_date])

        return changes

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def write_to_csv(changes):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Changed', 'New Value', 'Change Date'])
        if not changes:
            return
        csvwriter.writerows(changes)

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")
    
    try:
        changes = get_instagram_changes()
        write_to_csv(changes)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()