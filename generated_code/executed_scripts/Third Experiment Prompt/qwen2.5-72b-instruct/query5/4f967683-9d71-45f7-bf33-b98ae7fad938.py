import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def parse_login_time(timestamp):
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
                if last_login:
                    login_time = parse_login_time(last_login)
                    if login_time:
                        results.append((device.get("title"), login_time))
            return results
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON file.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred: {str(e)}")

def generate_csv(results):
    csv_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Device ID', 'Login Time'])
        if results:
            writer.writerows(results)

def main():
    try:
        devices_json_path = os.path.join(root_dir, 'personal_information', 'device_information', 'devices.json')
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        if not os.path.exists(devices_json_path):
            generate_csv([])
            return

        results = process_devices_json(devices_json_path)
        generate_csv(results)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()