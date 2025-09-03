import os
import json
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Initialize a dictionary to store the count of messages sent per week
messages_per_week = {}

# Function to convert timestamp to week format
def get_week_from_timestamp(timestamp_ms):
    timestamp = timestamp_ms / 1000  # Convert from milliseconds to seconds
    dt = datetime.utcfromtimestamp(timestamp)
    week = dt.strftime("Week %Y-%W")
    return week

# Function to process messages from JSON files
def process_messages(json_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            messages = data.get("messages", [])
            for message in messages:
                sender_name = message.get("sender_name")
                timestamp_ms = message.get("timestamp_ms")
                if sender_name and timestamp_ms:
                    week = get_week_from_timestamp(timestamp_ms)
                    if week in messages_per_week:
                        messages_per_week[week] += 1
                    else:
                        messages_per_week[week] = 1
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON file.")

# Function to traverse the directory and process message files
def traverse_directory(directory):
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.startswith("message_") and file.endswith(".json"):
                    json_file_path = os.path.join(root, file)
                    process_messages(json_file_path)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Traverse the 'inbox' directory to process message files
inbox_dir = os.path.join(root_dir, "messages", "inbox")
if os.path.exists(inbox_dir):
    traverse_directory(inbox_dir)
else:
    print("Warning: 'inbox' directory not found. Generating an empty CSV file.")

# Write the results to a CSV file
output_file = "query_responses/results.csv"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Week', 'Messages Sent']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for week, count in messages_per_week.items():
        writer.writerow({'Week': week, 'Messages Sent': count})

print(f"CSV file has been saved to {output_file}")