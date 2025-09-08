import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def get_weekly_messages(conversation_dir):
    weekly_messages = {}
    for file_name in sorted(os.listdir(conversation_dir)):
        if file_name.startswith("message_") and file_name.endswith(".json"):
            file_path = os.path.join(conversation_dir, file_name)
            data = load_json(file_path)
            for message in data.get("messages", []):
                timestamp_ms = message.get("timestamp_ms")
                if timestamp_ms:
                    timestamp = timestamp_ms / 1000
                    dt = datetime.fromtimestamp(timestamp)
                    week = dt.strftime('%Y-%W')
                    if week not in weekly_messages:
                        weekly_messages[week] = 0
                    weekly_messages[week] += 1
    return weekly_messages

def process_inbox(inbox_dir):
    weekly_messages = {}
    for conversation_dir in os.listdir(inbox_dir):
        conversation_path = os.path.join(inbox_dir, conversation_dir)
        if os.path.isdir(conversation_path):
            conversation_weekly_messages = get_weekly_messages(conversation_path)
            for week, count in conversation_weekly_messages.items():
                if week not in weekly_messages:
                    weekly_messages[week] = 0
                weekly_messages[week] += count
    return weekly_messages

def write_csv(weekly_messages):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Week', 'Messages Sent'])
        for week, count in sorted(weekly_messages.items()):
            writer.writerow([f"Week {week}", count])

def main():
    try:
        inbox_dir = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")
        if not os.path.exists(inbox_dir):
            raise FileNotFoundError(f"FileNotFoundError: The inbox directory {inbox_dir} does not exist.")
        
        weekly_messages = process_inbox(inbox_dir)
        write_csv(weekly_messages)
    except Exception as e:
        print(e)
        # If any error occurs, create an empty CSV with headers only
        file_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Week', 'Messages Sent'])

if __name__ == "__main__":
    main()