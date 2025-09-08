import csv
import os
import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the changes
changes = []

# Iterate over the JSON files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = file.read()
            # Parse the JSON data
            import json
            json_data = json.loads(data)
            # Check if the JSON data contains the required information
            if 'relationships_following' in json_data:
                # Iterate over the relationships in the JSON data
                for relationship in json_data['relationships_following']:
                    # Check if the relationship contains the required information
                    if 'title' in relationship and 'string_list_data' in relationship:
                        # Iterate over the string list data in the relationship
                        for string_data in relationship['string_list_data']:
                            # Check if the string data contains the required information
                            if 'value' in string_data:
                                # Extract the value from the string data
                                value = string_data['value']
                                # Extract the timestamp from the string data
                                timestamp = string_data['timestamp']
                                # Convert the timestamp to a date string
                                date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                                # Append the change to the list
                                changes.append((filename, value, date))

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create a CSV writer
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(['Changed', 'New Value', 'Change Date'])
    # Write the changes
    for change in changes:
        writer.writerow(change)