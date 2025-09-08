import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# Function to parse JSON files and extract account changes
def extract_account_changes(directory):
    changes = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Assuming the JSON structure contains account details
                        if 'account_details' in data:
                            for detail in data['account_details']:
                                changes.append({
                                    'Changed': detail['field'],
                                    'New Value': detail['new_value'],
                                    'Change Date': detail['change_date']
                                })
                except FileNotFoundError:
                    raise FileNotFoundError(f"Error: FileNotFoundError: The file {file_path} does not exist.")
                except json.JSONDecodeError:
                    raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON.")
    return changes

# Function to write changes to CSV
def write_changes_to_csv(changes, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Changed', 'New Value', 'Change Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for change in changes:
            writer.writerow(change)

# Main function to process the directory and generate the CSV
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: FileNotFoundError: The root directory does not exist.")

    changes = extract_account_changes(root_dir)
    write_changes_to_csv(changes, output_csv)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)