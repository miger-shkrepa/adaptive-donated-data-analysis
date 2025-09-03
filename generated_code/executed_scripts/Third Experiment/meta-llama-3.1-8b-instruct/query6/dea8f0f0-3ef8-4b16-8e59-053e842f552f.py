import csv
import os
import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list of changes
changes = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the required information
            if "string_map_data" in data and "title" in data["string_map_data"]:
                # Iterate over the string map data
                for key, value in data["string_map_data"].items():
                    # Check if the value is a dictionary with the required keys
                    if "href" in value and "timestamp" in value and "value" in value:
                        # Extract the change information
                        change = {
                            "Changed": key,
                            "New Value": value["value"],
                            "Change Date": datetime.datetime.fromtimestamp(value["timestamp"]).strftime("%Y-%m-%d")
                        }

                        # Add the change to the list of changes
                        changes.append(change)

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ["Changed", "New Value", "Change Date"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the column headers
    writer.writeheader()

    # Write the changes
    for change in changes:
        writer.writerow(change)