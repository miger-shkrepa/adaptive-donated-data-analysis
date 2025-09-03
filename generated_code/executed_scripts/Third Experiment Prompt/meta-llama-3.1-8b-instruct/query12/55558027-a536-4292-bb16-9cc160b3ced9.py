import os
import csv
import json
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the results list
results = []

# Iterate over all subdirectories in the root directory
for dirpath, dirnames, filenames in os.walk(root_dir):
    # Check if the subdirectory is the 'inbox' directory
    if dirnames and dirnames[0] == 'inbox':
        # Iterate over all message_X.json files in the subdirectory
        for filename in filenames:
            if filename.startswith('message_') and filename.endswith('.json'):
                # Extract the conversation ID from the filename
                conversation_id = filename.split('_')[1].split('.')[0]
                # Construct the full path to the message_X.json file
                filepath = os.path.join(dirpath, filename)
                try:
                    # Open the message_X.json file and load its contents
                    with open(filepath, 'r') as f:
                        message_data = json.load(f)
                    # Extract the timestamp of the message
                    timestamp = message_data['timestamp_ms']
                    # Convert the timestamp to a datetime object
                    dt = datetime.fromtimestamp(timestamp / 1000)
                    # Extract the week number from the datetime object
                    week = dt.strftime('%Y-%W')
                    # Increment the message count for the week
                    results.append((week, 1))
                except FileNotFoundError:
                    # If the message_X.json file does not exist, treat its contribution as 0
                    results.append((week, 0))
                except json.JSONDecodeError:
                    # If the message_X.json file is not a valid JSON file, treat its contribution as 0
                    results.append((week, 0))

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Week', 'Messages Sent'])
    writer.writerows(results)