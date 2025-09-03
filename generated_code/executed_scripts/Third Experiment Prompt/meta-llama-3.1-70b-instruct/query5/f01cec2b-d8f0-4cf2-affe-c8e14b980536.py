import os
import csv
import json

root_dir = "root_dir"

def get_devices_and_login_times(root_dir):
    devices = []
    login_times = []

    devices_file_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")
    if not os.path.exists(devices_file_path):
        raise FileNotFoundError("Error: The devices.json file does not exist.")

    with open(devices_file_path, "r") as devices_file:
        devices_data = json.load(devices_file)
        for device in devices_data.get("devices_devices", []):
            string_map_data = device.get("string_map_data", {})
            device_id = string_map_data.get("Device ID", {}).get("value")
            login_time = string_map_data.get("Last Login", {}).get("value")
            if device_id and login_time:
                devices.append(device_id)
                login_times.append(login_time)

    return devices, login_times

def format_login_time(login_time):
    # Assuming login_time is a Unix timestamp
    from datetime import datetime
    return datetime.fromtimestamp(int(login_time)).strftime("%Y-%m-%d %H:%M:%S")

def write_to_csv(devices, login_times):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Device ID", "Login Time"])  # header
        for device, login_time in zip(devices, login_times):
            writer.writerow([device, format_login_time(login_time)])

def main():
    try:
        devices, login_times = get_devices_and_login_times(root_dir)
        write_to_csv(devices, login_times)
    except FileNotFoundError as e:
        print(e)
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Device ID", "Login Time"])  # header

if __name__ == "__main__":
    main()