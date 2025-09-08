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

def get_account_changes():
    try:
        changes = []
        account_history_path = os.path.join(root_dir, "security_and_login_information", "login_and_profile_creation", "instagram_signup_details.json")
        if not os.path.exists(account_history_path):
            return []

        account_history = load_json(account_history_path)
        for entry in account_history.get("account_history_registration_info", []):
            string_map_data = entry.get("string_map_data", {})
            for key, value in string_map_data.items():
                if key in ["Name", "Phone Number", "Email"]:
                    changes.append({
                        "Changed": key,
                        "New Value": value.get("value"),
                        "Change Date": datetime.fromtimestamp(value.get("timestamp")).strftime('%Y-%m-%d')
                    })
        return changes
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def write_to_csv(changes):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Changed', 'New Value', 'Change Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for change in changes:
            writer.writerow(change)

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")
    
    try:
        changes = get_account_changes()
        write_to_csv(changes)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()