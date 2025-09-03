import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to parse the JSON file and extract relevant data
def parse_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to extract account changes from the data
def extract_account_changes(data):
    changes = []
    for entry in data.get('account_history_registration_info', []):
        string_map_data = entry.get('string_map_data', {})
        for key, value in string_map_data.items():
            if key in ['Benutzername', 'E-Mail-Adresse', 'Telefonnummer']:
                changes.append({
                    'Changed': key,
                    'New Value': value.get('value', ''),
                    'Change Date': datetime.fromtimestamp(value.get('timestamp', 0)).strftime('%Y-%m-%d')
                })
    return changes

# Function to write the results to a CSV file
def write_to_csv(changes, output_csv):
    try:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for change in changes:
                writer.writerow(change)
    except Exception as e:
        raise ValueError(f"ValueError: Failed to write to CSV file. {str(e)}")

# Main function to process the directory and extract account changes
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Path to the JSON file containing account history registration info
    account_history_file = os.path.join(root_dir, 'account_history_registration_info.json')

    # Check if the file exists
    if not os.path.exists(account_history_file):
        # If the file does not exist, create a CSV with only the column headers
        write_to_csv([], output_csv)
        return

    # Parse the JSON file
    data = parse_json_file(account_history_file)

    # Extract account changes
    changes = extract_account_changes(data)

    # Write the results to a CSV file
    write_to_csv(changes, output_csv)

if __name__ == "__main__":
    main()