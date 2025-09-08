import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON file.")

def get_account_changes():
    changes = []

    try:
        personal_info_path = os.path.join(root_dir, "personal_information", "personal_information", "personal_information.json")
        if not os.path.exists(personal_info_path):
            return changes

        personal_info = load_json_file(personal_info_path)
        account_changes = personal_info.get("personal_information", {}).get("personal_information", {}).get("profile_user", [])

        for change in account_changes:
            string_map_data = change.get("string_map_data", {})
            for key, value in string_map_data.items():
                timestamp = value.get("timestamp")
                if timestamp:
                    change_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                    changes.append([key, value.get("value"), change_date])

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

    return changes

def save_to_csv(changes):
    csv_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Changed', 'New Value', 'Change Date'])
        csvwriter.writerows(changes)

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    try:
        account_changes = get_account_changes()
        save_to_csv(account_changes)
    except Exception as e:
        print(str(e))
        save_to_csv([])

if __name__ == "__main__":
    main()