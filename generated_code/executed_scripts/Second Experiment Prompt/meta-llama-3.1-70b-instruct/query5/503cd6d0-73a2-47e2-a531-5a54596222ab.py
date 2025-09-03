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
                content = file.read()

                # Assuming the content is a list of devices
                # In a real-world scenario, you would use a JSON parser to parse the content
                devices_info = eval(content)

                # Iterate over the devices
                for device in devices_info.get("devices_devices", []):
                    # Extract the device ID and login time
                    device_id = device.get("string_map_data", {}).get("Device ID", {}).get("value")
                    login_time = device.get("string_map_data", {}).get("Last Login", {}).get("value")

                    # Convert the login time to the required format
                    if login_time:
                        try:
                            login_time = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            login_time = None

                    # Add the device information to the list
                    devices.append((device_id, login_time))

        # Return the list of devices
        return devices

    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def save_to_csv(devices):
    try:
        # Define the path to the output CSV file
        output_file_path = "query_responses/results.csv"

        # Create the output directory if it does not exist
        output_dir = os.path.dirname(output_file_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Open the output CSV file and write the device information
        with open(output_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Device ID", "Login Time"])  # Write the header

            # Write the device information
            for device in devices:
                writer.writerow(device)

    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def main():
    try:
        devices = get_login_devices(root_dir)

        # If no devices are found, save a CSV file with only the column headers
        if not devices:
            devices = []

        save_to_csv(devices)

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()