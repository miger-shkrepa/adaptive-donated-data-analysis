import os
import json
import csv

root_dir = "root_dir"

def get_devices_login_time(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize lists to store device IDs and login times
        device_ids = []
        login_times = []

        # Iterate over all files in the root directory
        for filename in os.listdir(root_dir):
            # Check if the file is 'devices.json'
            if filename == 'devices.json':
                # Open the 'devices.json' file
                with open(os.path.join(root_dir, filename), 'r') as file:
                    # Load the JSON data
                    data = json.load(file)

                    # Iterate over the devices
                    for device in data['devices_devices']:
                        # Get the device ID and login time
                        device_id = device['title']
                        login_time = device['string_map_data']['Last Login']['value']

                        # Convert the login time to the required format
                        login_time = convert_timestamp_to_datetime(login_time)

                        # Append the device ID and login time to the lists
                        device_ids.append(device_id)
                        login_times.append(login_time)

        # Save the results to a CSV file
        save_to_csv(device_ids, login_times)

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Error parsing JSON - {e}")
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred - {e}")


def convert_timestamp_to_datetime(timestamp):
    try:
        # Convert the timestamp to a datetime object
        from datetime import datetime
        dt = datetime.fromtimestamp(int(timestamp))

        # Return the datetime object in the required format
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        raise ValueError(f"ValueError: Error converting timestamp to datetime - {e}")


def save_to_csv(device_ids, login_times):
    try:
        # Check if the output directory exists
        output_dir = 'query_responses'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the results to a CSV file
        with open(os.path.join(output_dir, 'results.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Device ID', 'Login Time'])
            for device_id, login_time in zip(device_ids, login_times):
                writer.writerow([device_id, login_time])
    except Exception as e:
        raise ValueError(f"ValueError: Error saving to CSV - {e}")


if __name__ == "__main__":
    get_devices_login_time(root_dir)