import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_account_changes(root_dir):
    account_changes = []
    profile_changes_file = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")
    
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")
    
    if not os.path.exists(profile_changes_file):
        return account_changes
    
    with open(profile_changes_file, 'r') as f:
        data = json.load(f)
        
        for change in data["profile_profile_change"]:
            changed = change["string_map_data"]["Changed"]["value"]
            new_value = change["string_map_data"]["New Value"]["value"]
            change_date = datetime.fromtimestamp(change["string_map_data"]["Change Date"]["timestamp"]).strftime('%Y-%m-%d')
            
            account_changes.append([changed, new_value, change_date])
    
    return account_changes

def save_to_csv(account_changes):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Changed", "New Value", "Change Date"])  # header
        writer.writerows(account_changes)

def main():
    try:
        account_changes = get_account_changes(root_dir)
        save_to_csv(account_changes)
    except Exception as e:
        raise Exception("Error: " + str(e))

if __name__ == "__main__":
    main()