import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_account_changes(root_dir):
    account_changes = []
    account_info_file = os.path.join(root_dir, "personal_information", "personal_information", "account_information.json")
    
    if not os.path.exists(account_info_file):
        raise FileNotFoundError("FileNotFoundError: The account information file does not exist.")
    
    with open(account_info_file, 'r') as f:
        account_info = json.load(f)
    
    for change in account_info["profile_account_insights"]:
        for key, value in change["string_map_data"].items():
            if key in ["Name", "Telefonnummer", "E-Mail-Adresse"]:
                account_changes.append({
                    "Changed": key,
                    "New Value": value["value"],
                    "Change Date": datetime.fromtimestamp(value["timestamp"]).strftime("%Y-%m-%d")
                })
    
    return account_changes

def save_to_csv(account_changes):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ["Changed", "New Value", "Change Date"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for change in account_changes:
            writer.writerow(change)

try:
    account_changes = get_account_changes(root_dir)
    save_to_csv(account_changes)
except FileNotFoundError as e:
    raise FileNotFoundError("Error: " + str(e))
except Exception as e:
    raise ValueError("Error: " + str(e))