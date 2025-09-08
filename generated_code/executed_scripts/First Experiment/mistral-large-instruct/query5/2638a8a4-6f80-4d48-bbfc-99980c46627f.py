import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to extract login information from the JSON files
def extract_login_info(root_dir):
    login_info = []

    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Walk through the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "devices.json":
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for device in data.get("devices_devices", []):
                            login_data = device.get("string_map_data", {}).get("Last Login", {})
                            if login_data:
                                device_id = login_data.get("value")
                                timestamp = login_data.get("timestamp")
                                if device_id and timestamp:
                                    login_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                                    login_info.append((device_id, login_time))
                except json.JSONDecodeError:
                    raise ValueError("ValueError: Failed to decode JSON from file: {}".format(file_path))
                except Exception as e:
                    raise Exception("Error: An unexpected error occurred while processing the file: {}".format(file_path))

    return login_info

# Function to write the login information to a CSV file
def write_to_csv(login_info, output_csv):
    try:
        with open(output_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Device ID", "Login Time"])
            writer.writerows(login_info)
    except Exception as e:
        raise Exception("Error: Failed to write to CSV file: {}".format(output_csv))

# Main function to execute the script
def main():
    login_info = extract_login_info(root_dir)
    write_to_csv(login_info, output_csv)

if __name__ == "__main__":
    main()