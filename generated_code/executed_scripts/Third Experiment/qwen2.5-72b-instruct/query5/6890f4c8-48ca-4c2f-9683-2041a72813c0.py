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
                user_agent = string_map_data.get("User Agent", {}).get("value", "")
                timestamp = string_map_data.get("Time", {}).get("timestamp", 0)
                if timestamp:
                    login_time = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    results.append({"Device ID": user_agent, "Login Time": login_time})
            return results
    except FileNotFoundError:
        raise FileNotFoundError("Error: The login_activity.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The login_activity.json file is not a valid JSON.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred: {str(e)}")

def generate_csv(results):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Device ID', 'Login Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            if results:
                writer.writerows(results)
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while writing the CSV: {str(e)}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        login_activity_path = os.path.join(root_dir, "security_and_login_information", "login_and_profile_creation", "login_activity.json")
        if not os.path.exists(login_activity_path):
            generate_csv([])
            return
        
        login_results = process_login_activity(login_activity_path)
        generate_csv(login_results)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()