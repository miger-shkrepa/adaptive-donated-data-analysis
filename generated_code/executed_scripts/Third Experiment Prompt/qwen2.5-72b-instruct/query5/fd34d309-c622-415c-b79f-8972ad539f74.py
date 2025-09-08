import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Function to parse the login time from timestamp
def parse_login_time(timestamp):
    try:
        return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        raise ValueError(f"Error: Failed to parse timestamp {timestamp}. Reason: {str(e)}")

# Function to process the login activity JSON file
def process_login_activity(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            login_history = data.get("account_history_login_history", [])
            results = []
            for entry in login_history:
                string_map_data = entry.get("string_map_data", {})
                device_id = string_map_data.get("User Agent", {}).get("value")
                timestamp = string_map_data.get("Zeit", {}).get("timestamp")
                if device_id and timestamp:
                    login_time = parse_login_time(timestamp)
                    results.append((device_id, login_time))
            return results
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The login_activity.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON from login_activity.json.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while processing {file_path}. Reason: {str(e)}")

# Function to generate the CSV file
def generate_csv(results):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
            writer.writerows(results)
    except Exception as e:
        raise Exception(f"Error: Failed to write to CSV file. Reason: {str(e)}")

# Main function to execute the query
def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        login_activity_path = os.path.join(root_dir, "security_and_login_information", "login_and_account_creation", "login_activity.json")
        
        if not os.path.exists(login_activity_path):
            generate_csv([])  # Generate CSV with headers only if the file is missing
            return
        
        results = process_login_activity(login_activity_path)
        generate_csv(results)
        
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()