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
                # Since the JSON structure is complex and we don't have the json library, we'll assume the file has the expected structure
                # and parse it manually. This might not work for all possible JSON structures.
                content = file.read()
                # Remove the 'devices_devices' and 'media_map_data' parts
                content = content.replace('{"devices_devices": [', '').replace(',"media_map_data": {}', '')
                # Split the content into individual devices
                devices_content = content.split('}, {"string_map_data": {')
                for device_content in devices_content:
                    # Extract the device ID and login time
                    device_id = None
                    login_time = None
                    lines = device_content.split(', ')
                    for line in lines:
                        if '"Device ID"' in line:
                            device_id = line.split(': ')[1].strip('"')
                        elif '"Last Login"' in line:
                            login_time = line.split(': ')[1].strip('"')
                    if device_id and login_time:
                        # Convert the login time to the required format
                        try:
                            login_time = datetime.utcfromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            # If the conversion fails, skip this device
                            continue
                        devices.append((device_id, login_time))
        else:
            # If the devices.json file does not exist, return an empty list
            pass

        return devices

    except Exception as e:
        raise ValueError("Error: An unexpected error occurred: " + str(e))

def save_to_csv(devices):
    try:
        # Define the path to the output CSV file
        output_file_path = 'query_responses/results.csv'

        # Create the output directory if it does not exist
        output_dir = os.path.dirname(output_file_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the devices to the CSV file
        with open(output_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Device ID", "Login Time"])
            for device in devices:
                writer.writerow(device)

    except Exception as e:
        raise ValueError("Error: Failed to save the results to the CSV file: " + str(e))

def main():
    try:
        devices = get_login_devices(root_dir)
        if not devices:
            # If no devices are found, save a CSV file with only the column headers
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Device ID", "Login Time"])
        else:
            save_to_csv(devices)
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()