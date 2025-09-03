import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Function to convert timestamp to YYYY-MM-DD format
def timestamp_to_date(timestamp):
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except (ValueError, TypeError):
        return ""

# Function to process the profile_changes.json file and extract the required data
def process_profile_changes(profile_changes_path):
    try:
        with open(profile_changes_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            changes = data.get("profile_profile_change", [])
            result = []
            for change in changes:
                string_map_data = change.get("string_map_data", {})
                changed = string_map_data.get("Changed", {}).get("value", "")
                new_value = string_map_data.get("New Value", {}).get("value", "")
                change_date = timestamp_to_date(string_map_data.get("Change Date", {}).get("timestamp", 0))
                result.append([changed, new_value, change_date])
            return result
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The profile_changes.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON from profile_changes.json.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while processing profile_changes.json: {str(e)}")

# Function to write the result to a CSV file
def write_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Changed", "New Value", "Change Date"])
            writer.writerows(data)
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while writing to CSV: {str(e)}")

# Main function to execute the query
def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        profile_changes_path = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")
        if not os.path.exists(profile_changes_path):
            write_to_csv([], 'query_responses/results.csv')
            return

        changes_data = process_profile_changes(profile_changes_path)
        write_to_csv(changes_data, 'query_responses/results.csv')
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()