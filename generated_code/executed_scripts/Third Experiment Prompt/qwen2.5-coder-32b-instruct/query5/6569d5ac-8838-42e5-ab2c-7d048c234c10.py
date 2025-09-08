import os
import csv
import json
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

# Function to convert timestamp to datetime string
def timestamp_to_datetime(timestamp):
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except (OSError, OverflowError, ValueError) as e:
        raise ValueError(f"ValueError: Invalid timestamp {timestamp} - {str(e)}")

# Function to process login activity and extract device information
def process_login_activity(root_dir):
    login_activity_file_path = os.path.join(root_dir, "security_and_login_information", "login_and_account_creation", "login_activity.json")
    
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(login_activity_file_path):
        return []  # Return empty list if the file does not exist
    
    try:
        with open(login_activity_file_path, 'r', encoding='utf-8') as file:
            login_data = json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        raise ValueError(f"ValueError: Error reading or decoding login_activity.json - {str(e)}")
    
    device_logins = []
    
    try:
        for entry in login_data.get("account_history_login_history", []):
            device_id = entry.get("string_map_data", {}).get("GerÃ¤te-ID", {}).get("value", "")
            login_time_timestamp = entry.get("string_map_data", {}).get("Zeit", {}).get("timestamp", 0)
            login_time = timestamp_to_datetime(login_time_timestamp)
            device_logins.append((device_id, login_time))
    except Exception as e:
        raise ValueError(f"ValueError: Error processing login_activity.json - {str(e)}")
    
    return device_logins

# Main function to execute the query and save the results to a CSV file
def main():
    try:
        device_logins = process_login_activity(root_dir)
        
        # Define the output file path
        output_file_path = 'query_responses/results.csv'
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        
        # Write the results to a CSV file
        with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Device ID", "Login Time"])
            csvwriter.writerows(device_logins)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        # If there's an error, create an empty CSV with only the headers
        with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Device ID", "Login Time"])

if __name__ == "__main__":
    main()