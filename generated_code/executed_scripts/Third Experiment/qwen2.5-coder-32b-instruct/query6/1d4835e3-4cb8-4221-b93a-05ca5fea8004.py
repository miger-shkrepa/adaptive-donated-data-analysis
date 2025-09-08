import os
import csv
from datetime import datetime

root_dir = "root_dir"

def convert_timestamp_to_date(timestamp):
    try:
        return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')
    except ValueError:
        raise ValueError("Error: Invalid timestamp format.")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        profile_changes_path = os.path.join(root_dir, "personal_information", "profile_changes.json")
        
        if not os.path.exists(profile_changes_path):
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Changed', 'New Value', 'Change Date'])
            return
        
        with open(profile_changes_path, 'r') as file:
            import json
            data = json.load(file)
        
        if 'profile_profile_change' not in data['structure']:
            raise ValueError("Error: The required data structure is missing.")
        
        changes = data['structure']['profile_profile_change']
        
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Changed', 'New Value', 'Change Date'])
            
            for change in changes:
                string_map_data = change['string_map_data']
                changed = string_map_data['Changed']['value']
                new_value = string_map_data['New Value']['value']
                change_date = convert_timestamp_to_date(string_map_data['Change Date']['timestamp'])
                
                writer.writerow([changed, new_value, change_date])
    
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()