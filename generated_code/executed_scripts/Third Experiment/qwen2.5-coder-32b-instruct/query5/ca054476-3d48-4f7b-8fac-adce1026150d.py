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
    devices_file_path = os.path.join(root_dir, "devices.json")
    
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(devices_file_path):
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
        return
    
    try:
        with open(devices_file_path, 'r') as file:
            devices_data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("Error: The devices.json file is not a valid JSON file.")
    
    devices = devices_data.get('devices_devices', [])
    
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Device ID', 'Login Time'])
        
        for device in devices:
            title = device.get('title', 'Unknown Device')
            last_login = device.get('string_map_data', {}).get('Last Login', {}).get('value', None)
            
            if last_login:
                try:
                    login_time = convert_timestamp_to_datetime(last_login)
                except ValueError as e:
                    print(e)
                    login_time = 'Unknown Time'
            else:
                login_time = 'Unknown Time'
            
            writer.writerow([title, login_time])

if __name__ == "__main__":
    main()