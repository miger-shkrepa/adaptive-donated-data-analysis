import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def parse_timestamp(timestamp):
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return None

def process_devices_data(devices_data):
    devices_info = []
    for device in devices_data:
        device_id = device.get("string_map_data", {}).get("User Agent", {}).get("value")
        login_time = parse_timestamp(device.get("string_map_data", {}).get("Last Login", {}).get("timestamp"))
        if device_id and login_time:
            devices_info.append((device_id, login_time))
    return devices_info

def generate_csv(devices_info):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Device ID', 'Login Time'])
        for device_id, login_time in devices_info:
            csvwriter.writerow([device_id, login_time])

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        devices_json_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")
        if not os.path.exists(devices_json_path):
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['Device ID', 'Login Time'])
            return

        with open(devices_json_path, 'r') as file:
            devices_data = json.load(file)
        
        devices_info = process_devices_data(devices_data.get("devices_devices", []))
        generate_csv(devices_info)
    
    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON data.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()