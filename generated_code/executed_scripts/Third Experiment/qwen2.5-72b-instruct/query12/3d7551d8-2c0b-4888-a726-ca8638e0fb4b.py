import os
import json
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("Error: FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the count of messages per week
messages_per_week = {}

# Function to convert timestamp to week format
def get_week_from_timestamp(timestamp_ms):
    timestamp = timestamp_ms / 1000  # Convert from milliseconds to seconds
    dt = datetime.utcfromtimestamp(timestamp)
    week = dt.strftime('Week %Y-%W')
    return week

# Function to process messages in a conversation
def process_conversation(conversation_dir):
    message_files = sorted([f for f in os.listdir(conversation_dir) if f.startswith("message_") and f.endswith(".json")])
    for message_file in message_files:
        file_path = os.path.join(conversation_dir, message_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for message in data.get("messages", []):
                    sender_name = message.get("sender_name")
                    timestamp_ms = message.get("timestamp_ms")
                    if sender_name and timestamp_ms:
                        week = get_week_from_timestamp(timestamp_ms)
                        if week in messages_per_week:
                            messages_per_week[week] += 1
                        else:
                            messages_per_week[week] = 1
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: FileNotFoundError: Message file {message_file} not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error: ValueError: Invalid JSON format in file {message_file}.")

# Traverse the directory structure to find and process conversations
inbox_dir = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")
if os.path.exists(inbox_dir):
    for conversation_dir in os.listdir(inbox_dir):
        conversation_path = os.path.join(inbox_dir, conversation_dir)
        if os.path.isdir(conversation_path):
            process_conversation(conversation_path)
else:
    print("Warning: The 'inbox' directory does not exist. Creating an empty CSV file.")

# Write the results to a CSV file
output_file = 'query_responses/results.csv'
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Week', 'Messages Sent']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for week, count in messages_per_week.items():
        writer.writerow({'Week': week, 'Messages Sent': count})

print(f"CSV file has been saved to {output_file}")