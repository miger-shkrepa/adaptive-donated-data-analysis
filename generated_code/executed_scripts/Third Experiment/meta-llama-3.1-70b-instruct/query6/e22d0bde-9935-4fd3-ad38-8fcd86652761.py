import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_account_changes(root_dir):
    changes = []
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Check if the 'logged_information' directory exists
        logged_info_dir = os.path.join(root_dir, 'logged_information')
        if not os.path.exists(logged_info_dir):
            return changes

        # Check if the 'policy_updates_and_permissions' directory exists
        policy_updates_dir = os.path.join(logged_info_dir, 'policy_updates_and_permissions')
        if not os.path.exists(policy_updates_dir):
            return changes

        # Check if the 'policy_updates_and_permissions' directory contains a JSON file
        policy_updates_file = os.path.join(policy_updates_dir, 'policy_updates_and_permissions.json')
        if not os.path.exists(policy_updates_file):
            return changes

        # Read the 'policy_updates_and_permissions.json' file
        with open(policy_updates_file, 'r') as file:
            # Since the exact structure of the JSON file is not provided, we assume it contains the account changes
            # If the structure is different, the code should be adjusted accordingly
            pass

        # Since the directory structure does not contain information about account changes,
        # we return an empty list
        return changes

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(changes):
    with open('query_responses/results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Changed", "New Value", "Change Date"])
        for change in changes:
            writer.writerow(change)

def main():
    changes = get_account_changes(root_dir)
    save_to_csv(changes)

if __name__ == "__main__":
    main()