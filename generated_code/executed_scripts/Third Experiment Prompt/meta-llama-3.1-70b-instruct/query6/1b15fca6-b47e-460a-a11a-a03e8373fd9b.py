import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_account_changes(root_dir):
    changes = []
    profile_changes_file = os.path.join(root_dir, "personal_information", "profile_changes.json")
    
    if not os.path.exists(profile_changes_file):
        return changes
    
    with open(profile_changes_file, 'r') as f:
        data = json.load(f)
        
        for change in data["profile_profile_change"]:
            changed = change["string_map_data"]["Changed"]["value"]
            new_value = change["string_map_data"]["New Value"]["value"]
            change_date = datetime.fromtimestamp(change["string_map_data"]["Change Date"]["timestamp"]).strftime('%Y-%m-%d')
            
            changes.append([changed, new_value, change_date])
    
    return changes

def save_to_csv(changes):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Changed", "New Value", "Change Date"])  # header
        writer.writerows(changes)

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        changes = get_account_changes(root_dir)
        save_to_csv(changes)
    
    except FileNotFoundError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Changed", "New Value", "Change Date"])  # header
    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()