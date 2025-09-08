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
                # Since the file structure is not provided, we assume it's a simple JSON file
                # with the structure: {"profile_profile_change": [...]}

                # Try to parse the JSON file
                try:
                    import json
                    data = json.load(file)
                    profile_changes = data.get("profile_profile_change", [])

                    # Iterate over each profile change
                    for change in profile_changes:
                        string_map_data = change.get("string_map_data", {})
                        changed = string_map_data.get("Changed", "")
                        new_value = string_map_data.get("New Value", "")
                        change_date = string_map_data.get("Change Date", "")

                        # Try to parse the change date
                        try:
                            change_date = datetime.strptime(change_date, "%Y-%m-%d %H:%M:%S")
                            change_date = change_date.strftime("%Y-%m-%d")
                        except ValueError:
                            change_date = ""

                        # Add the account change to the list
                        account_changes.append({
                            "Changed": changed,
                            "New Value": new_value,
                            "Change Date": change_date
                        })

                except json.JSONDecodeError:
                    raise ValueError("ValueError: The profile_changes.json file is not a valid JSON file.")

        # Return the list of account changes
        return account_changes

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def save_account_changes_to_csv(account_changes):
    try:
        # Define the path to the output CSV file
        output_csv_path = "query_responses/results.csv"

        # Create the output CSV file
        with open(output_csv_path, 'w', newline='') as file:
            # Create a CSV writer
            writer = csv.DictWriter(file, fieldnames=["Changed", "New Value", "Change Date"])

            # Write the header
            writer.writeheader()

            # Write each account change
            for change in account_changes:
                writer.writerow(change)

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def main():
    try:
        account_changes = get_account_changes(root_dir)

        # If no account changes are found, create a CSV file with only the column headers
        if not account_changes:
            account_changes = [{"Changed": "", "New Value": "", "Change Date": ""}]

        save_account_changes_to_csv(account_changes)

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()