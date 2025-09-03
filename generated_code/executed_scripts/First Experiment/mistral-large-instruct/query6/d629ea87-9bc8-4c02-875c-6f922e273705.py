import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to parse JSON files and extract relevant information
def parse_json_files(directory):
    changes = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        changes.extend(extract_changes(data))
                except FileNotFoundError:
                    raise FileNotFoundError(f"Error: FileNotFoundError: The file {file_path} does not exist.")
                except json.JSONDecodeError:
                    raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON.")
    return changes

# Function to extract changes from JSON data
def extract_changes(data):
    changes = []
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict) and 'timestamp' in value and 'value' in value:
                timestamp = value['timestamp']
                new_value = value['value']
                change_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                changes.append((key, new_value, change_date))
            elif isinstance(value, (dict, list)):
                changes.extend(extract_changes(value))
    elif isinstance(data, list):
        for item in data:
            changes.extend(extract_changes(item))
    return changes

# Function to write changes to a CSV file
def write_to_csv(changes, output_csv):
    try:
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for change in changes:
                writer.writerow(dict(zip(fieldnames, change)))
    except Exception as e:
        raise IOError(f"Error: IOError: Failed to write to CSV file. {str(e)}")

# Main function to execute the script
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: FileNotFoundError: The root directory does not exist.")

    changes = parse_json_files(root_dir)
    write_to_csv(changes, output_csv)

if __name__ == "__main__":
    main()