import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_account_changes(root_dir):
    changes = []
    profile_changes_file = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")
    
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")
    
    if not os.path.exists(profile_changes_file):
        # If the file is missing, return an empty list
        return changes
    
    try:
        with open(profile_changes_file, 'r') as f:
            data = json.load(f)
            for change in data["profile_profile_change"]:
                changed = change["string_map_data"]["Changed"]["value"]
                new_value = change["string_map_data"]["New Value"]["value"]
                change_date = datetime.fromtimestamp(change["string_map_data"]["Change Date"]["timestamp"]).strftime('%Y-%m-%d')
                changes.append((changed, new_value, change_date))
    except json.JSONDecodeError as e:
        raise ValueError("Error: Failed to parse JSON file: {}".format(e))
    
    return changes

def save_to_csv(changes):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Changed', 'New Value', 'Change Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for change in changes:
            writer.writerow({'Changed': change[0], 'New Value': change[1], 'Change Date': change[2]})

try:
    changes = get_account_changes(root_dir)
    save_to_csv(changes)
except Exception as e:
    print("Error: {}".format(e))