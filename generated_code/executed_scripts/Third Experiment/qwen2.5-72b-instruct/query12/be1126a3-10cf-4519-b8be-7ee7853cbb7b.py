import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Initialize a dictionary to store the count of messages per week
    messages_per_week = {}

    # Check if the 'inbox' directory exists
    inbox_dir = os.path.join(root_dir, 'inbox')
    if not os.path.exists(inbox_dir):
        # If 'inbox' directory does not exist, create a CSV with only headers
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Week', 'Messages Sent'])
        print("CSV file created with only headers as 'inbox' directory does not exist.")
        exit()

    # Iterate through each conversation subfolder in the 'inbox' directory
    for conversation_folder in os.listdir(inbox_dir):
        conversation_path = os.path.join(inbox_dir, conversation_folder)
        if os.path.isdir(conversation_path):
            message_files = []
            for file in os.listdir(conversation_path):
                if file.startswith("message_") and file.endswith(".json"):
                    try:
                        message_files.append(int(file.split('_')[1].split('.')[0]))
                    except ValueError:
                        raise ValueError("Error: Invalid message file naming format.")
            message_files.sort()

            for i, message_num in enumerate(message_files):
                message_file_path = os.path.join(conversation_path, f"message_{message_num}.json")
                with open(message_file_path, 'r') as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        raise ValueError("Error: Invalid JSON format in message file.")

                    # Assuming the JSON structure contains a 'messages' list with 'timestamp' and 'sender_name' fields
                    if 'messages' in data:
                        for message in data['messages']:
                            if 'timestamp' in message and 'sender_name' in message:
                                timestamp = message['timestamp']
                                sender_name = message['sender_name']
                                if sender_name == "user":  # Assuming "user" is the user's name
                                    week = datetime.fromtimestamp(timestamp).strftime('Week %Y-%W')
                                    if week in messages_per_week:
                                        messages_per_week[week] += 1
                                    else:
                                        messages_per_week[week] = 1

    # Write the results to a CSV file
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Week', 'Messages Sent'])
        for week, count in messages_per_week.items():
            writer.writerow([week, count])

except FileNotFoundError as e:
    print(e)
except ValueError as e:
    print(e)
except Exception as e:
    print(f"Error: An unexpected error occurred: {e}")