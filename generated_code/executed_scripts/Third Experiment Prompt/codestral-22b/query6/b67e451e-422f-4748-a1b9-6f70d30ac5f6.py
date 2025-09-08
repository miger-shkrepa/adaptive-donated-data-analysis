import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def parse_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

def get_account_changes(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    account_changes = []
    personal_info_path = os.path.join(root_dir, "personal_information", "personal_information", "personal_information.json")

    if os.path.exists(personal_info_path):
        with open(personal_info_path, 'r') as f:
            data = json.load(f)

        for change in data["profile_user"]:
            for key, value in change["string_map_data"].items():
                account_changes.append({
                    "Changed": key,
                    "New Value": value["value"],
                    "Change Date": parse_date(value["timestamp"])
                })

    return account_changes

def save_to_csv(data, output_path):
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Changed", "New Value", "Change Date"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

try:
    account_changes = get_account_changes(root_dir)
    save_to_csv(account_changes, "query_responses/results.csv")
except Exception as e:
    print(f"Error: {str(e)}")