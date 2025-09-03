import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def process_message_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            messages = data.get('messages', [])
            return [(datetime.fromtimestamp(msg['timestamp_ms'] / 1000).strftime('%Y-%W'), 1) for msg in messages if msg.get('sender_name') == 'user']
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        raise ValueError(f"Error: Failed to process {file_path}. Reason: {str(e)}")

def aggregate_messages_per_week(messages):
    weekly_counts = {}
    for week, count in messages:
        weekly_counts[week] = weekly_counts.get(week, 0) + count
    return weekly_counts

def write_to_csv(data, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Week', 'Messages Sent'])
        for week, count in sorted(data.items()):
            writer.writerow([f"Week {week}", count])

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    inbox_dir = os.path.join(root_dir, 'inbox')
    if not os.path.exists(inbox_dir):
        write_to_csv({}, 'query_responses/results.csv')
        return

    all_messages = []
    for conversation_dir in os.listdir(inbox_dir):
        conversation_path = os.path.join(inbox_dir, conversation_dir)
        if os.path.isdir(conversation_path):
            message_files = sorted([f for f in os.listdir(conversation_path) if f.startswith('message_') and f.endswith('.json')])
            for message_file in message_files:
                file_path = os.path.join(conversation_path, message_file)
                try:
                    all_messages.extend(process_message_file(file_path))
                except ValueError as e:
                    print(e)

    weekly_counts = aggregate_messages_per_week(all_messages)
    write_to_csv(weekly_counts, 'query_responses/results.csv')

if __name__ == "__main__":
    main()