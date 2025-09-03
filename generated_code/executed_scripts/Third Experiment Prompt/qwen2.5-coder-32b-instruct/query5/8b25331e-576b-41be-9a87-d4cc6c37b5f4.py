import os
import csv
import json
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

# Function to convert timestamp to datetime string
def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a list to store the results
results = []

# Define the path to the login activity file
login_activity_path = os.path.join(root_dir, "security_and_login_information", "login_and_account_creation", "login_activity.json")

# Check if the login activity file exists
if os.path.exists(login_activity_path):
    try:
        with open(login_activity_path, 'r', encoding='utf-8') as file:
            login_data = json.load(file)
            
            # Check if the expected structure is present
            if 'account_history_login_history' in login_data:
                for entry in login_data['account_history_login_history']:
                    if 'string_map_data' in entry:
                        string_map_data = entry['string_map_data']
                        device_id = string_map_data.get('User Agent', {}).get('value', '')
                        login_time = string_map_data.get('Zeit', {}).get('timestamp', 0)
                        if login_time:
                            login_time_str = timestamp_to_datetime(login_time)
                            results.append((device_id, login_time_str))
    except (json.JSONDecodeError, KeyError) as e:
        raise ValueError(f"ValueError: Error parsing login activity file - {str(e)}")

# Define the path to the output CSV file
output_csv_path = 'query_responses/results.csv'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

# Write the results to the CSV file
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Device ID', 'Login Time'])
    csvwriter.writerows(results)