import os
import csv
import json
import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the results list
results = []

# Iterate over all subdirectories in the root directory
for dirpath, dirnames, filenames in os.walk(root_dir):
    # Check if the subdirectory is an 'inbox' directory
    if dirnames and dirnames[0] == 'inbox':
        # Get the week number from the directory path
        week_dir = os.path.basename(dirpath)
        try:
            week = datetime.datetime.strptime(week_dir, '%Y-%m-%d').strftime('%Y-%W')
        except ValueError:
            # If the directory path does not match the expected format, treat its contribution as 0
            continue

        # Initialize the messages sent for this week
        messages_sent = 0

        # Iterate over all files in the subdirectory
        for filename in filenames:
            # Check if the file is a message_X.json file
            if filename.startswith('message_') and filename.endswith('.json'):
                # Get the file path
                filepath = os.path.join(dirpath, filename)

                # Try to open and read the file
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                except FileNotFoundError:
                    # If the file does not exist, treat its contribution as 0
                    continue
                except json.JSONDecodeError:
                    # If the file is not a valid JSON file, treat its contribution as 0
                    continue

                # Get the messages from the file
                messages = data.get('messages', [])

                # Increment the messages sent for this week
                messages_sent += len(messages)

        # Append the results for this week
        results.append((week, messages_sent))

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Week', 'Messages Sent'])
    writer.writerows(results)