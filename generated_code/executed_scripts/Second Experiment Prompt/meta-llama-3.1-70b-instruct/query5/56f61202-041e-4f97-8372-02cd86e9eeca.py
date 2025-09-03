import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_login_devices(root_dir):
    try:
        devices_file_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        if not os.path.exists(devices_file_path):
            return []
        
        with open(devices_file_path, 'r') as file:
            import json
            data = json.load(file)
            devices = []
            for device in data['devices_devices']:
                device_id = device['string_map_data'].get('User Agent', {}).get('value', '')
                login_time = device['string_map_data'].get('Last Login', {}).get('value', '')
                if login_time:
                    try:
                        login_time = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        login_time = ''
                devices.append((device_id, login_time))
            return devices
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_to_csv(devices):
    with open('query_responses/results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Device ID", "Login Time"])
        for device in devices:
            writer.writerow(device)

def main():
    try:
        devices = get_login_devices(root_dir)
        write_to_csv(devices)
    except Exception as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Device ID", "Login Time"])
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()