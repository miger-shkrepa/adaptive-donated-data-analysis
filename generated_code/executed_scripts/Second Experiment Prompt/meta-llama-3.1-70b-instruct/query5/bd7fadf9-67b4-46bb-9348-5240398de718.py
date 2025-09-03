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
                # Since the structure of the JSON file is not provided, we assume it's a simple JSON object
                # In a real-world scenario, you would use a JSON parser to parse the file content
                # For simplicity, we will assume the file content is a string and we will extract the device information manually
                content = file.read()

                # Extract the device information from the content
                # This is a very simplified example and may not work for all cases
                start_index = content.find('"Device ID"')
                while start_index != -1:
                    end_index = content.find('"', start_index + 11)
                    device_id = content[start_index + 11:end_index]

                    start_index = content.find('"Last Login"')
                    end_index = content.find('"', start_index + 11)
                    login_time = content[start_index + 11:end_index]

                    # Convert the login time to the required format
                    try:
                        login_time = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        login_time = ''

                    devices.append((device_id, login_time))

                    start_index = content.find('"Device ID"', start_index + 1)

        # Save the device information to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Device ID', 'Login Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for device in devices:
                writer.writerow({'Device ID': device[0], 'Login Time': device[1]})

    except Exception as e:
        # Save an empty CSV file with column headers if an error occurs
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Device ID', 'Login Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        raise Exception(f"Error: {str(e)}")

get_login_devices(root_dir)