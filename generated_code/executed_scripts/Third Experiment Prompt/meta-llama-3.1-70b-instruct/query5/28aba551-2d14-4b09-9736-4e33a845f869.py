import os
import csv
import json

root_dir = "root_dir"

def get_devices_login_time(root_dir):
    devices_login_time = []
    devices_file_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")
    
    try:
        with open(devices_file_path, 'r') as devices_file:
            devices_data = json.load(devices_file)
            for device in devices_data.get("devices_devices", []):
                device_id = device.get("string_map_data", {}).get("Device ID", {}).get("value")
                login_time = device.get("string_map_data", {}).get("Last Login", {}).get("value")
                if device_id and login_time:
                    devices_login_time.append((device_id, login_time))
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The devices.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The devices.json file is not a valid JSON.")
    
    return devices_login_time

def save_to_csv(devices_login_time):
    csv_file_path = "query_responses/results.csv"
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Device ID", "Login Time"])
        for device_id, login_time in devices_login_time:
            csv_writer.writerow([device_id, login_time])

def main():
    try:
        devices_login_time = get_devices_login_time(root_dir)
        if not devices_login_time:
            save_to_csv([["Device ID", "Login Time"]])
        else:
            save_to_csv(devices_login_time)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except ValueError as e:
        raise ValueError(f"ValueError: {e}")

if __name__ == "__main__":
    main()