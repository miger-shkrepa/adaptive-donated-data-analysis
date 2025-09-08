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
        raise FileNotFoundError("FileNotFoundError: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON file.")

def get_device_login_times(root_dir):
    device_login_times = []

    try:
        login_activity_path = os.path.join(root_dir, "security_and_login_information", "login_and_account_creation", "login_activity.json")
        if os.path.exists(login_activity_path):
            login_activity_data = load_json_file(login_activity_path)
            for entry in login_activity_data.get("account_history_login_history", []):
                string_map_data = entry.get("string_map_data", {})
                device_id = string_map_data.get("Device", {}).get("value")
                login_time = string_map_data.get("Time", {}).get("value")
                if device_id and login_time:
                    try:
                        login_time_formatted = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')
                        device_login_times.append((device_id, login_time_formatted))
                    except (ValueError, TypeError):
                        raise ValueError("Error: Invalid timestamp value in login activity data.")
        else:
            print("Warning: login_activity.json not found. Returning empty data.")
    except Exception as e:
        print(f"Error: {e}")

    return device_login_times

def save_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Device ID", "Login Time"])
            csvwriter.writerows(data)
    except Exception as e:
        raise IOError(f"Error: Failed to write to CSV file. {e}")

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    device_login_times = get_device_login_times(root_dir)
    save_to_csv(device_login_times, 'query_responses/results.csv')

if __name__ == "__main__":
    main()