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

        # Define the path to the profile_changes.json file
        profile_changes_path = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

        # Check if the profile_changes.json file exists
        if os.path.exists(profile_changes_path):
            # Open and read the profile_changes.json file
            with open(profile_changes_path, 'r') as file:
                # Since the file structure is not provided, we assume it's a JSON file with a similar structure
                # We will iterate over each change and extract the relevant information
                import json
                data = json.load(file)
                for change in data['profile_profile_change']:
                    string_map_data = change['string_map_data']
                    changed = string_map_data.get('Changed', '')
                    new_value = string_map_data.get('New Value', '')
                    change_date = string_map_data.get('Change Date', '')
                    # Convert the change date to the required format
                    if change_date:
                        try:
                            change_date = datetime.strptime(change_date, '%Y-%m-%dT%H:%M:%S.%fZ')
                            change_date = change_date.strftime('%Y-%m-%d')
                        except ValueError:
                            # If the date is not in the expected format, skip this change
                            continue
                    account_changes.append({
                        'Changed': changed,
                        'New Value': new_value,
                        'Change Date': change_date
                    })
        else:
            # If the profile_changes.json file does not exist, return an empty list
            pass

        return account_changes

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(account_changes):
    try:
        # Define the path to the output CSV file
        output_path = 'query_responses/results.csv'

        # Create the output directory if it does not exist
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Open and write to the output CSV file
        with open(output_path, 'w', newline='') as file:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for change in account_changes:
                writer.writerow(change)

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        account_changes = get_account_changes(root_dir)
        if not account_changes:
            # If no account changes are found, save a CSV file with only the column headers
            with open('query_responses/results.csv', 'w', newline='') as file:
                fieldnames = ['Changed', 'New Value', 'Change Date']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
        else:
            save_to_csv(account_changes)
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()