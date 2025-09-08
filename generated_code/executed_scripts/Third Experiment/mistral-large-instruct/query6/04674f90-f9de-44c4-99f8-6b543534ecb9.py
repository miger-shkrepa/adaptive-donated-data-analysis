import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Function to parse JSON files and extract relevant information
def parse_json_files(directory):
    changes = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if "relationships_follow_requests_received" in data:
                            for item in data["relationships_follow_requests_received"]:
                                for string_data in item["string_list_data"]:
                                    changes.append((string_data["value"], string_data["timestamp"], string_data["timestamp"]))
                        elif "relationships_hide_stories_from" in data:
                            for item in data["relationships_hide_stories_from"]:
                                for string_data in item["string_list_data"]:
                                    changes.append((string_data["value"], string_data["timestamp"], string_data["timestamp"]))
                        elif "relationships_dismissed_suggested_users" in data:
                            for item in data["relationships_dismissed_suggested_users"]:
                                for string_data in item["string_list_data"]:
                                    changes.append((string_data["value"], string_data["timestamp"], string_data["timestamp"]))
                        elif "relationships_restricted_users" in data:
                            for item in data["relationships_restricted_users"]:
                                for string_data in item["string_list_data"]:
                                    changes.append((string_data["value"], string_data["timestamp"], string_data["timestamp"]))
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    raise FileNotFoundError(f"Error: {e}")
    return changes

# Function to write changes to a CSV file
def write_to_csv(changes):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Changed', 'New Value', 'Change Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for change in changes:
            change_date = datetime.fromtimestamp(change[1]).strftime('%Y-%m-%d')
            writer.writerow({'Changed': change[0], 'New Value': change[0], 'Change Date': change_date})

# Main function to execute the script
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    changes = parse_json_files(root_dir)
    if not changes:
        # If no changes are found, create a CSV with only the column headers
        write_to_csv([])
    else:
        write_to_csv(changes)

if __name__ == "__main__":
    main()