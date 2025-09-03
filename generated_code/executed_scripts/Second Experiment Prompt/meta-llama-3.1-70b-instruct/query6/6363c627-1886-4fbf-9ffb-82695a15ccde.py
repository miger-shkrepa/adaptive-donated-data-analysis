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
            # Open the profile_changes.json file
            with open(profile_changes_path, 'r') as file:
                # Load the JSON data
                import json
                data = json.load(file)

                # Iterate over the profile changes
                for change in data["profile_profile_change"]:
                    # Extract the change date, changed field, and new value
                    change_date = change["string_map_data"]["Change Date"]["value"]
                    changed = change["string_map_data"]["Changed"]["value"]
                    new_value = change["string_map_data"]["New Value"]["value"]

                    # Convert the change date to the required format
                    try:
                        change_date = datetime.strptime(change_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                        change_date = change_date.strftime("%Y-%m-%d")
                    except ValueError:
                        # If the date is not in the expected format, skip this change
                        continue

                    # Add the change to the list
                    account_changes.append((changed, new_value, change_date))

        # Return the list of account changes
        return account_changes

    except Exception as e:
        # Raise a ValueError with the error message
        raise ValueError("Error: " + str(e))

def save_account_changes_to_csv(account_changes):
    try:
        # Define the path to the output CSV file
        output_path = "query_responses/results.csv"

        # Create the output directory if it does not exist
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Open the output CSV file
        with open(output_path, 'w', newline='') as file:
            # Create a CSV writer
            writer = csv.writer(file)

            # Write the column headers
            writer.writerow(["Changed", "New Value", "Change Date"])

            # Write the account changes
            for change in account_changes:
                writer.writerow(change)

    except Exception as e:
        # Raise a ValueError with the error message
        raise ValueError("Error: " + str(e))

def main():
    try:
        # Get the account changes
        account_changes = get_account_changes(root_dir)

        # Save the account changes to a CSV file
        save_account_changes_to_csv(account_changes)

    except FileNotFoundError as e:
        # If the root directory does not exist, create an empty CSV file
        with open("query_responses/results.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Changed", "New Value", "Change Date"])
        print(e)
    except Exception as e:
        # Print the error message
        print("Error: " + str(e))

if __name__ == "__main__":
    main()