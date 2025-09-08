import csv
import json
import os

# Set the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Set the input file path
input_file = os.path.join(root_dir, 'personal_information', 'device_information', 'devices.json')

# Check if the input file exists
if not os.path.exists(input_file):
    print("Warning: Input file does not exist. Returning CSV file with only column headers.")
else:
    try:
        # Load the JSON data
        with open(input_file, 'r') as f:
            data = json.load(f)

        # Extract the required data
        device_ids = []
        login_times = []
        for device in data['devices_devices']:
            user_agent = device['string_map_data']['User Agent']['value']
            last_login = device['string_map_data']['Last Login']['value']
            timestamp = device['string_map_data']['Last Login']['timestamp']
            login_time = last_login + ' ' + str(timestamp)
            device_ids.append(user_agent)
            login_times.append(login_time)

        # Create the CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
            for device_id, login_time in zip(device_ids, login_times):
                writer.writerow([device_id, login_time])

        print("CSV file saved to query_responses/results.csv")

    except json.JSONDecodeError as e:
        raise ValueError("Error: Failed to parse JSON data: " + str(e))
    except KeyError as e:
        raise ValueError("Error: Missing key in JSON data: " + str(e))