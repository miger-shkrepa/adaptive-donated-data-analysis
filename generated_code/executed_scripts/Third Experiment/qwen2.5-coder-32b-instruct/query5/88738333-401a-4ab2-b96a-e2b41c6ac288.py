import os
import csv
import json
from datetime import datetime

root_dir = "root_dir"

def convert_timestamp_to_datetime(timestamp):
    try:
        return datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise ValueError("Error: Invalid timestamp value.")

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    login_activity_path = os.path.join(root_dir, "security_and_login_information", "login_and_profile_creation", "login_activity.json")
    
    if not os.path.exists(login_activity_path):
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
        return
    
    try:
        with open(login_activity_path, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("Error: The login_activity.json file is not properly formatted.")
    
    login_data = data.get("account_history_login_history", [])
    
    if not login_data:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
        return
    
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Device ID', 'Login Time'])
        
        for entry in login_data:
            string_map_data = entry.get("string_map_data", {})
            device_id = string_map_data.get("Device", {}).get("value", "")
            login_time_timestamp = string_map_data.get("Time", {}).get("value", "")
            
            if device_id and login_time_timestamp:
                login_time = convert_timestamp_to_datetime(login_time_timestamp)
                writer.writerow([device_id, login_time])

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)