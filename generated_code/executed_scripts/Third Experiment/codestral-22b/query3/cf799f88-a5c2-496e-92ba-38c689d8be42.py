import os
import json
import csv
from datetime import datetime, timedelta
from collections import defaultdict

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("Error: The root directory does not exist.")

# Initialize the data structure to store the results
results = defaultdict(lambda: {"Daily": 0, "Weekly": 0})

# Traverse the directory structure
for foldername, subfolders, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.json'):
            filepath = os.path.join(foldername, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    if 'structure' in data and 'messages' in data['structure']:
                        for message in data['structure']['messages']:
                            if 'timestamp_ms' in message:
                                timestamp = int(message['timestamp_ms']) / 1000.0  # Convert to seconds
                                date = datetime.fromtimestamp(timestamp)
                                week = date.strftime("%Y-%W")
                                day = date.strftime("%Y-%m-%d")
                                results[day]["Daily"] += 1
                                results[week]["Weekly"] += 1
            except Exception as e:
                print(f"Error processing file {filepath}: {str(e)}")

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for date_week, counts in results.items():
        writer.writerow({'Date/Week': date_week, 'Posts Viewed': counts['Daily'], 'Type': 'Daily'})
        writer.writerow({'Date/Week': date_week, 'Posts Viewed': counts['Weekly'], 'Type': 'Weekly'})