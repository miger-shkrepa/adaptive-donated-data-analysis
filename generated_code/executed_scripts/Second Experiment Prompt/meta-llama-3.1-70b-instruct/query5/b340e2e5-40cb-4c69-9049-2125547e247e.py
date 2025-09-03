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
                device_id = device['string_map_data'].get('User Agent', {}).get('value')
                login_time = device['string_map_data'].get('Last Login', {}).get('value')
                if login_time:
                    try:
                        login_time = datetime.strptime(login_time, '%Y-%m-%dT%H:%M:%S.%fZ')
                        login_time = login_time.strftime('%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        login_time = None
                devices.append((device_id, login_time))
            return devices
    
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def save_to_csv(devices, csv_file_path):
    try:
        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Device ID", "Login Time"])
            for device in devices:
                writer.writerow(device)
    
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def main():
    try:
        devices = get_login_devices(root_dir)
        csv_file_path = 'query_responses/results.csv'
        if not devices:
            with open(csv_file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Device ID", "Login Time"])
        else:
            save_to_csv(devices, csv_file_path)
    
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

if __name__ == "__main__":
    main()