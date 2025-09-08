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

def process_conversation(conversation_dir):
    weekly_counts = {}
    for filename in sorted(os.listdir(conversation_dir)):
        if filename.startswith("message_") and filename.endswith(".json"):
            file_path = os.path.join(conversation_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    messages = data.get('messages', [])
                    weekly_counts_conversation = process_messages(messages)
                    for week, count in weekly_counts_conversation.items():
                        weekly_counts[week] = weekly_counts.get(week, 0) + count
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error processing {file_path}: {e}")
    return weekly_counts

def process_inbox(inbox_dir):
    weekly_counts = {}
    if not os.path.exists(inbox_dir):
        return weekly_counts
    for conversation_dir in os.listdir(inbox_dir):
        conversation_path = os.path.join(inbox_dir, conversation_dir)
        if os.path.isdir(conversation_path):
            weekly_counts_conversation = process_conversation(conversation_path)
            for week, count in weekly_counts_conversation.items():
                weekly_counts[week] = weekly_counts.get(week, 0) + count
    return weekly_counts

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    inbox_dir = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")
    weekly_counts = process_inbox(inbox_dir)

    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Week', 'Messages Sent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for week, count in sorted(weekly_counts.items()):
            writer.writerow({'Week': f"Week {week}", 'Messages Sent': count})

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")