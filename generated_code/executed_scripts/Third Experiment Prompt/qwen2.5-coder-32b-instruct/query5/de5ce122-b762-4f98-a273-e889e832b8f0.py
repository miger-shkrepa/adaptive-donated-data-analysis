import os
import csv
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

def get_login_activity_file_path(root_dir):
    login_activity_path = os.path.join(root_dir, "security_and_login_information", "login_and_account_creation", "login_activity.json")
    return login_activity_path

def read_json_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        import json
        data = json.load(file)
    return data

def extract_device_and_login_time(data):
    device_login_times = []
    if "account_history_login_history" in data:
        for entry in data["account_history_login_history"]:
            string_map_data = entry.get("string_map_data", {})
            device_id = string_map_data.get("GerÃ¤te-ID", {}).get("value", "")
            timestamp = string_map_data.get("Zeit", {}).get("timestamp", 0)
            if timestamp:
                login_time = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
                device_login_times.append((device_id, login_time))
    return device_login_times

def write_to_csv(device_login_times, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Device ID", "Login Time"])
        csvwriter.writerows(device_login_times)

def main():
    try:
        login_activity_path = get_login_activity_file_path(root_dir)
        data = read_json_file(login_activity_path)
        device_login_times = extract_device_and_login_time(data)
        write_to_csv(device_login_times, 'query_responses/results.csv')
    except FileNotFoundError as e:
        write_to_csv([], 'query_responses/results.csv')
        print(e)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()