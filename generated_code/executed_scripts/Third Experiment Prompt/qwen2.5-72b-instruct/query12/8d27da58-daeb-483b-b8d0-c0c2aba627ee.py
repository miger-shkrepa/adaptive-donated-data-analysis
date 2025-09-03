import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Function to parse JSON files and extract message timestamps
def parse_message_files(conversation_dir):
    messages = []
    i = 1
    while True:
        file_path = os.path.join(conversation_dir, f"message_{i}.json")
        if not os.path.exists(file_path):
            break
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for message in data.get("messages", []):
                    timestamp_ms = message.get("timestamp_ms")
                    if timestamp_ms:
                        timestamp = timestamp_ms / 1000  # Convert to seconds
                        messages.append(datetime.fromtimestamp(timestamp))
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Error: Failed to parse JSON file {file_path}. Reason: {str(e)}")
        i += 1
    return messages

# Function to count messages per week
def count_messages_per_week(messages):
    message_counts = {}
    for message in messages:
        week = message.strftime('%Y-%W')
        if week not in message_counts:
            message_counts[week] = 0
        message_counts[week] += 1
    return message_counts

# Main function to process the directory and generate the CSV file
def process_directory(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    all_messages = []
    inbox_dir = os.path.join(root_dir, "inbox")
    if os.path.exists(inbox_dir):
        for conversation_dir in os.listdir(inbox_dir):
            conversation_path = os.path.join(inbox_dir, conversation_dir)
            if os.path.isdir(conversation_path):
                messages = parse_message_files(conversation_path)
                all_messages.extend(messages)
    
    message_counts = count_messages_per_week(all_messages)
    
    # Write the results to a CSV file
    output_path = "query_responses/results.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Week', 'Messages Sent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for week, count in sorted(message_counts.items()):
            writer.writerow({'Week': f"Week {week}", 'Messages Sent': count})

# Execute the main function
try:
    process_directory(root_dir)
except Exception as e:
    print(f"Error: {str(e)}")