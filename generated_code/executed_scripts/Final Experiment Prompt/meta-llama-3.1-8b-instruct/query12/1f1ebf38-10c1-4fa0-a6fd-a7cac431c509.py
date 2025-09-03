import csv
import os
import datetime
import json

root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Week', 'Messages Sent']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate over each subfolder in the inbox directory
    for folder in os.listdir(os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox')):
        folder_path = os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox', folder)
        if os.path.isdir(folder_path):
            # Initialize the message count for the current week
            week_messages = 0

            # Iterate over each message file in the subfolder
            for file in os.listdir(folder_path):
                if file.startswith('message_') and file.endswith('.json'):
                    file_path = os.path.join(folder_path, file)
                    try:
                        with open(file_path, 'r') as json_file:
                            data = json.load(json_file)
                            # Check if the 'timestamp_ms' key exists in the data
                            if 'timestamp_ms' in data:
                                # Get the timestamp in seconds
                                timestamp = int(data['timestamp_ms']) / 1000
                                # Get the week from the timestamp
                                week = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%W')
                                # Increment the message count for the current week
                                week_messages += 1
                            else:
                                # If the 'timestamp_ms' key does not exist, treat its contribution as 0
                                pass
                    except FileNotFoundError:
                        # If the file does not exist, treat its contribution as 0
                        pass
                    except json.JSONDecodeError:
                        # If the file is not a valid JSON file, treat its contribution as 0
                        pass

            # Write the message count for the current week to the CSV file
            writer.writerow({'Week': folder, 'Messages Sent': week_messages})