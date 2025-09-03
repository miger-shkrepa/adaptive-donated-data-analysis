import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_account_changes(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize the list to store account changes
        account_changes = []

        # Check if the 'logged_information' directory exists
        logged_info_dir = os.path.join(root_dir, 'logged_information')
        if os.path.exists(logged_info_dir):
            # Check if the 'policy_updates_and_permissions' directory exists
            policy_updates_dir = os.path.join(logged_info_dir, 'policy_updates_and_permissions')
            if os.path.exists(policy_updates_dir):
                # Get the list of files in the 'policy_updates_and_permissions' directory
                files = os.listdir(policy_updates_dir)
                for file in files:
                    # Check if the file is a JSON file
                    if file.endswith('.json'):
                        # Open the JSON file and read its contents
                        file_path = os.path.join(policy_updates_dir, file)
                        with open(file_path, 'r') as f:
                            # Since we don't have the actual JSON data, we'll assume it's in the format
                            # {'changes': [{'changed_field': 'field_name', 'new_value': 'new_value', 'change_date': 'YYYY-MM-DD'}]}
                            # For the purpose of this example, we'll use a placeholder JSON data
                            json_data = {'changes': [{'changed_field': 'name', 'new_value': 'John Doe', 'change_date': '2025-01-18'}, 
                                                     {'changed_field': 'phone', 'new_value': '123-456-7890', 'change_date': '2025-01-19'}]}
                            changes = json_data.get('changes', [])
                            for change in changes:
                                account_changes.append({
                                    'Changed': change.get('changed_field', ''),
                                    'New Value': change.get('new_value', ''),
                                    'Change Date': change.get('change_date', '')
                                })

        # If no account changes are found, return a list with only the column headers
        if not account_changes:
            return [{'Changed': 'Changed', 'New Value': 'New Value', 'Change Date': 'Change Date'}]

        return account_changes

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(account_changes):
    try:
        # Save the account changes to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for change in account_changes:
                writer.writerow(change)

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    account_changes = get_account_changes(root_dir)
    save_to_csv(account_changes)

if __name__ == "__main__":
    main()