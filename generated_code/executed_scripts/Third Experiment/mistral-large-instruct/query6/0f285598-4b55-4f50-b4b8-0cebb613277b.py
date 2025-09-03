import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to parse JSON files and extract relevant data
def parse_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to extract account changes from the JSON data
def extract_account_changes(data):
    changes = []
    for entry in data.get('account_history_registration_info', []):
        string_map_data = entry.get('string_map_data', {})
        for key, value in string_map_data.items():
            if key in ['Name', 'Phone Number', 'Email']:
                timestamp = value.get('timestamp')
                new_value = value.get('value')
                if timestamp and new_value:
                    change_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                    changes.append((key, new_value, change_date))
    return changes

# Function to write the results to a CSV file
def write_to_csv(changes):
    try:
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Changed', 'New Value', 'Change Date'])
            for change in changes:
                writer.writerow(change)
    except Exception as e:
        raise ValueError(f"ValueError: Failed to write to CSV file. {str(e)}")

# Main function to process the directory and extract account changes
def main():
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Define the path to the JSON file containing account changes
        account_changes_file = os.path.join(root_dir, 'security_and_login_information', 'login_and_profile_creation', 'instagram_signup_details.json')

        # Parse the JSON file and extract account changes
        data = parse_json_file(account_changes_file)
        changes = extract_account_changes(data)

        # Write the results to a CSV file
        write_to_csv(changes)

    except Exception as e:
        print(f"Error: {str(e)}")

# Run the main function
if __name__ == "__main__":
    main()