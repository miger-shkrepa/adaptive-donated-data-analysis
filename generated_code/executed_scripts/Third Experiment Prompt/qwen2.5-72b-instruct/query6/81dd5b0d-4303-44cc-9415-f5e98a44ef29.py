import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv_path = 'query_responses/results.csv'

# Create the output directory if it doesn't exist
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

def get_account_changes(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        personal_info_path = os.path.join(root_dir, "personal_information", "information_about_you", "personal_information.json")
        profile_info_path = os.path.join(root_dir, "personal_information", "personal_information", "instagram_profile_information.json")

        changes = []

        if os.path.exists(personal_info_path):
            with open(personal_info_path, 'r') as file:
                data = json.load(file)
                for entry in data.get("profile_user", []):
                    for key, value in entry.get("string_map_data", {}).items():
                        if "timestamp" in value:
                            timestamp = value["timestamp"]
                            change_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                            changes.append([key, value["value"], change_date])

        if os.path.exists(profile_info_path):
            with open(profile_info_path, 'r') as file:
                data = json.load(file)
                for entry in data.get("profile_account_insights", []):
                    for key, value in entry.get("string_map_data", {}).items():
                        if "timestamp" in value:
                            timestamp = value["timestamp"]
                            change_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                            changes.append([key, value["value"], change_date])

        return changes

    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

def write_to_csv(changes):
    with open(output_csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Changed", "New Value", "Change Date"])
        if changes:
            csvwriter.writerows(changes)

try:
    changes = get_account_changes(root_dir)
    write_to_csv(changes)
except Exception as e:
    print(e)
    with open(output_csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Changed", "New Value", "Change Date"])