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
                            # Since we don't have the actual JSON data, we'll assume it's in the format:
                            # {
                            #     "changes": [
                            #         {
                            #             "changed": "str",
                            #             "new_value": "str",
                            #             "change_date": "int"
                            #         }
                            #     ]
                            # }
                            # We'll also assume that the 'change_date' is a Unix timestamp
                            data = eval(f.read())
                            for change in data.get('changes', []):
                                changed = change.get('changed', '')
                                new_value = change.get('new_value', '')
                                change_date = datetime.fromtimestamp(change.get('change_date', 0)).strftime('%Y-%-%d')
                                account_changes.append((changed, new_value, change_date))

        # If no account changes were found, return an empty list
        if not account_changes:
            return []

        # Return the list of account changes
        return account_changes

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(account_changes):
    try:
        # Create the 'query_responses' directory if it doesn't exist
        query_responses_dir = 'query_responses'
        if not os.path.exists(query_responses_dir):
            os.makedirs(query_responses_dir)

        # Save the account changes to a CSV file
        with open(os.path.join(query_responses_dir, 'results.csv'), 'w', newline='') as csvfile:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for change in account_changes:
                writer.writerow({'Changed': change[0], 'New Value': change[1], 'Change Date': change[2]})

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    account_changes = get_account_changes(root_dir)
    if not account_changes:
        # If no account changes were found, save a CSV file with only the column headers
        with open(os.path.join('query_responses', 'results.csv'), 'w', newline='') as csvfile:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    else:
        save_to_csv(account_changes)

if __name__ == "__main__":
    main()