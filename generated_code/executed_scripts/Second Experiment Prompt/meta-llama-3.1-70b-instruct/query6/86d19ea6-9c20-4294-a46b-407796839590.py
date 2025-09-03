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
            try:
                # Open and read the profile_changes.json file
                with open(profile_changes_path, 'r') as file:
                    # Since the file structure is not provided, we assume it's a simple JSON file
                    # and we will parse it manually
                    for line in file:
                        # Remove leading and trailing whitespaces
                        line = line.strip()
                        # Check if the line contains a change
                        if "Changed" in line and "New Value" in line and "Change Date" in line:
                            # Extract the change, new value, and change date
                            changed = line.split("Changed")[1].split(",")[0].strip().replace('"', '')
                            new_value = line.split("New Value")[1].split(",")[0].strip().replace('"', '')
                            change_date = line.split("Change Date")[1].split(",")[0].strip().replace('"', '')
                            # Convert the change date to the required format
                            change_date = datetime.strptime(change_date, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d')
                            # Append the change to the list
                            account_changes.append([changed, new_value, change_date])
            except Exception as e:
                raise ValueError("ValueError: Failed to parse the profile_changes.json file. " + str(e))
        else:
            # If the profile_changes.json file does not exist, return an empty list
            pass

        return account_changes

    except Exception as e:
        raise Exception("Error: " + str(e))

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
        raise Exception("Error: Failed to save the results to the CSV file. " + str(e))

def main():
    try:
        account_changes = get_account_changes(root_dir)
        if not account_changes:
            # If no account changes are found, save a CSV file with only the column headers
            save_to_csv([["Changed", "New Value", "Change Date"]])
        else:
            save_to_csv(account_changes)
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()