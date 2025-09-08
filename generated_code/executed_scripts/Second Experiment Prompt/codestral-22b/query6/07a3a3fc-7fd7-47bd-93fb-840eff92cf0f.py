import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"
output_file = "query_responses/results.csv"

def parse_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

def get_account_changes(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    account_changes = []
    profile_changes_path = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

    if not os.path.exists(profile_changes_path):
        return account_changes

    with open(profile_changes_path, 'r') as f:
        data = json.load(f)

    for change in data.get("profile_profile_change", []):
        changed = change["string_map_data"]["Changed"]["value"]
        new_value = change["string_map_data"].get("New Value", {}).get("value", "")
        change_date = parse_date(change["string_map_data"]["Change Date"]["timestamp"])

        account_changes.append([changed, new_value, change_date])

    return account_changes

def write_to_csv(account_changes, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Changed", "New Value", "Change Date"])
        writer.writerows(account_changes)

account_changes = get_account_changes(root_dir)
write_to_csv(account_changes, output_file)