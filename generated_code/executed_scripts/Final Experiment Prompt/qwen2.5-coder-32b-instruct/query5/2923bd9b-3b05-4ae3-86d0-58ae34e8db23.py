import os
import json
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

def extract_device_and_login_time(data):
    results = []
    for device in data.get("devices_devices", []):
        user_agent = device.get("string_map_data", {}).get("User Agent", {}).get("value", "")
        login_timestamp = device.get("string_map_data", {}).get("Last Login", {}).get("timestamp", 0)
        
        if user_agent and login_timestamp:
            login_time = datetime.fromtimestamp(login_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            results.append((user_agent, login_time))
    
    return results

def main():
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Define the path to the JSON file
    json_file_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")
    
    # Check if the JSON file exists
    if not os.path.exists(json_file_path):
        # If the file does not exist, create a CSV with only headers
        with open('query_responses/results.csv', 'w') as f:
            f.write("Device ID,Login Time\n")
        return
    
    # Load the JSON data
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        raise ValueError("ValueError: The JSON file is not properly formatted.")
    
    # Extract device and login time
    results = extract_device_and_login_time(data)
    
    # Write the results to a CSV file
    with open('query_responses/results.csv', 'w') as f:
        f.write("Device ID,Login Time\n")
        for device_id, login_time in results:
            f.write(f"{device_id},{login_time}\n")

if __name__ == "__main__":
    main()