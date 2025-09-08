import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def parse_login_time(timestamp):
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        raise ValueError(f"Error: Failed to parse timestamp {timestamp}. Reason: {str(e)}")

def process_devices_data(devices_data):
    devices_info = []
    for device in devices_data:
        string_map_data = device.get("string_map_data", {})
        device_id = string_map_data.get("Device ID", {}).get("value")
        last_login = string_map_data.get("Last Login", {}).get("timestamp")
        if device_id and last_login:
            login_time = parse_login_time(last_login)
            devices_info.append((device_id, login_time))
    return devices_info

def generate_csv(devices_info):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Device ID', 'Login Time'])
        if devices_info:
            writer.writerows(devices_info)

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        devices_json_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")
        if not os.path.exists(devices_json_path):
            generate_csv([])
            return
        
        with open(devices_json_path, 'r') as file:
            devices_data = json.load(file).get("devices_devices", [])
        
        devices_info = process_devices_data(devices_data)
        generate_csv(devices_info)
    
    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON. Reason: {str(e)}")
    except Exception as e:
        print(f"Error: An unexpected error occurred. Reason: {str(e)}")

if __name__ == "__main__":
    main()