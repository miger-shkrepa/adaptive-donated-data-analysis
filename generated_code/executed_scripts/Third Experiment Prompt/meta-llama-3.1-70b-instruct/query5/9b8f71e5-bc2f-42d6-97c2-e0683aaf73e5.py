import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_login_devices(root_dir):
    try:
        devices_file = os.path.join(root_dir, "personal_information", "device_information", "devices.json")
        if not os.path.exists(devices_file):
            raise FileNotFoundError("FileNotFoundError: The devices.json file does not exist.")

        with open(devices_file, "r") as f:
            devices_data = json.load(f)

        devices = []
        for device in devices_data.get("devices_devices", []):
            string_map_data = device.get("string_map_data", {})
            device_id = string_map_data.get("Geräte-ID", {}).get("value")
            login_time = string_map_data.get("Last Login", {}).get("value")
            if device_id and login_time:
                login_time = datetime.strptime(login_time, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                devices.append((device_id, login_time))

        return devices

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")

    except Exception as e:
        raise ValueError(f"Error: {e}")

def write_to_csv(devices):
    try:
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Device ID", "Login Time"])
            for device in devices:
                writer.writerow(device)

    except Exception as e:
        raise ValueError(f"Error: {e}")

def main():
    try:
        devices = get_login_devices(root_dir)
        if not devices:
            with open("query_responses/results.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Device ID", "Login Time"])
        else:
            write_to_csv(devices)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()