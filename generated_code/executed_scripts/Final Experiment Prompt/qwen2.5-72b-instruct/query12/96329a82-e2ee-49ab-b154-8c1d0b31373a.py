import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def load_messages_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get('messages', [])
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")

def get_weekly_message_counts(messages):
    weekly_counts = {}
    for message in messages:
        timestamp_ms = message.get('timestamp_ms')
        if timestamp_ms is None:
            continue
        timestamp = datetime.fromtimestamp(timestamp_ms / 1000)
        week = timestamp.strftime('%Y-%W')
        weekly_counts[week] = weekly_counts.get(week, 0) + 1
    return weekly_counts

def write_to_csv(weekly_counts):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Week', 'Messages Sent'])
        for week, count in sorted(weekly_counts.items()):
            writer.writerow([f"Week {week}", count])

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        inbox_dir = os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox')
        if not os.path.exists(inbox_dir):
            write_to_csv({})
            return

        all_messages = []
        for conversation_dir in os.listdir(inbox_dir):
            conversation_path = os.path.join(inbox_dir, conversation_dir)
            if os.path.isdir(conversation_path):
                for file_name in os.listdir(conversation_path):
                    if file_name.startswith('message_') and file_name.endswith('.json'):
                        file_path = os.path.join(conversation_path, file_name)
                        messages = load_messages_from_json(file_path)
                        all_messages.extend(messages)

        weekly_counts = get_weekly_message_counts(all_messages)
        write_to_csv(weekly_counts)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()