import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("Error: The root directory does not exist.")

# Initialize a dictionary to store the count of messages per week
messages_per_week = {}

# Walk through the directory structure
for dirpath, dirnames, filenames in os.walk(root_dir):
    if 'inbox' in dirpath:
        for filename in filenames:
            if filename.startswith('message_') and filename.endswith('.json'):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        # Assuming the timestamp is in the 'timestamp' field
                        timestamp = data.get('timestamp')
                        if timestamp:
                            # Convert timestamp to datetime object
                            message_date = datetime.fromtimestamp(timestamp)
                            # Get the week number and year
                            week_number = message_date.strftime('%Y-%U')
                            # Increment the message count for the week
                            if week_number in messages_per_week:
                                messages_per_week[week_number] += 1
                            else:
                                messages_per_week[week_number] = 1
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"Error processing file {file_path}: {e}")

# Write the results to a CSV file
try:
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Week', 'Messages Sent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for week, count in messages_per_week.items():
            writer.writerow({'Week': f'Week {week}', 'Messages Sent': count})
except Exception as e:
    raise IOError(f"Error: Unable to write to the output CSV file. {e}")