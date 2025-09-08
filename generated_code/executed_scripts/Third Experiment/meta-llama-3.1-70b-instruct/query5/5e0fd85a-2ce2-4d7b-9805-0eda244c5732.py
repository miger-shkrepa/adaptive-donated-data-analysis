import os
import csv
import json

root_dir = "root_dir"

def get_device_login_info(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize the list to store device login information
        device_login_info = []

        # Iterate over the directories in the root directory
        for dir_name in os.listdir(root_dir):
            dir_path = os.path.join(root_dir, dir_name)

            # Check if the directory is 'personal_information'
            if dir_name == 'personal_information':
                # Iterate over the files in the 'personal_information' directory
                for file_name in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, file_name)

                    # Check if the file is 'device_information'
                    if file_name == 'device_information':
                        # Iterate over the files in the 'device_information' directory
                        for device_file_name in os.listdir(file_path):
                            device_file_path = os.path.join(file_path, device_file_name)

                            # Check if the file is 'devices.json'
                            if device_file_name == 'devices.json':
                                try:
                                    # Open and read the 'devices.json' file
                                    with open(device_file_path, 'r') as device_file:
                                        device_data = json.load(device_file)

                                        # Iterate over the devices in the 'devices.json' file
                                        for device in device_data['devices_devices']:
                                            # Get the device ID and login time
                                            device_id = device['title']
                                            login_time = device['string_map_data']['Last Login']['value']

                                            # Convert the login time to the required format
                                            login_time = login_time[:4] + '-' + login_time[4:6] + '-' + login_time[6:8] + ' ' + login_time[8:10] + ':' + login_time[10:12] + ':' + login_time[12:14]

                                            # Add the device ID and login time to the list
                                            device_login_info.append([device_id, login_time])

                                except json.JSONDecodeError:
                                    raise ValueError("ValueError: The 'devices.json' file is not a valid JSON file.")

        return device_login_info

    except Exception as e:
        raise Exception("Error: " + str(e))

def save_to_csv(device_login_info):
    try:
        # Save the device login information to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Device ID', 'Login Time'])

            # Check if the device login information list is empty
            if device_login_info:
                csv_writer.writerows(device_login_info)
            else:
                # If the list is empty, write only the column headers
                csv_writer.writerow(['Device ID', 'Login Time'])

    except Exception as e:
        raise Exception("Error: " + str(e))

def main():
    try:
        device_login_info = get_device_login_info(root_dir)
        save_to_csv(device_login_info)

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()