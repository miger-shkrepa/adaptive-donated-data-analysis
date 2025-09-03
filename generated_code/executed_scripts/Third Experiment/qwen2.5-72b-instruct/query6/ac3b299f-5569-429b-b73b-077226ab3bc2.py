import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")

def get_account_changes(data):
    changes = []
    try:
        account_history = data["account_history_registration_info"][0]["string_map_data"]
        for key, value in account_history.items():
            if key in ["Benutzername", "E-Mail-Adresse", "Telefonnummer"]:
                changes.append({
                    "Changed": key,
                    "New Value": value["value"],
                    "Change Date": datetime.fromtimestamp(value["timestamp"] / 1000).strftime('%Y-%m-%d')
                })
    except KeyError:
        raise ValueError("Error: The required data structure is not found in the JSON file.")
    return changes

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
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        json_file_path = os.path.join(root_dir, "account_history_registration_info.json")
        if not os.path.exists(json_file_path):
            write_to_csv([])
            return
        
        data = load_json_data(json_file_path)
        changes = get_account_changes(data)
        write_to_csv(changes)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()