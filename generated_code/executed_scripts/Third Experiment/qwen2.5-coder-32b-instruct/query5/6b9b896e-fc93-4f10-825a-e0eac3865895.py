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
    login_activity_path = os.path.join(root_dir, "security_and_login_information", "login_activity.json")
    
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(login_activity_path):
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
        return
    
    try:
        with open(login_activity_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("Error: The login_activity.json file is not a valid JSON file.")
    
    login_history = data.get('account_history_login_history', [])
    
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Device ID', 'Login Time'])
        
        for entry in login_history:
            string_map_data = entry.get('string_map_data', {})
            ip_address = string_map_data.get('IP-Adresse', {}).get('value', '')
            timestamp = string_map_data.get('Zeit', {}).get('timestamp', '')
            
            if ip_address and timestamp:
                login_time = convert_timestamp_to_datetime(timestamp)
                writer.writerow([ip_address, login_time])

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)