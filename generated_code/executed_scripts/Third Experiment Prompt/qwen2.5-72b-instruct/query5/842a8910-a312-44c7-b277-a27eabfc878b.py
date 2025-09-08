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

def get_device_login_times(root_dir):
    device_login_times = []

    try:
        login_activity_path = os.path.join(root_dir, "security_and_login_information", "login_and_account_creation", "login_activity.json")
        if os.path.exists(login_activity_path):
            login_activity_data = load_json_file(login_activity_path)
            for entry in login_activity_data.get("account_history_login_history", []):
                string_map_data = entry.get("string_map_data", {})
                ip_address = string_map_data.get("IP-Adresse", {}).get("value")
                user_agent = string_map_data.get("User Agent", {}).get("value")
                timestamp = string_map_data.get("Zeit", {}).get("timestamp")
                if ip_address and user_agent and timestamp:
                    login_time = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    device_login_times.append((f"{ip_address} - {user_agent}", login_time))
    except Exception as e:
        print(f"Error processing login_activity.json: {e}")

    return device_login_times

def write_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Device ID", "Login Time"])
            writer.writerows(data)
    except Exception as e:
        raise ValueError(f"Error: Failed to write to CSV file {output_path}. Reason: {e}")

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    device_login_times = get_device_login_times(root_dir)
    output_path = 'query_responses/results.csv'
    write_to_csv(device_login_times, output_path)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)