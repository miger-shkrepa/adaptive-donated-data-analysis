import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_week_from_timestamp(timestamp_ms):
    dt = datetime.fromtimestamp(timestamp_ms / 1000.0)
    return dt.strftime('Week %Y-%W')

def process_messages(directory):
    messages_per_week = {}

    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        if os.path.isdir(subdir_path):
            message_files = sorted([f for f in os.listdir(subdir_path) if f.startswith('message_') and f.endswith('.json')])
            for message_file in message_files:
                message_file_path = os.path.join(subdir_path, message_file)
                try:
                    with open(message_file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        for message in data.get('messages', []):
                            if message.get('sender_name') == 'user':
                                week = get_week_from_timestamp(message['timestamp_ms'])
                                if week in messages_per_week:
                                    messages_per_week[week] += 1
                                else:
                                    messages_per_week[week] = 1
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error processing {message_file_path}: {e}")

    return messages_per_week

def save_to_csv(data, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Week', 'Messages Sent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for week, count in data.items():
            writer.writerow({'Week': week, 'Messages Sent': count})

def main():
    messages_directory = os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox')
    if not os.path.exists(messages_directory):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    messages_per_week = process_messages(messages_directory)

    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    save_to_csv(messages_per_week, output_path)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")