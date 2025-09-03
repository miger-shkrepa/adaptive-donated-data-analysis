import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def extract_device_info(root_dir):
    try:
        # Define the path to the devices.json file
        devices_file_path = os.path.join(root_dir, 'personal_information', 'device_information', 'devices.json')

        # Check if the file exists
        if not os.path.exists(devices_file_path):
            raise FileNotFoundError("FileNotFoundError: The devices.json file does not exist.")

        # Read the JSON file
        with open(devices_file_path, 'r') as file:
            data = json.load(file)

        # Extract the devices_devices list
        devices_devices = data.get('devices_devices', [])

        # Prepare the CSV data
        csv_data = [["Device ID", "Login Time"]]

        for device in devices_devices:
            string_map_data = device.get('string_map_data', {})
            user_agent = string_map_data.get('User Agent', {}).get('value', '')
            last_login_timestamp = string_map_data.get('Last Login', {}).get('timestamp', 0)

            # Extract Device ID from User Agent
            device_id = user_agent.split()[0] if user_agent else 'Unknown'

            # Convert timestamp to datetime
            login_time = datetime.utcfromtimestamp(last_login_timestamp).strftime('%Y-%m-%d %H:%M:%S')

            # Append to CSV data
            csv_data.append([device_id, login_time])

        # Write the CSV data to the output file
        output_file_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        with open(output_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(csv_data)

    except FileNotFoundError as fnf_error:
        print(fnf_error)
        # Create a CSV file with only the column headers
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Device ID", "Login Time"])
    except ValueError as val_error:
        print(f"ValueError: {val_error}")
    except Exception as e:
        print(f"Error: {e}")

# Execute the function
extract_device_info(root_dir)