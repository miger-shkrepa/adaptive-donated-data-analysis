import os
import json
import csv
from datetime import datetime

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the messages sent per week
messages_per_week = {}

# Traverse the directory
for dirpath, dirnames, filenames in os.walk(root_dir):
    # Check if the current directory is a conversation directory
    if 'message_1.json' in filenames:
        # Sort the filenames to ensure they are processed in order
        filenames.sort()
        for filename in filenames:
            # Check if the file is a message file
            if filename.startswith('message_') and filename.endswith('.json'):
                try:
                    # Open the file
                    with open(os.path.join(dirpath, filename), 'r') as f:
                        # Load the JSON data
                        data = json.load(f)
                        # Extract the timestamp
                        timestamp = data.get('timestamp')
                        if timestamp is not None:
                            # Convert the timestamp to a datetime object
                            dt = datetime.fromtimestamp(timestamp)
                            # Format the datetime object to get the week
                            week = dt.strftime('%Y-%W')
                            # Increment the count for this week
                            if week in messages_per_week:
                                messages_per_week[week] += 1
                            else:
                                messages_per_week[week] = 1
                except Exception as e:
                    print(f"Error processing file {filename}: {e}")

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    # Write the header
    writer.writerow(['Week', 'Messages Sent'])
    # Write the data
    for week, count in messages_per_week.items():
        writer.writerow([f'Week {week}', count])