import csv
import os
import json

# Declare the variable referring to the file input
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
            
            # Check if the JSON data contains the required structure
            if 'devices.json' in data and 'devices_devices' in data['devices.json'] and 'string_map_data' in data['devices.json']['devices_devices'][0]:
                # Iterate over the devices
                for device in data['devices.json']['devices_devices']:
                    # Check if the device has a 'Last Login' entry
                    if 'Last Login' in device['string_map_data']:
                        # Extract the login time
                        login_time = device['string_map_data']['Last Login']['value']
                        
                        # Add the result to the list
                        results.append([device['title'], login_time])

# Create the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create the CSV writer
    writer = csv.writer(csvfile)
    
    # Write the column headers
    writer.writerow(['Device ID', 'Login Time'])
    
    # Write the results
    for result in results:
        writer.writerow(result)

print("Query completed successfully.")