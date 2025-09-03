import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to parse JSON files and extract relevant information
def parse_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON file.")

# Function to extract changes from the JSON data
def extract_changes(data):
    changes = []
    for entry in data:
        for item in entry.get('string_list_data', []):
            changes.append({
                'Changed': item['value'],
                'New Value': item['value'],
                'Change Date': datetime.fromtimestamp(item['timestamp']).strftime('%Y-%m-%d')
            })
    return changes

# Main function to process the directory and extract account changes
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: FileNotFoundError: The root directory does not exist.")

    changes = []

    # Define the paths to the relevant JSON files
    files_to_check = [
        os.path.join(root_dir, 'personal_information', 'information_about_you', 'account_based_in.json')
    ]

    for file_path in files_to_check:
        if os.path.exists(file_path):
            data = parse_json_file(file_path)
            changes.extend(extract_changes(data))

    # Write the results to a CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Changed', 'New Value', 'Change Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for change in changes:
            writer.writerow(change)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)