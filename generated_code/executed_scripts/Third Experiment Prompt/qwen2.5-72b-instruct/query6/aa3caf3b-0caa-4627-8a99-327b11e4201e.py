import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Function to parse the JSON file and extract the required data
def extract_account_changes(json_data):
    changes = []
    if "profile_profile_change" in json_data:
        for change in json_data["profile_profile_change"]:
            string_map_data = change.get("string_map_data", {})
            changed = string_map_data.get("Changed", {}).get("value", "")
            new_value = string_map_data.get("New Value", {}).get("value", "")
            change_date = string_map_data.get("Change Date", {}).get("value", "")
            if change_date:
                try:
                    change_date = datetime.strptime(change_date, "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    change_date = ""
            changes.append((changed, new_value, change_date))
    return changes

# Function to write the data to a CSV file
def write_to_csv(changes):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Changed', 'New Value', 'Change Date'])
        if changes:
            csvwriter.writerows(changes)

# Main function to process the data
def process_account_changes(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        personal_info_path = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")
        
        if not os.path.exists(personal_info_path):
            write_to_csv([])
            return
        
        with open(personal_info_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        
        changes = extract_account_changes(json_data)
        write_to_csv(changes)
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: {e}")

# Execute the main function
process_account_changes(root_dir)