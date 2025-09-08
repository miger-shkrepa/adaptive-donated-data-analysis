import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def get_login_data(root_dir):
    login_data = []
    devices_file_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")
    
    if not os.path.exists(devices_file_path):
        return login_data

    try:
        devices_data = load_json_file(devices_file_path)
        devices = devices_data.get("devices_devices", [])
        
        for device in devices:
            string_map_data = device.get("string_map_data", {})
            last_login = string_map_data.get("Last Login", {}).get("value")
            device_id = string_map_data.get("Device ID", {}).get("value")
            
            if last_login and device_id:
                try:
                    login_time = datetime.fromtimestamp(int(last_login)).strftime('%Y-%m-%d %H:%M:%S')
                    login_data.append((device_id, login_time))
                except ValueError:
                    raise ValueError(f"Error: Invalid timestamp value {last_login} for device {device_id}.")
    except Exception as e:
        raise e

    return login_data

def write_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
            writer.writerows(data)
    except Exception as e:
        raise e

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        login_data = get_login_data(root_dir)
        output_path = 'query_responses/results.csv'
        write_to_csv(login_data, output_path)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()