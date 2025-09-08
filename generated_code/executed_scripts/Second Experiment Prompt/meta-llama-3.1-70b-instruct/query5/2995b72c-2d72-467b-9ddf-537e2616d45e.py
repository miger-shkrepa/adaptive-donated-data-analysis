import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_login_devices(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize the list to store device information
        devices = []

        # Define the path to the devices.json file
        devices_file_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")

        # Check if the devices.json file exists
        if os.path.exists(devices_file_path):
            # Open the devices.json file and read its content
            with open(devices_file_path, 'r') as file:
                # Since the JSON structure is known, we can parse it manually
                content = file.read()
                # Find the start of the JSON data
                start_idx = content.find('{"devices_devices"')
                if start_idx != -1:
                    # Find the end of the JSON data
                    end_idx = content.find('}', start_idx) + 1
                    # Extract the JSON data
                    json_data = content[start_idx:end_idx]
                    # Parse the JSON data
                    devices_data = eval(json_data)
                    # Extract the device information
                    for device in devices_data['devices_devices']:
                        device_id = device['string_map_data'].get('Device ID', {}).get('value')
                        login_time = device['string_map_data'].get('Last Login', {}).get('value')
                        if login_time:
                            # Convert the login time to the required format
                            login_time = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            login_time = ''
                        devices.append((device_id, login_time))
        else:
            # If the devices.json file does not exist, return an empty list
            devices = []

        return devices

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(devices):
    try:
        # Define the path to the output CSV file
        output_file_path = 'query_responses/results.csv'

        # Create the output directory if it does not exist
        output_dir = os.path.dirname(output_file_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the device information to the CSV file
        with open(output_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Device ID', 'Login Time'])
            for device in devices:
                writer.writerow(device)

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        devices = get_login_devices(root_dir)
        save_to_csv(devices)
    except Exception as e:
        print("Error: " + str(e))
        # Save an empty CSV file with column headers if an error occurs
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Device ID', 'Login Time'])

if __name__ == "__main__":
    main()