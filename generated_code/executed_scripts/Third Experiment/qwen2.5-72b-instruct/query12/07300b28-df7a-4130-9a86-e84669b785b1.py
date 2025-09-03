import os
import json
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("Error: The root directory does not exist.")

# Initialize a dictionary to store the count of messages per week
messages_per_week = {}

# Function to convert timestamp to week format
def get_week(timestamp_ms):
    timestamp = timestamp_ms / 1000  # Convert from milliseconds to seconds
    dt = datetime.utcfromtimestamp(timestamp)
    return f"Week {dt.strftime('%Y-%W')}"

# Function to process a single message file
def process_message_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
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
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

# Traverse the directory structure
inbox_path = os.path.join(root_dir, "messages", "inbox")
if not os.path.exists(inbox_path):
    # If the necessary directory does not exist, create a CSV with only headers
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Week', 'Messages Sent'])
    exit()

for conversation_dir in os.listdir(inbox_path):
    conversation_path = os.path.join(inbox_path, conversation_dir)
    if os.path.isdir(conversation_path):
        message_files = sorted([f for f in os.listdir(conversation_path) if f.startswith("message_") and f.endswith(".json")])
        for message_file in message_files:
            message_file_path = os.path.join(conversation_path, message_file)
            process_message_file(message_file_path)

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Week', 'Messages Sent'])
    for week, count in sorted(messages_per_week.items()):
        writer.writerow([week, count])