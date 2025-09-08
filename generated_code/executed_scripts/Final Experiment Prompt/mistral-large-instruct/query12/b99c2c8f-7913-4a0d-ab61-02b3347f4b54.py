import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_week_from_timestamp(timestamp_ms):
    dt = datetime.fromtimestamp(timestamp_ms / 1000.0)
    return dt.strftime('%Y-%W')

def process_messages(root_dir):
    messages_per_week = {}

    inbox_dir = os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox')

    if not os.path.exists(inbox_dir):
        raise FileNotFoundError("FileNotFoundError: The inbox directory does not exist.")

    for conversation_folder in os.listdir(inbox_dir):
        conversation_path = os.path.join(inbox_dir, conversation_folder)
        if os.path.isdir(conversation_path):
            message_files = sorted([f for f in os.listdir(conversation_path) if f.startswith('message_') and f.endswith('.json')])
            for message_file in message_files:
                message_file_path = os.path.join(conversation_path, message_file)
                try:
                    with open(message_file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        for message in data.get('messages', []):
                            if message.get('sender_name') == 'user':
                                week = get_week_from_timestamp(message.get('timestamp_ms', 0))
                                if week in messages_per_week:
                                    messages_per_week[week] += 1
                                else:
                                    messages_per_week[week] = 1
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"Error processing {message_file_path}: {e}")
                except FileNotFoundError:
                    print(f"FileNotFoundError: {message_file_path} does not exist.")

    return messages_per_week

def save_to_csv(messages_per_week):
    output_dir = 'query_responses'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'results.csv')

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Week', 'Messages Sent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for week, count in messages_per_week.items():
            writer.writerow({'Week': f'Week {week}', 'Messages Sent': count})

if __name__ == "__main__":
    try:
        messages_per_week = process_messages(root_dir)
        save_to_csv(messages_per_week)
    except Exception as e:
        print(f"Error: {e}")