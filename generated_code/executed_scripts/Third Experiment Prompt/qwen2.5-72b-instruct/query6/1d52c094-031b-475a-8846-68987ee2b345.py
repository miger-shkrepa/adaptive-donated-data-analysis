import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def find_account_changes(directory):
    changes = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'changes' in data:  # Assuming 'changes' key contains account changes
                            for change in data['changes']:
                                if all(key in change for key in ['Changed', 'New Value', 'Change Date']):
                                    changes.append({
                                        'Changed': change['Changed'],
                                        'New Value': change['New Value'],
                                        'Change Date': change['Change Date']
                                    })
                except (json.JSONDecodeError, KeyError):
                    continue
    return changes

def save_to_csv(changes, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Changed', 'New Value', 'Change Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for change in changes:
            writer.writerow(change)

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        changes = find_account_changes(root_dir)
        
        if not changes:
            changes = []  # Return only headers if no changes found
        
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        save_to_csv(changes, output_path)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()