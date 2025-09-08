import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the results
results = []

# Iterate over each file in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a directory
    if os.path.isdir(os.path.join(root_dir, filename)):
        # Iterate over each file in the subdirectory
        for subfilename in os.listdir(os.path.join(root_dir, filename)):
            # Check if the file is a JSON file
            if subfilename.endswith(".json"):
                # Open the JSON file
                with open(os.path.join(root_dir, filename, subfilename), 'r') as file:
                    # Read the JSON file
                    data = file.read()
                    # Parse the JSON data
                    import json
                    parsed_data = json.loads(data)
                    # Check if the JSON data contains the 'messages' key
                    if 'messages' in parsed_data:
                        # Iterate over each message in the 'messages' list
                        for message in parsed_data['messages']['inbox']['message_1.json']['structure']['messages']:
                            # Check if the message contains the 'timestamp_ms' key
                            if 'timestamp_ms' in message:
                                # Extract the timestamp from the message
                                timestamp = int(message['timestamp_ms'])
                                # Calculate the week from the timestamp
                                week = timestamp // (7 * 24 * 60 * 60 * 1000)
                                # Increment the count of messages sent in the week
                                results.append((f"Week {week // 100}{'-' + str(week % 100).zfill(2) if week % 100 != 0 else ''}", 1))

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(['Week', 'Messages Sent'])
    # Write the results
    for result in results:
        writer.writerow(result)

# Check if the CSV file was written successfully
if not os.path.exists('query_responses/results.csv'):
    raise ValueError("ValueError: The CSV file was not written successfully.")