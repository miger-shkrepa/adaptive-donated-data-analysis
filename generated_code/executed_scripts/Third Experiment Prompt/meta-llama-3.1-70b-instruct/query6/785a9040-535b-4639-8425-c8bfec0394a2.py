import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_account_changes(root_dir):
    account_changes = []
    try:
        personal_info_dir = os.path.join(root_dir, "personal_information")
        if not os.path.exists(personal_info_dir):
            raise FileNotFoundError("Error: The personal information directory does not exist.")
        
        device_info_dir = os.path.join(personal_info_dir, "device_information")
        if not os.path.exists(device_info_dir):
            raise FileNotFoundError("Error: The device information directory does not exist.")
        
        # Assuming account changes are stored in a file named "account_changes.json" in the device information directory
        account_changes_file = os.path.join(device_info_dir, "account_changes.json")
        if not os.path.exists(account_changes_file):
            return account_changes  # Return an empty list if the file does not exist
        
        with open(account_changes_file, "r") as f:
            account_changes_data = json.load(f)
            for change in account_changes_data:
                changed = change["field"]
                new_value = change["new_value"]
                change_date = datetime.fromtimestamp(change["timestamp"]).strftime("%Y-%m-%d")
                account_changes.append((changed, new_value, change_date))
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: Failed to parse JSON file: {e}")
    except Exception as e:
        raise ValueError(f"Error: An unexpected error occurred: {e}")
    
    return account_changes

def write_csv(account_changes):
    csv_file = "query_responses/results.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Changed", "New Value", "Change Date"])  # Write header
        for change in account_changes:
            writer.writerow(change)

if __name__ == "__main__":
    account_changes = get_account_changes(root_dir)
    write_csv(account_changes)