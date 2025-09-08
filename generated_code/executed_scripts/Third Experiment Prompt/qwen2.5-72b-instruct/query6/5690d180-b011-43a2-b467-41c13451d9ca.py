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
        personal_info_path = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")
        if not os.path.exists(personal_info_path):
            return changes

        data = load_json_file(personal_info_path)
        profile_changes = data.get("profile_profile_change", [])

        for change in profile_changes:
            string_map_data = change.get("string_map_data", {})
            changed = string_map_data.get("Changed", {}).get("value", "")
            new_value = string_map_data.get("New Value", {}).get("value", "")
            change_date = string_map_data.get("Change Date", {}).get("value", "")

            if change_date:
                try:
                    change_date = datetime.strptime(change_date, "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    change_date = ""

            changes.append((changed, new_value, change_date))

    except Exception as e:
        print(f"Error: {e}")

    return changes

def save_to_csv(changes):
    output_path = "query_responses/results.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Changed", "New Value", "Change Date"])
        csvwriter.writerows(changes)

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    account_changes = get_account_changes()
    save_to_csv(account_changes)

if __name__ == "__main__":
    main()