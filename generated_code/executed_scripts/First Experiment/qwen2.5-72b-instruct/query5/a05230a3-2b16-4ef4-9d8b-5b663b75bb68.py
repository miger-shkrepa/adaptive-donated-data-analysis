import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def parse_timestamp(timestamp):
    try:
        return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        raise ValueError(f"Error: Failed to parse timestamp - {str(e)}")

def get_login_data(root_directory):
    try:
        devices_file_path = os.path.join(root_directory, "security_and_login_information", "login_and_profile_creation", "login_activity.json")
        if not os.path.exists(devices_file_path):
            raise FileNotFoundError("FileNotFoundError: The login_activity.json file does not exist.")
        
        with open(devices_file_path, 'r') as file:
            data = json.load(file)
        
        login_data = []
        for entry in data["account_history_login_history"]:
            string_map_data = entry["string_map_data"]
            device_id = string_map_data["User Agent"]["value"]
            login_time = parse_timestamp(string_map_data["Time"]["timestamp"])
            login_data.append((device_id, login_time))
        
        return login_data
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON.")
    except KeyError as e:
        raise KeyError(f"Error: Missing key in JSON data - {str(e)}")

def write_to_csv(data):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
            writer.writerows(data)
    except Exception as e:
        raise IOError(f"Error: Failed to write to CSV - {str(e)}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        login_data = get_login_data(root_dir)
        write_to_csv(login_data)
        print("CSV file has been successfully created.")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()