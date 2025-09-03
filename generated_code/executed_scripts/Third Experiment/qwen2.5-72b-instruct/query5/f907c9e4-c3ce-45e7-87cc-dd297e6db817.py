import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def process_login_data(root_directory):
    try:
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        login_data_path = os.path.join(root_directory, "security_and_login_information", "login_and_account_creation", "login_activity.json")
        
        if not os.path.exists(login_data_path):
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Device ID', 'Login Time'])
            return
        
        with open(login_data_path, 'r') as file:
            login_data = json.load(file)
        
        login_history = login_data.get("account_history_login_history", [])
        
        results = []
        for entry in login_history:
            string_map_data = entry.get("string_map_data", {})
            user_agent = string_map_data.get("User Agent", {}).get("value", "")
            timestamp = string_map_data.get("Zeit", {}).get("timestamp", 0)
            
            if timestamp:
                login_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                results.append([user_agent, login_time])
        
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
            writer.writerows(results)
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

# Call the function with the root directory
process_login_data(root_dir)