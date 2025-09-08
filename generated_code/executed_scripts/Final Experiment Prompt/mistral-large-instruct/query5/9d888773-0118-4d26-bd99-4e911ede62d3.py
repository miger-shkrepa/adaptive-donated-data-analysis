import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the path to the devices.json file
devices_file_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")

# Define the path to the output CSV file
output_csv_path = "query_responses/results.csv"

# Function to convert timestamp to datetime string
def convert_timestamp(timestamp):
    try:
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError) as e:
        raise ValueError(f"Error: Invalid timestamp value - {e}")

# Function to process the devices.json file
def process_devices_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError("Error: FileNotFoundError: The devices.json file does not exist.")

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSONDecodeError: Failed to decode JSON - {e}")
    except Exception as e:
        raise ValueError(f"Error: Failed to read the file - {e}")

    devices_data = data.get("devices_devices", [])
    results = []

    for device in devices_data:
        string_map_data = device.get("string_map_data", {})
        user_agent = string_map_data.get("User Agent", {}).get("value", "")
        last_login_timestamp = string_map_data.get("Last Login", {}).get("timestamp", None)

        if user_agent and last_login_timestamp is not None:
            device_id = user_agent  # Assuming 'User Agent' contains 'Device ID'
            login_time = convert_timestamp(last_login_timestamp)
            results.append((device_id, login_time))

    return results

# Function to write results to CSV
def write_results_to_csv(results, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Device ID", "Login Time"])
            csvwriter.writerows(results)
    except Exception as e:
        raise ValueError(f"Error: Failed to write to CSV file - {e}")

# Main function to execute the script
def main():
    try:
        results = process_devices_file(devices_file_path)
        write_results_to_csv(results, output_csv_path)
    except Exception as e:
        # If any error occurs, write only the headers to the CSV
        write_results_to_csv([], output_csv_path)
        print(e)

if __name__ == "__main__":
    main()