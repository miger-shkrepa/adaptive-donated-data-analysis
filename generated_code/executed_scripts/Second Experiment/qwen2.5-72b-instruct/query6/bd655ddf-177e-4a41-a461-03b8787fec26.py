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
        raise FileNotFoundError("Error: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def get_instagram_changes():
    try:
        personal_info_path = os.path.join(root_dir, "personal_information", "personal_information.json")
        if not os.path.exists(personal_info_path):
            return []

        personal_info = load_json(personal_info_path)
        changes = []

        for profile in personal_info.get("profile_user", []):
            string_map_data = profile.get("string_map_data", {})
            for key, value in string_map_data.items():
                if key in ["Bio", "Date of birth"]:
                    timestamp = value.get("timestamp")
                    if timestamp:
                        change_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                        changes.append([key, value.get("value"), change_date])

        return changes

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def write_to_csv(changes):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Changed", "New Value", "Change Date"])
        if changes:
            writer.writerows(changes)

try:
    changes = get_instagram_changes()
    write_to_csv(changes)
except Exception as e:
    print(str(e))
    write_to_csv([])