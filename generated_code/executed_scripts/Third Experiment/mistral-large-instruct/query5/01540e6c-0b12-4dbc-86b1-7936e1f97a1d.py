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
            login_data = data.get('account_history_login_history', [])
            results = []
            for entry in login_data:
                string_map_data = entry.get('string_map_data', {})
                device_id = string_map_data.get('User Agent', {}).get('value', 'Unknown')
                timestamp = string_map_data.get('Time', {}).get('timestamp', 0)
                login_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                results.append((device_id, login_time))
            return results
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The login activity file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The login activity file is not a valid JSON.")

# Function to write the results to a CSV file
def write_to_csv(results, file_path):
    try:
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
            writer.writerows(results)
    except Exception as e:
        raise IOError(f"IOError: Failed to write to CSV file. {str(e)}")

# Main function to process the directory and generate the CSV
def main():
    login_activity_path = os.path.join(root_dir, 'security_and_login_information', 'login_and_profile_creation', 'login_activity.json')

    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    if not os.path.exists(login_activity_path):
        # If the login activity file does not exist, create a CSV with only the column headers
        write_to_csv([], output_csv)
        return

    login_data = parse_login_activity(login_activity_path)
    write_to_csv(login_data, output_csv)

if __name__ == "__main__":
    main()