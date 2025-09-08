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
        raise FileNotFoundError("Error: The root directory does not exist.")

    messages_dir = os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox')
    if not os.path.exists(messages_dir):
        raise FileNotFoundError("Error: The messages directory does not exist.")

    message_counts = {}

    for subfolder in os.listdir(messages_dir):
        subfolder_path = os.path.join(messages_dir, subfolder)
        if os.path.isdir(subfolder_path):
            message_files = sorted([f for f in os.listdir(subfolder_path) if f.startswith('message_') and f.endswith('.json')])
            for message_file in message_files:
                message_file_path = os.path.join(subfolder_path, message_file)
                try:
                    with open(message_file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
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

def main():
    try:
        message_counts = process_messages(root_dir)
        save_to_csv(message_counts)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()