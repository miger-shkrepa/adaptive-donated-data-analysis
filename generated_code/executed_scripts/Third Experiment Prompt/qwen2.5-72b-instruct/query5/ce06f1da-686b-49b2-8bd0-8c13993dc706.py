import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

def parse_timestamp(timestamp):
    try:
        return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        raise ValueError(f"Error: Failed to parse timestamp {timestamp}. {str(e)}")

def process_login_activity(root_dir):
    try:
        login_activity_path = os.path.join(root_dir, "security_and_login_information", "login_and_account_creation", "login_activity.json")
        if not os.path.exists(login_activity_path):
            return []

        with open(login_activity_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        login_data = data.get("account_history_login_history", [])
        result = []

        for entry in login_data:
            string_map_data = entry.get("string_map_data", {})
            device_id = string_map_data.get("Device ID", {}).get("value")
            login_time = string_map_data.get("Zeit", {}).get("value")
            if device_id and login_time:
                try:
                    login_time_parsed = parse_timestamp(int(login_time))
                    result.append((device_id, login_time_parsed))
                except ValueError as e:
                    print(f"Warning: {str(e)}")
                    continue

        return result

    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON data.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred. {str(e)}")

def write_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Device ID", "Login Time"])
            writer.writerows(data)
    except Exception as e:
        raise Exception(f"Error: Failed to write to CSV file. {str(e)}")

def main():
    try:
        login_data = process_login_activity(root_dir)
        output_path = 'query_responses/results.csv'
        write_to_csv(login_data, output_path)
        print(f"CSV file has been saved to {output_path}")
    except Exception as e:
        print(str(e))
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Device ID", "Login Time"])

if __name__ == "__main__":
    main()