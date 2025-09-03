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

# Function to parse login activity JSON
def parse_login_activity(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            login_data = data.get('account_history_login_history', [])
            results = []
            for entry in login_data:
                string_map_data = entry.get('string_map_data', {})
                device_id = string_map_data.get('Device', {}).get('value', '')
                login_time = string_map_data.get('Time', {}).get('value', '')
                if device_id and login_time:
                    try:
                        login_time = datetime.strptime(login_time, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')
                        results.append((device_id, login_time))
                    except ValueError:
                        continue
            return results
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The login activity file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The login activity file is not a valid JSON.")

# Main function to process the directory
def main():
    login_activity_path = os.path.join(root_dir, 'security_and_login_information', 'login_and_profile_creation', 'login_activity.json')

    try:
        login_data = parse_login_activity(login_activity_path)

        # Write the results to the CSV file
        with open(output_csv, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Device ID', 'Login Time'])
            csvwriter.writerows(login_data)

    except FileNotFoundError as e:
        with open(output_csv, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Device ID', 'Login Time'])
        raise e
    except ValueError as e:
        with open(output_csv, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Device ID', 'Login Time'])
        raise e

if __name__ == "__main__":
    main()