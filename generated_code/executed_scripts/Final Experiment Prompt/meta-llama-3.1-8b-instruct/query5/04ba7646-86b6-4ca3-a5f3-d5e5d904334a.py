import csv
import json
import os

# Set the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Set the input file path
input_file_path = os.path.join(root_dir, 'personal_information', 'device_information', 'devices.json')

# Check if the input file exists
if not os.path.exists(input_file_path):
    print("Warning: Input file does not exist. Returning CSV file with only column headers.")
else:
    try:
        # Load the JSON data
        with open(input_file_path, 'r') as input_file:
            data = json.load(input_file)

        # Extract the device information
        device_info = data['devices_devices']

        # Initialize the CSV writer
        with open('query_responses/results.csv', 'w', newline='') as output_file:
            writer = csv.writer(output_file)

            # Write the column headers
            writer.writerow(['Device ID', 'Login Time'])

            # Iterate over the device information
            for device in device_info:
                user_agent = device['string_map_data']['User Agent']['value']
                last_login_timestamp = device['string_map_data']['Last Login']['timestamp']

                # Write the device information to the CSV file
                writer.writerow([user_agent, last_login_timestamp])

    except json.JSONDecodeError as e:
        raise ValueError("Error: Failed to parse JSON data: " + str(e))
    except Exception as e:
        raise Exception("Error: An unexpected error occurred: " + str(e))