import os
import json
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to count messages per week
messages_per_week = {}

# Function to convert timestamp to week format
def get_week(timestamp_ms):
    timestamp = datetime.fromtimestamp(timestamp_ms / 1000)
    return f"Week {timestamp.strftime('%Y-%W')}"

# Function to process JSON files and count messages
def process_message_files(directory):
    for entry in os.scandir(directory):
        if entry.is_dir():
            process_message_files(entry.path)
        elif entry.name.startswith("message_") and entry.name.endswith(".json"):
            with open(entry.path, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    for message in data.get("messages", []):
                        sender_name = message.get("sender_name")
                        timestamp_ms = message.get("timestamp_ms")
                        if sender_name and timestamp_ms:
                            week = get_week(timestamp_ms)
                            if week not in messages_per_week:
                                messages_per_week[week] = 0
                            messages_per_week[week] += 1
                except json.JSONDecodeError:
                    raise ValueError("Error: Failed to decode JSON file.")

# Traverse the directory structure starting from the inbox
inbox_path = os.path.join(root_dir, "inbox")
if os.path.exists(inbox_path):
    for conversation_dir in os.scandir(inbox_path):
        if conversation_dir.is_dir():
            process_message_files(conversation_dir.path)
else:
    print("Warning: No 'inbox' directory found. The output CSV will only contain headers.")

# Write the results to a CSV file
output_path = "query_responses/results.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Week', 'Messages Sent']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for week, count in sorted(messages_per_week.items()):
        writer.writerow({'Week': week, 'Messages Sent': count})

print(f"CSV file has been saved to {output_path}")