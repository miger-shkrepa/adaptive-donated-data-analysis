import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_week_from_timestamp(timestamp_ms):
    dt = datetime.fromtimestamp(timestamp_ms / 1000.0)
    return dt.strftime('Week %Y-%W')

def process_messages(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    messages_dir = os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox')
    if not os.path.exists(messages_dir):
        raise FileNotFoundError("FileNotFoundError: The messages directory does not exist.")

    message_counts = {}

    for subdir in os.listdir(messages_dir):
        subdir_path = os.path.join(messages_dir, subdir)
        if os.path.isdir(subdir_path):
            message_files = sorted([f for f in os.listdir(subdir_path) if f.startswith('message_') and f.endswith('.json')])
            for message_file in message_files:
                message_file_path = os.path.join(subdir_path, message_file)
                try:
                    with open(message_file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'messages' in data:
                            for message in data['messages']:
                                if message.get('sender_name') == 'user':
                                    week = get_week_from_timestamp(message['timestamp_ms'])
                                    if week in message_counts:
                                        message_counts[week] += 1
                                    else:
                                        message_counts[week] = 1
                except (json.JSONDecodeError, KeyError, ValueError) as e:
                    print(f"Error processing {message_file_path}: {e}")

    return message_counts

def save_to_csv(message_counts):
    output_dir = 'query_responses'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'results.csv')

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Week', 'Messages Sent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for week, count in message_counts.items():
            writer.writerow({'Week': week, 'Messages Sent': count})

if __name__ == "__main__":
    try:
        message_counts = process_messages(root_dir)
        save_to_csv(message_counts)
    except Exception as e:
        print(f"Error: {e}")