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
    writer = csv.writer(csvfile)
    writer.writerow(['Week', 'Messages Sent'])

    # Iterate over each subfolder in the inbox directory
    for folder in os.listdir(os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox')):
        folder_path = os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox', folder)
        
        # Check if the folder exists
        if not os.path.exists(folder_path):
            continue
        
        # Initialize the message count for the current week
        week_messages = 0
        
        # Iterate over each message file in the folder
        for file in os.listdir(folder_path):
            if file.startswith('message_') and file.endswith('.json'):
                file_path = os.path.join(folder_path, file)
                
                # Check if the file exists
                if not os.path.exists(file_path):
                    continue
                
                # Load the JSON data from the file
                try:
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                        
                        # Get the timestamp from the message
                        timestamp_ms = data['messages'][0]['timestamp_ms']
                        
                        # Convert the timestamp to a datetime object
                        timestamp = datetime.datetime.fromtimestamp(timestamp_ms / 1000)
                        
                        # Get the week from the timestamp
                        week = timestamp.strftime('%Y-%W')
                        
                        # Increment the message count for the current week
                        week_messages += 1
                except (FileNotFoundError, json.JSONDecodeError):
                    # If the file does not exist or the JSON data is invalid, treat its contribution as 0
                    pass
        
        # Write the message count for the current week to the CSV file
        writer.writerow([week, week_messages])