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
            return [
                datetime.fromtimestamp(msg['timestamp_ms'] / 1000).strftime('%Y-%W')
                for msg in messages
                if msg.get('sender_name') == 'user'
            ]
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON in file {file_path}.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while processing {file_path}: {e}")

def count_messages_per_week(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        week_counts = {}
        inbox_path = os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox')
        if not os.path.exists(inbox_path):
            return week_counts

        for conversation_dir in os.listdir(inbox_path):
            conversation_path = os.path.join(inbox_path, conversation_dir)
            if not os.path.isdir(conversation_path):
                continue

            for file_name in os.listdir(conversation_path):
                if file_name.startswith('message_') and file_name.endswith('.json'):
                    file_path = os.path.join(conversation_path, file_name)
                    weeks = process_message_file(file_path)
                    for week in weeks:
                        week_counts[week] = week_counts.get(week, 0) + 1

        return week_counts

    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred: {e}")

def save_to_csv(week_counts):
    try:
        os.makedirs('query_responses', exist_ok=True)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Week', 'Messages Sent']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for week, count in sorted(week_counts.items()):
                writer.writerow({'Week': f"Week {week}", 'Messages Sent': count})
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while saving the CSV: {e}")

def main():
    try:
        week_counts = count_messages_per_week(root_dir)
        save_to_csv(week_counts)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()