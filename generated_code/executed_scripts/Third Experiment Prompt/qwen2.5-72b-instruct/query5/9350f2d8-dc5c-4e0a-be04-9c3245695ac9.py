import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def get_device_login_times(root_dir):
    devices_login_times = []

    try:
        devices_file_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")
        if not os.path.exists(devices_file_path):
            return devices_login_times

        devices_data = load_json_file(devices_file_path)

        for device in devices_data.get("devices_devices", []):
            string_map_data = device.get("string_map_data", {})
            device_id = string_map_data.get("Device ID", {}).get("value")
            last_login_timestamp = string_map_data.get("Last Login", {}).get("timestamp")

            if device_id and last_login_timestamp:
                try:
                    last_login_time = datetime.fromtimestamp(last_login_timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    devices_login_times.append((device_id, last_login_time))
                except ValueError:
                    raise ValueError(f"Error: Invalid timestamp value {last_login_timestamp} for device {device_id}.")

    except Exception as e:
        print(f"Error processing devices data: {e}")

    return devices_login_times

def write_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
            writer.writerows(data)
    except Exception as e:
        raise ValueError(f"Error: Failed to write to CSV file {output_path}. Reason: {e}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        devices_login_times = get_device_login_times(root_dir)
        output_path = 'query_responses/results.csv'
        write_to_csv(devices_login_times, output_path)
        print(f"CSV file has been saved to {output_path}")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()