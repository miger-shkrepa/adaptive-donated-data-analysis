import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def parse_timestamp(timestamp):
    try:
        return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return None

def process_devices_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            devices = data.get("devices_devices", [])
            results = []
            for device in devices:
                string_map_data = device.get("string_map_data", {})
                last_login = string_map_data.get("Last Login", {}).get("timestamp")
                if last_login is not None:
                    device_id = string_map_data.get("User Agent", {}).get("value")
                    login_time = parse_timestamp(last_login)
                    if device_id and login_time:
                        results.append((device_id, login_time))
            return results
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON file.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        devices_file_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")
        if not os.path.exists(devices_file_path):
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Device ID', 'Login Time'])
            return

        results = process_devices_json(devices_file_path)

        os.makedirs('query_responses', exist_ok=True)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
            writer.writerows(results)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()