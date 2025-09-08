import os
import json
from datetime import datetime
import csv

root_dir = "root_dir"
output_file = "query_responses/results.csv"

def convert_timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

def get_account_changes(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    account_changes = []
    profile_changes_path = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

    if os.path.exists(profile_changes_path):
        with open(profile_changes_path, 'r') as f:
            data = json.load(f)
            for change in data["profile_profile_change"]:
                changed = change["string_map_data"]["Changed"]["value"]
                new_value = change["string_map_data"]["New Value"]["value"]
                change_date = convert_timestamp_to_date(change["string_map_data"]["Change Date"]["timestamp"])
                account_changes.append([changed, new_value, change_date])

    return account_changes

def write_to_csv(account_changes, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Changed", "New Value", "Change Date"])
        writer.writerows(account_changes)

account_changes = get_account_changes(root_dir)
write_to_csv(account_changes, output_file)