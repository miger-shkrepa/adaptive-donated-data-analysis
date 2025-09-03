import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def process_messages(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            messages = data.get('messages', [])
            return [
                datetime.fromtimestamp(msg['timestamp_ms'] / 1000).strftime('%Y-%W')
                for msg in messages
                if msg.get('sender_name') == 'user'
            ]
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified message file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON from the message file.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while processing the message file: {str(e)}")

def aggregate_weekly_messages(root_dir):
    weekly_messages = {}
    inbox_path = os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox')

    if not os.path.exists(inbox_path):
        return weekly_messages

    for conversation_dir in os.listdir(inbox_path):
        conversation_path = os.path.join(inbox_path, conversation_dir)
        if not os.path.isdir(conversation_path):
            continue

        message_files = sorted([
            f for f in os.listdir(conversation_path)
            if f.startswith('message_') and f.endswith('.json')
        ])

        for message_file in message_files:
            file_path = os.path.join(conversation_path, message_file)
            weeks = process_messages(file_path)
            for week in weeks:
                weekly_messages[week] = weekly_messages.get(week, 0) + 1

    return weekly_messages

def write_to_csv(weekly_messages, output_path):
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Week', 'Messages Sent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for week, count in sorted(weekly_messages.items()):
            writer.writerow({'Week': f"Week {week}", 'Messages Sent': count})

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        weekly_messages = aggregate_weekly_messages(root_dir)
        output_path = 'query_responses/results.csv'
        write_to_csv(weekly_messages, output_path)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()