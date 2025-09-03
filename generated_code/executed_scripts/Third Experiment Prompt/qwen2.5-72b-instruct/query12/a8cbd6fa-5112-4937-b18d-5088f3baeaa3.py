import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def process_messages(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        message_counts = {}
        inbox_path = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")

        if not os.path.exists(inbox_path):
            return message_counts

        for conversation_dir in os.listdir(inbox_path):
            conversation_path = os.path.join(inbox_path, conversation_dir)
            if not os.path.isdir(conversation_path):
                continue

            message_files = sorted([f for f in os.listdir(conversation_path) if f.startswith("message_") and f.endswith(".json")])

            for message_file in message_files:
                message_file_path = os.path.join(conversation_path, message_file)
                with open(message_file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    messages = data.get("messages", [])
                    for message in messages:
                        timestamp_ms = message.get("timestamp_ms")
                        if timestamp_ms is None:
                            continue
                        timestamp = timestamp_ms / 1000
                        dt = datetime.fromtimestamp(timestamp)
                        week = dt.strftime('%Y-%W')
                        if message["sender_name"] == "username_placeholder":
                            message_counts[week] = message_counts.get(week, 0) + 1

        return message_counts

    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def save_to_csv(message_counts):
    output_path = "query_responses/results.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Week', 'Messages Sent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for week, count in sorted(message_counts.items()):
            writer.writerow({'Week': f"Week {week}", 'Messages Sent': count})

def main():
    try:
        message_counts = process_messages(root_dir)
        save_to_csv(message_counts)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()