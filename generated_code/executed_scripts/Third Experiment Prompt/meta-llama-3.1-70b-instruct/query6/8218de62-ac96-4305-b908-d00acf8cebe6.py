import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_account_changes(root_dir):
    account_changes = []
    account_info_file = os.path.join(root_dir, "personal_information", "account_info.json")
    
    if not os.path.exists(account_info_file):
        return account_changes
    
    with open(account_info_file, 'r') as f:
        account_info = json.load(f)
        
        for change in account_info.get("account_changes", []):
            changed = change.get("changed")
            new_value = change.get("new_value")
            change_date = datetime.fromtimestamp(change.get("change_date")).strftime('%Y-%m-%d')
            account_changes.append((changed, new_value, change_date))
    
    return account_changes

def save_to_csv(account_changes):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Changed', 'New Value', 'Change Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for change in account_changes:
            writer.writerow({'Changed': change[0], 'New Value': change[1], 'Change Date': change[2]})

def main():
    try:
        account_changes = get_account_changes(root_dir)
        save_to_csv(account_changes)
    except Exception as e:
        raise ValueError(f"Error: {e}")

if __name__ == "__main__":
    main()