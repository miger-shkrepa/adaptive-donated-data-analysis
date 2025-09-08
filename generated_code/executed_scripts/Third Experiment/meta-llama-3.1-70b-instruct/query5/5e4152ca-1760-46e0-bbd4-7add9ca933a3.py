import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_login_devices(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize the list to store device IDs and login times
        login_devices = []

        # Iterate over the files in the root directory
        for filename in os.listdir(root_dir):
            # Check if the file is 'login_activity.json'
            if filename == 'login_activity.json':
                # Open the 'login_activity.json' file
                with open(os.path.join(root_dir, filename), 'r') as file:
                    # Read the JSON data
                    import json
                    data = json.load(file)

                    # Iterate over the login history
                    for login in data['account_history_login_history']:
                        # Get the device ID and login time
                        device_id = login['string_map_data']['IP Address']['value']
                        login_time = login['string_map_data']['Time']['value']

                        # Convert the login time to the required format
                        try:
                            login_time = datetime.strptime(login_time, '%Y-%m-%d %H:%M:%S')
                            login_time = login_time.strftime('%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            # If the login time is not in the correct format, skip this login
                            continue

                        # Add the device ID and login time to the list
                        login_devices.append((device_id, login_time))

        # Return the list of device IDs and login times
        return login_devices

    except Exception as e:
        # Raise the exception with the required format
        raise Exception(f"Error: {str(e)}")

def save_to_csv(login_devices):
    try:
        # Open the CSV file for writing
        with open('query_responses/results.csv', 'w', newline='') as file:
            # Create a CSV writer
            writer = csv.writer(file)

            # Write the column headers
            writer.writerow(['Device ID', 'Login Time'])

            # Write the device IDs and login times
            for device_id, login_time in login_devices:
                writer.writerow([device_id, login_time])

    except Exception as e:
        # Raise the exception with the required format
        raise Exception(f"Error: {str(e)}")

def main():
    try:
        # Get the device IDs and login times
        login_devices = get_login_devices(root_dir)

        # Save the device IDs and login times to a CSV file
        save_to_csv(login_devices)

    except FileNotFoundError as e:
        # If the root directory does not exist, create a CSV file with only the column headers
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Device ID', 'Login Time'])
        raise Exception(f"Error: {str(e)}")

    except Exception as e:
        # Raise the exception with the required format
        raise Exception(f"Error: {str(e)}")

if __name__ == '__main__':
    main()