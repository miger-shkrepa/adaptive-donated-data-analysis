import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_messages_sent_per_week(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store the messages sent per week
        messages_sent_per_week = {}

        # Iterate over the subfolders in the 'inbox' directory
        inbox_dir = os.path.join(root_dir, 'messages', 'inbox')
        if os.path.exists(inbox_dir):
            for subfolder in os.listdir(inbox_dir):
                subfolder_path = os.path.join(inbox_dir, subfolder)
                if os.path.isdir(subfolder_path):
                    # Iterate over the message_X.json files in the subfolder
                    for filename in os.listdir(subfolder_path):
                        if filename.startswith('message_') and filename.endswith('.json'):
                            file_path = os.path.join(subfolder_path, filename)
                            with open(file_path, 'r') as file:
                                data = json.load(file)
                                for message in data['structure']['messages']:
                                    if 'sender_name' in message:
                                        # Get the timestamp of the message
                                        timestamp_ms = message['timestamp_ms']
                                        # Convert the timestamp to a datetime object
                                        dt = datetime.fromtimestamp(timestamp_ms / 1000)
                                        # Get the week of the year
                                        week = dt.strftime('Week %Y-%U')
                                        # Increment the count of messages sent in the week
                                        if week in messages_sent_per_week:
                                            messages_sent_per_week[week] += 1
                                        else:
                                            messages_sent_per_week[week] = 1

        # Write the results to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Week', 'Messages Sent'])
            for week, count in messages_sent_per_week.items():
                writer.writerow([week, count])

    except Exception as e:
        raise ValueError("Error: " + str(e))

get_messages_sent_per_week(root_dir)