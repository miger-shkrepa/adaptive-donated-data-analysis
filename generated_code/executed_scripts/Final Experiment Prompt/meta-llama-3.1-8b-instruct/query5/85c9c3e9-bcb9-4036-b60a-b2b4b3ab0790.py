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

        # Extract the device information
        devices = data['devices_devices']

        # Initialize the CSV writer
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write the column headers
            writer.writerow(['Device ID', 'Login Time'])

            # Iterate over the devices
            for device in devices:
                user_agent = device['string_map_data']['User Agent']['value']
                login_time = device['string_map_data']['Last Login']['timestamp']

                # Write the device information to the CSV file
                writer.writerow([user_agent, login_time])

    except json.JSONDecodeError as e:
        raise ValueError("Error: Failed to parse JSON data: " + str(e))
    except Exception as e:
        raise Exception("Error: An unexpected error occurred: " + str(e))