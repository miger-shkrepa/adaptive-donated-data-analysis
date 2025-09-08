import os
import json
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Check if the 'inbox' directory exists
    inbox_path = os.path.join(root_dir, 'inbox')
    if not os.path.exists(inbox_path):
        # If 'inbox' directory does not exist, create a CSV with only headers
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Week', 'Messages Sent'])
        print("CSV file created with headers only as 'inbox' directory is missing.")
        exit()

    # Initialize a dictionary to count messages per week
    messages_per_week = {}

    # Iterate over each conversation folder in 'inbox'
    for conversation_folder in os.listdir(inbox_path):
        conversation_path = os.path.join(inbox_path, conversation_folder)
        if os.path.isdir(conversation_path):
            message_files = [f for f in os.listdir(conversation_path) if f.startswith('message_') and f.endswith('.json')]
            message_files.sort()  # Ensure files are processed in order

            for message_file in message_files:
                message_path = os.path.join(conversation_path, message_file)
                with open(message_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    for message in data.get('messages', []):
                        timestamp_ms = message.get('timestamp_ms')
                        if timestamp_ms:
                            timestamp = datetime.fromtimestamp(timestamp_ms / 1000)
                            week = timestamp.strftime('Week %Y-%W')
                            messages_per_week[week] = messages_per_week.get(week, 0) + 1

    # Write the results to a CSV file
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Week', 'Messages Sent'])
        for week, count in sorted(messages_per_week.items()):
            writer.writerow([week, count])

except FileNotFoundError as e:
    print(e)
except json.JSONDecodeError as e:
    print(f"Error: JSON decoding error - {e}")
except Exception as e:
    print(f"Error: An unexpected error occurred - {e}")