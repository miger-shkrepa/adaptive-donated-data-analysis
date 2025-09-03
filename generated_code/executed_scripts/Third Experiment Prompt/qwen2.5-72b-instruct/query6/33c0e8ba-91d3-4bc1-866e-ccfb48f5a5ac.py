import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Function to parse the JSON file and extract the required data
def parse_profile_changes(json_data):
    changes = []
    if "profile_profile_change" in json_data:
        for entry in json_data["profile_profile_change"]:
            string_map_data = entry.get("string_map_data", {})
            changed = string_map_data.get("Changed", {}).get("value", "")
            new_value = string_map_data.get("New Value", {}).get("value", "")
            change_date = string_map_data.get("Change Date", {}).get("value", "")
            if change_date:
                try:
                    change_date = datetime.strptime(change_date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                except ValueError:
                    change_date = ""
            changes.append((changed, new_value, change_date))
    return changes

# Function to write the data to a CSV file
def write_to_csv(changes, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Changed", "New Value", "Change Date"])
        csvwriter.writerows(changes)

# Main function to process the data
def process_data(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        changes = []
        profile_changes_path = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")
        
        if os.path.exists(profile_changes_path):
            with open(profile_changes_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                changes = parse_profile_changes(json_data)
        else:
            print("Warning: profile_changes.json not found. Creating an empty CSV file.")
        
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        write_to_csv(changes, output_path)
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: {e}")

# Execute the main function
if __name__ == "__main__":
    process_data(root_dir)