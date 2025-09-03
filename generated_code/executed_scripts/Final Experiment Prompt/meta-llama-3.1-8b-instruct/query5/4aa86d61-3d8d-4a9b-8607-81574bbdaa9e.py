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

        # Initialize the output data
        output_data = []

        # Iterate over the devices
        for device in devices:
            # Extract the device ID and login time
            device_id = device['string_map_data']['User Agent']['value']
            login_time = device['string_map_data']['Last Login']['timestamp']

            # Append the data to the output list
            output_data.append([device_id, login_time])

        # Write the output data to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])  # Write the column headers
            writer.writerows(output_data)

        print("Output CSV file written to query_responses/results.csv")

    except json.JSONDecodeError as e:
        raise ValueError("Error: Failed to parse JSON data: " + str(e))
    except KeyError as e:
        raise ValueError("Error: Missing key in JSON data: " + str(e))