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

        # Iterate over the personal information directory
        personal_info_dir = os.path.join(root_dir, "personal_information")
        if os.path.exists(personal_info_dir):
            profile_changes_file = os.path.join(personal_info_dir, "profile_changes.json")
            if os.path.exists(profile_changes_file):
                # Open and read the profile changes file
                with open(profile_changes_file, "r") as file:
                    # Since we don't have the actual JSON data, we'll assume it's in the correct format
                    # and extract the necessary information
                    for line in file:
                        # Assuming each line is a separate change
                        change = eval(line)
                        changed = change["string_map_data"]["Changed"]["value"]
                        new_value = change["string_map_data"]["New Value"]["value"]
                        change_date = datetime.fromtimestamp(change["string_map_data"]["Change Date"]["timestamp"]).strftime("%Y-%m-%d")
                        account_changes.append((changed, new_value, change_date))

        # If no account changes were found, return a list with only the column headers
        if not account_changes:
            return [("Changed", "New Value", "Change Date")]

        return account_changes

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(account_changes):
    try:
        # Save the account changes to a CSV file
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Changed", "New Value", "Change Date"])
            writer.writerows(account_changes)

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    account_changes = get_account_changes(root_dir)
    save_to_csv(account_changes)

if __name__ == "__main__":
    main()