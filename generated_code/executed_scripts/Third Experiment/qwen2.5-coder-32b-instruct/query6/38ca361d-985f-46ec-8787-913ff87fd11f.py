import os
import csv
import json
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

# Function to check if the directory exists
def check_directory_exists(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Function to parse the JSON file and extract account changes
def parse_account_changes(root_dir):
    account_changes = []
    file_path = os.path.join(root_dir, "logged_information", "policy_updates_and_permissions", "notification_of_privacy_policy_updates.json")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError("FileNotFoundError: The notification_of_privacy_policy_updates.json file does not exist.")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if 'string_list_data' in data:
        for entry in data['string_list_data']:
            if 'value' in entry and 'timestamp' in entry:
                change_date = datetime.fromtimestamp(entry['timestamp']).strftime('%Y-%MM-%d')
                account_changes.append({
                    'Changed': entry['value'],
                    'New Value': entry['value'],  # Assuming 'value' contains the new value
                    'Change Date': change_date
                })
    
    return account_changes

# Main function to execute the script
def main():
    try:
        check_directory_exists(root_dir)
        account_changes = parse_account_changes(root_dir)
        
        # Writing the results to a CSV file
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for change in account_changes:
                writer.writerow(change)
    
    except FileNotFoundError as e:
        print(e)
        # Writing only the column headers if the file is not found
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

if __name__ == "__main__":
    main()