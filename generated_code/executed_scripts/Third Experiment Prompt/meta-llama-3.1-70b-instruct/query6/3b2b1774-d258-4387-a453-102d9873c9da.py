import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_account_changes(root_dir):
    changes = []
    account_info_file = os.path.join(root_dir, "personal_information", "personal_information", "instagram_profile_information.json")
    
    if not os.path.exists(account_info_file):
        raise FileNotFoundError("FileNotFoundError: The instagram_profile_information.json file does not exist.")
    
    with open(account_info_file, 'r') as f:
        data = json.load(f)
        
        for account_info in data["profile_account_insights"]:
            for key, value in account_info["string_map_data"].items():
                if key in ["Name", "Phone Number", "Email"]:
                    change_date = datetime.fromtimestamp(value["timestamp"]).strftime('%Y-%m-%d')
                    changes.append({"Changed": key, "New Value": value["value"], "Change Date": change_date})
    
    return changes

def save_to_csv(changes):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ["Changed", "New Value", "Change Date"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for change in changes:
            writer.writerow(change)

try:
    changes = get_account_changes(root_dir)
    save_to_csv(changes)
except FileNotFoundError as e:
    raise FileNotFoundError("Error: " + str(e))
except Exception as e:
    raise ValueError("Error: " + str(e))