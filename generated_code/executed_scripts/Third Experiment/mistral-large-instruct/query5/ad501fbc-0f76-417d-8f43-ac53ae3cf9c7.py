import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to parse login activity JSON files
def parse_login_activity(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            login_history = data.get('account_history_login_history', [])
            login_data = []
            for entry in login_history:
                string_map_data = entry.get('string_map_data', {})
                device = string_map_data.get('Device', {}).get('value', 'Unknown')
                time_str = string_map_data.get('Time', {}).get('value', '')
                if time_str:
                    try:
                        login_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                        login_data.append((device, login_time.strftime('%Y-%m-%d %H:%M:%S')))
                    except ValueError:
                        pass  # Skip entries with invalid date format
            return login_data
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The login activity file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The login activity file is not a valid JSON.")

# Function to write data to CSV
def write_to_csv(data, file_path):
    try:
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
            writer.writerows(data)
    except Exception as e:
        raise IOError(f"IOError: Failed to write to CSV file. {str(e)}")

# Main function to process the directory
def main():
    login_activity_file = os.path.join(root_dir, 'login_activity.json')
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    if not os.path.exists(login_activity_file):
        # If the login activity file does not exist, create a CSV with only headers
        write_to_csv([], output_csv)
        return

    login_data = parse_login_activity(login_activity_file)
    write_to_csv(login_data, output_csv)

if __name__ == "__main__":
    main()