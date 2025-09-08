import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def process_login_activity(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            login_data = data.get("account_history_login_history", [])
            results = []
            for entry in login_data:
                string_map_data = entry.get("string_map_data", {})
                device = string_map_data.get("Device", {}).get("value", "")
                timestamp = string_map_data.get("Time", {}).get("timestamp", 0)
                if timestamp:
                    login_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                    results.append((device, login_time))
            return results
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified login activity file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The login activity file is not a valid JSON.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while processing the login activity file: {str(e)}")

def generate_csv(results):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
            if results:
                writer.writerows(results)
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while generating the CSV file: {str(e)}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        login_activity_path = os.path.join(root_dir, "your_instagram_activity", "login_activity.json")
        if not os.path.exists(login_activity_path):
            with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Device ID', 'Login Time'])
            return
        
        login_results = process_login_activity(login_activity_path)
        generate_csv(login_results)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()