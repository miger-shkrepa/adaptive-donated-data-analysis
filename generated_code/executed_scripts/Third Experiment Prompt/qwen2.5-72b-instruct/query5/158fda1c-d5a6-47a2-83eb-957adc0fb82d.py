import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Function to parse timestamp to the required format
def parse_timestamp(timestamp):
    try:
        return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return None

# Function to process the login activity JSON file
def process_login_activity(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            login_data = data.get("account_history_login_history", [])
            results = []
            for entry in login_data:
                string_map_data = entry.get("string_map_data", {})
                device = string_map_data.get("Device", {}).get("value")
                timestamp = string_map_data.get("Time", {}).get("timestamp")
                if device and timestamp:
                    login_time = parse_timestamp(timestamp)
                    if login_time:
                        results.append((device, login_time))
            return results
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified login activity file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON from the login activity file.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while processing the login activity file: {str(e)}")

# Function to generate the CSV file
def generate_csv(results):
    csv_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Device ID', 'Login Time'])
        writer.writerows(results)

# Main function to execute the query
def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        login_activity_path = os.path.join(root_dir, "security_and_login_information", "login_and_profile_creation", "login_activity.json")
        if not os.path.exists(login_activity_path):
            generate_csv([])
            return

        results = process_login_activity(login_activity_path)
        generate_csv(results)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()