import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_devices_login_time(root_dir):
    devices = []
    try:
        personal_info_dir = os.path.join(root_dir, "personal_information")
        if not os.path.exists(personal_info_dir):
            raise FileNotFoundError("Error: The personal information directory does not exist.")
        
        device_info_dir = os.path.join(personal_info_dir, "device_information")
        if not os.path.exists(device_info_dir):
            raise FileNotFoundError("Error: The device information directory does not exist.")
        
        devices_json_path = os.path.join(device_info_dir, "devices.json")
        if not os.path.exists(devices_json_path):
            raise FileNotFoundError("Error: The devices.json file does not exist.")
        
        with open(devices_json_path, 'r') as file:
            # Since we don't have the exact JSON structure, we'll assume it's a list of devices
            # and each device has a 'string_map_data' key with 'Last Login' and 'User Agent' keys
            import json
            data = json.load(file)
            for device in data.get("devices_devices", []):
                string_map_data = device.get("string_map_data", {})
                last_login = string_map_data.get("Last Login", {}).get("value")
                user_agent = string_map_data.get("User Agent", {}).get("value")
                if last_login:
                    try:
                        login_time = datetime.fromtimestamp(int(last_login)).strftime('%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        login_time = last_login
                    devices.append((user_agent, login_time))
        
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")
    
    return devices

def save_to_csv(devices):
    with open('query_responses/results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Device ID", "Login Time"])
        for device in devices:
            writer.writerow(device)

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")
        
        devices = get_devices_login_time(root_dir)
        save_to_csv(devices)
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Device ID", "Login Time"])
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

if __name__ == "__main__":
    main()