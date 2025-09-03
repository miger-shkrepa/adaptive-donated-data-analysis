import os
import csv
from datetime import datetime

root_dir = "root_dir"

def count_messages_per_week(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        messages_per_week = {}

        # Navigate to the messages directory
        messages_dir = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")
        if not os.path.exists(messages_dir):
            raise FileNotFoundError("FileNotFoundError: The messages directory does not exist.")

        # Iterate over each conversation folder
        for conversation_folder in os.listdir(messages_dir):
            conversation_path = os.path.join(messages_dir, conversation_folder)
            if os.path.isdir(conversation_path):
                # Iterate over each message file in the conversation folder
                for message_file in sorted(os.listdir(conversation_path)):
                    if message_file.startswith("message_") and message_file.endswith(".json"):
                        message_file_path = os.path.join(conversation_path, message_file)
                        if not os.path.exists(message_file_path):
                            raise FileNotFoundError(f"FileNotFoundError: The message file {message_file} does not exist.")
                        
                        with open(message_file_path, 'r', encoding='utf-8') as file:
                            import json
                            data = json.load(file)
                            
                            for message in data.get('messages', []):
                                if message.get('sender_name') == 'Your Name':  # Assuming 'Your Name' is the user's name
                                    timestamp_ms = message.get('timestamp_ms')
                                    if timestamp_ms:
                                        timestamp = datetime.fromtimestamp(timestamp_ms / 1000)
                                        week = timestamp.strftime('Week %Y-%W')
                                        if week in messages_per_week:
                                            messages_per_week[week] += 1
                                        else:
                                            messages_per_week[week] = 1

        # Write the results to a CSV file
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Week', 'Messages Sent'])
            for week, count in sorted(messages_per_week.items()):
                writer.writerow([week, count])

    except Exception as e:
        # Create an empty CSV file with headers if an error occurs
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Week', 'Messages Sent'])
        print(f"Error: {e}")

# Call the function
count_messages_per_week(root_dir)