import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def process_messages(messages):
    weekly_counts = {}
    for message in messages:
        timestamp_ms = message.get('timestamp_ms')
        if timestamp_ms is None:
            continue
        timestamp = timestamp_ms / 1000
        dt = datetime.fromtimestamp(timestamp)
        week = dt.strftime('%Y-%W')
        weekly_counts[week] = weekly_counts.get(week, 0) + 1
    return weekly_counts

def get_messages_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            messages = data.get('messages', [])
            return messages
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def get_all_messages(root_dir):
    all_messages = []
    inbox_path = os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox')
    if not os.path.exists(inbox_path):
        return all_messages

    for conversation_dir in os.listdir(inbox_path):
        conversation_path = os.path.join(inbox_path, conversation_dir)
        if not os.path.isdir(conversation_path):
            continue

        message_files = sorted([f for f in os.listdir(conversation_path) if f.startswith('message_') and f.endswith('.json')])
        for message_file in message_files:
            file_path = os.path.join(conversation_path, message_file)
            messages = get_messages_from_file(file_path)
            all_messages.extend(messages)

    return all_messages

def write_to_csv(weekly_counts):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Week', 'Messages Sent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for week, count in weekly_counts.items():
            writer.writerow({'Week': f"Week {week}", 'Messages Sent': count})

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    try:
        all_messages = get_all_messages(root_dir)
        weekly_counts = process_messages(all_messages)
        write_to_csv(weekly_counts)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()