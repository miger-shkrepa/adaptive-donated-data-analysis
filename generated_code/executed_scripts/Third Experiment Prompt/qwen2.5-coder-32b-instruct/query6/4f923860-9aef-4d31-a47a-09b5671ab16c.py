import os
import csv
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

def get_profile_changes_file_path(root_dir):
    return os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

def read_json_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    
    with open(file_path, 'r') as file:
        import json
        return json.load(file)

def extract_changes(data):
    changes = []
    if "profile_profile_change" in data:
        for change in data["profile_profile_change"]:
            string_map_data = change.get("string_map_data", {})
            change_date = string_map_data.get("Change Date", {}).get("value", "")
            changed = string_map_data.get("Changed", {}).get("value", "")
            new_value = string_map_data.get("New Value", {}).get("value", "")
            
            if change_date:
                try:
                    change_date = datetime.strptime(change_date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
                except ValueError:
                    raise ValueError(f"ValueError: The date format in {change_date} is incorrect.")
            
            changes.append((changed, new_value, change_date))
    
    return changes

def write_csv(changes, output_path):
    with open(output_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Changed", "New Value", "Change Date"])
        csvwriter.writerows(changes)

def main():
    try:
        profile_changes_file_path = get_profile_changes_file_path(root_dir)
        data = read_json_file(profile_changes_file_path)
        changes = extract_changes(data)
        write_csv(changes, "query_responses/results.csv")
    except FileNotFoundError as e:
        write_csv([], "query_responses/results.csv")
        print(e)
    except ValueError as e:
        write_csv([], "query_responses/results.csv")
        print(e)

if __name__ == "__main__":
    main()