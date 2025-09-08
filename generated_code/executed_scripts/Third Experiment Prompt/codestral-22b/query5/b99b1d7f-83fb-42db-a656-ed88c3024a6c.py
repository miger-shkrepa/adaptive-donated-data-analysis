import os
import json
import csv
from datetime import datetime

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the results
results = []

# Define the path to the login activity file
login_activity_file = os.path.join(root_dir, "security_and_login_information", "login_and_account_creation", "login_activity.json")

# Check if the login activity file exists
if os.path.exists(login_activity_file):
    # Open the login activity file
    with open(login_activity_file, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Check if the data is a list
        if isinstance(data, list):
            # Iterate over the list
            for item in data:
                # Check if the item is a dictionary
                if isinstance(item, dict):
                    # Check if the item contains the string_map_data key
                    if "string_map_data" in item:
                        # Get the string_map_data
                        string_map_data = item["string_map_data"]

                        # Check if the string_map_data contains the Device ID and Time keys
                        if "Name des Cookies" in string_map_data and "Zeit" in string_map_data:
                            # Get the Device ID and Time
                            device_id = string_map_data["Name des Cookies"]["value"]
                            login_time = string_map_data["Zeit"]["value"]

                            # Convert the login time to the desired format
                            login_time = datetime.strptime(login_time, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d %H:%M:%S")

                            # Append the results to the list
                            results.append([device_id, login_time])

# Define the path to the output file
output_file = "query_responses/results.csv"

# Create the directory if it does not exist
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Open the output file
with open(output_file, "w", newline="") as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the header
    writer.writerow(["Device ID", "Login Time"])

    # Write the results
    writer.writerows(results)