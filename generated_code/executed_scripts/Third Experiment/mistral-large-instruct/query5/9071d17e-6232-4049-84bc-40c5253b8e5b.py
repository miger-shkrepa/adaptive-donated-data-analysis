import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to parse the login activity JSON file
def parse_login_activity(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            login_activity = data.get("account_history_login_history", [])
            return login_activity
    except FileNotFoundError:
        raise FileNotFoundError("Error: The login activity file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The login activity file is not a valid JSON.")

# Function to extract device ID and login time
def extract_device_info(login_activity):
    device_info = []
    for entry in login_activity:
        string_map_data = entry.get("string_map_data", {})
        device_id = string_map_data.get("Device ID", {}).get("value", "")
        login_time = string_map_data.get("Time", {}).get("value", "")
        if device_id and login_time:
            try:
                login_time = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')
                device_info.append((device_id, login_time))
            except ValueError:
                continue
    return device_info

# Function to write the results to a CSV file
def write_to_csv(device_info, output_csv):
    try:
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Device ID", "Login Time"])
            writer.writerows(device_info)
    except Exception as e:
        raise IOError(f"Error: Failed to write to CSV file. {str(e)}")

# Main function to process the query
def main():
    login_activity_file = os.path.join(root_dir, "security_and_login_information", "login_and_account_creation", "login_activity.json")

    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    login_activity = parse_login_activity(login_activity_file)
    device_info = extract_device_info(login_activity)

    if not os.path.exists(os.path.dirname(output_csv)):
        os.makedirs(os.path.dirname(output_csv))

    write_to_csv(device_info, output_csv)

if __name__ == "__main__":
    main()