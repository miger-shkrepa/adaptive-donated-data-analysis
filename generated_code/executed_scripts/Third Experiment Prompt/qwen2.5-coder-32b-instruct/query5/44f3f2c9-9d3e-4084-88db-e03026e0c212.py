import os
import csv
import json
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

# Function to convert timestamp to datetime string
def timestamp_to_datetime(timestamp):
    try:
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except (OSError, OverflowError, ValueError) as e:
        raise ValueError(f"ValueError: Failed to convert timestamp {timestamp} to datetime. {str(e)}")

# Function to process login activity and extract device IDs and login times
def process_login_activity(root_dir):
    login_activity_file_path = os.path.join(root_dir, "security_and_login_information", "login_and_profile_creation", "login_activity.json")
    
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(login_activity_file_path):
        print(f"Warning: The file {login_activity_file_path} does not exist. Returning an empty CSV.")
        return []

    try:
        with open(login_activity_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        raise ValueError(f"ValueError: Failed to read or decode the file {login_activity_file_path}. {str(e)}")

    login_activities = []
    try:
        for entry in data.get("account_history_login_history", []):
            string_map_data = entry.get("string_map_data", {})
            device_id = string_map_data.get("Device ID", {}).get("value")
            timestamp = string_map_data.get("Time", {}).get("timestamp")
            if device_id and timestamp:
                login_time = timestamp_to_datetime(timestamp)
                login_activities.append((device_id, login_time))
    except Exception as e:
        raise ValueError(f"ValueError: Failed to process login activity data. {str(e)}")

    return login_activities

# Main function to execute the query and save the results to a CSV file
def main():
    try:
        login_activities = process_login_activity(root_dir)
        
        # Define the output file path
        output_file_path = "query_responses/results.csv"
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        
        # Write the results to a CSV file
        with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Device ID", "Login Time"])
            csvwriter.writerows(login_activities)
        
        print(f"Results saved to {output_file_path}")
    
    except Exception as e:
        print(f"Error: {str(e)}")

# Execute the main function
if __name__ == "__main__":
    main()