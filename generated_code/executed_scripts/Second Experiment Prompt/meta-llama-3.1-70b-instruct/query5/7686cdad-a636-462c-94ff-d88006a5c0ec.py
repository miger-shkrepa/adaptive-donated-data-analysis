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
                # Since the file structure is not a standard JSON, we'll assume it's a text file with a specific format
                # We'll iterate over each line in the file
                for line in file:
                    # We'll check if the line contains the required information
                    if "Device ID" in line and "Last Login" in line:
                        # We'll extract the device ID and login time from the line
                        device_id = line.split("Device ID")[1].split(":")[1].strip().replace('"', '')
                        login_time = line.split("Last Login")[1].split(":")[1].strip().replace('"', '')

                        # We'll convert the login time to the required format
                        login_time = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')

                        # We'll add the device information to the list
                        devices.append((device_id, login_time))

        # Return the list of devices
        return devices

    except Exception as e:
        # Raise an exception with the error message
        raise ValueError("Error: " + str(e))

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
        # Raise an exception with the error message
        raise ValueError("Error: " + str(e))

def main():
    try:
        # Get the device information
        devices = get_login_devices(root_dir)

        # Save the device information to a CSV file
        save_to_csv(devices)

    except FileNotFoundError as e:
        # If the root directory does not exist, create a CSV file with only the column headers
        with open("query_responses/results.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Device ID", "Login Time"])
        print(e)
    except Exception as e:
        # Print the error message
        print("Error: " + str(e))

if __name__ == "__main__":
    main()