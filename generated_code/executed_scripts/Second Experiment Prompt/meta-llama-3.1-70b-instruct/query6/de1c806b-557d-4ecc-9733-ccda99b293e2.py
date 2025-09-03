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
                # and we will parse it manually
                lines = file.readlines()
                for line in lines:
                    # We are looking for lines that contain "Changed", "New Value" and "Change Date"
                    if "Changed" in line and "New Value" in line and "Change Date" in line:
                        # Extract the values
                        changed = line.split('"Changed":')[1].split(',')[0].strip().replace('"', '')
                        new_value = line.split('"New Value":')[1].split(',')[0].strip().replace('"', '')
                        change_date = line.split('"Change Date":')[1].split(',')[0].strip().replace('"', '')
                        # Convert the change date to the required format
                        try:
                            change_date = datetime.strptime(change_date, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d')
                        except ValueError:
                            # If the date is not in the expected format, skip this line
                            continue
                        # Add the change to the list
                        account_changes.append((changed, new_value, change_date))

        # Return the list of account changes
        return account_changes

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(account_changes):
    try:
        # Define the path to the output CSV file
        output_path = "query_responses/results.csv"

        # Create the output directory if it does not exist
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Open and write to the output CSV file
        with open(output_path, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(["Changed", "New Value", "Change Date"])
            # Write the account changes
            for change in account_changes:
                writer.writerow(change)

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        account_changes = get_account_changes(root_dir)
        if not account_changes:
            # If no account changes are found, write only the header to the CSV file
            with open("query_responses/results.csv", 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Changed", "New Value", "Change Date"])
        else:
            save_to_csv(account_changes)

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()