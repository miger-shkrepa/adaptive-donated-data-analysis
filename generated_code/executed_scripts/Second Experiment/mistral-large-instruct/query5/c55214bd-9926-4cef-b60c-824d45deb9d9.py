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
            login_data = []
            for entry in data.get('account_history_login_history', []):
                string_map_data = entry.get('string_map_data', {})
                user_agent = string_map_data.get('User Agent', {}).get('value', 'Unknown')
                timestamp = string_map_data.get('Time', {}).get('timestamp', 0)
                login_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                login_data.append((user_agent, login_time))
            return login_data
    except FileNotFoundError:
        raise FileNotFoundError("Error: The login activity file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The login activity file is not a valid JSON.")

# Function to write the results to a CSV file
def write_to_csv(data, file_path):
    try:
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Device ID', 'Login Time'])
            writer.writerows(data)
    except Exception as e:
        raise IOError(f"Error: Failed to write to CSV file. {str(e)}")

# Main function to process the directory and generate the CSV
def main():
    login_activity_path = os.path.join(root_dir, 'security_and_login_information', 'login_and_profile_creation', 'login_activity.json')

    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    try:
        login_data = parse_login_activity(login_activity_path)
    except FileNotFoundError:
        login_data = []

    if not os.path.exists('query_responses'):
        os.makedirs('query_responses')

    write_to_csv(login_data, output_csv)

if __name__ == "__main__":
    main()