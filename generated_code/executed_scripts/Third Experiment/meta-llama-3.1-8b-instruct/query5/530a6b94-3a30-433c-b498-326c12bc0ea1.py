import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the results
results = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = json.load(file)
            
            # Check if the JSON data contains the required information
            if "devices_devices" in data["structure"]["devices_devices"]:
                # Iterate over the devices
                for device in data["structure"]["devices_devices"]:
                    # Check if the device has a login time
                    if "Last Login" in device["string_map_data"]:
                        # Extract the login time
                        login_time = device["string_map_data"]["Last Login"]["value"]
                        
                        # Extract the device ID
                        device_id = device["string_map_data"]["Device ID"]["value"]
                        
                        # Add the result to the list
                        results.append([device_id, login_time])

# Check if there are any results
if results:
    # Open the CSV file for writing
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        # Create the CSV writer
        writer = csv.writer(csvfile)
        
        # Write the header
        writer.writerow(["Device ID", "Login Time"])
        
        # Write the results
        writer.writerows(results)
else:
    # Open the CSV file for writing
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        # Create the CSV writer
        writer = csv.writer(csvfile)
        
        # Write the header
        writer.writerow(["Device ID", "Login Time"])
        
        # Write an empty row
        writer.writerow(["", ""])