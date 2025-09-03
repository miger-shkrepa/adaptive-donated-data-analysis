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

def process_login_activity(data):
    result = []
    if "account_history_login_history" in data:
        for entry in data["account_history_login_history"]:
            string_map_data = entry.get("string_map_data", {})
            device = string_map_data.get("Device", {}).get("value")
            time_str = string_map_data.get("Time", {}).get("value")
            if device and time_str:
                try:
                    login_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                    result.append((device, login_time.strftime("%Y-%m-%d %H:%M:%S")))
                except ValueError:
                    raise ValueError(f"Error: Invalid time format in {time_str}.")
    return result

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        login_activity_path = os.path.join(root_dir, "security_and_login_information", "login_and_profile_creation", "login_activity.json")
        if not os.path.exists(login_activity_path):
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Device ID', 'Login Time'])
            return

        login_activity_data = load_json_file(login_activity_path)
        login_data = process_login_activity(login_activity_data)

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
            writer.writerows(login_data)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()