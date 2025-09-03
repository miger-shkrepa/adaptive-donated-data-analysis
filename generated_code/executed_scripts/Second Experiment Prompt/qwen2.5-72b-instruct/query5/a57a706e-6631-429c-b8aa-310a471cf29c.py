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

def get_login_activity(root_dir):
    login_activity_path = os.path.join(root_dir, "security_and_login_information", "login_and_profile_creation", "login_activity.json")
    try:
        if not os.path.exists(login_activity_path):
            return []
        
        login_activity_data = load_json_file(login_activity_path)
        login_history = login_activity_data.get("account_history_login_history", [])
        
        login_records = []
        for entry in login_history:
            string_map_data = entry.get("string_map_data", {})
            time_str = string_map_data.get("Time", {}).get("value")
            if time_str:
                try:
                    login_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                    device = string_map_data.get("Device", {}).get("value", "Unknown Device")
                    login_records.append((device, login_time))
                except ValueError:
                    raise ValueError("Error: Invalid date format in login activity data.")
        
        return login_records
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def save_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Device ID", "Login Time"])
            for device, login_time in data:
                writer.writerow([device, login_time.strftime("%Y-%m-%d %H:%M:%S")])
    except Exception as e:
        raise Exception(f"Error: Failed to write to CSV file. {str(e)}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        login_records = get_login_activity(root_dir)
        output_path = "query_responses/results.csv"
        save_to_csv(login_records, output_path)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()