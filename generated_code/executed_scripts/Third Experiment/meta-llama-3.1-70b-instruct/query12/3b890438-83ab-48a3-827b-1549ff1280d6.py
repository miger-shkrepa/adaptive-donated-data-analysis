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
                                for message in data['messages']:
                                    # Check if the message is sent by the user
                                    if 'sender_name' in message:
                                        timestamp_ms = message['timestamp_ms']
                                        timestamp = datetime.fromtimestamp(timestamp_ms / 1000)
                                        week = timestamp.strftime('Week %Y-%U')
                                        if week not in messages_sent_per_week:
                                            messages_sent_per_week[week] = 0
                                        messages_sent_per_week[week] += 1

        # Write the results to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Week', 'Messages Sent']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for week, messages_sent in messages_sent_per_week.items():
                writer.writerow({'Week': week, 'Messages Sent': messages_sent})

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: {e}")
    except Exception as e:
        raise Exception(f"Error: {e}")

get_messages_sent_per_week(root_dir)