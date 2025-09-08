import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_weekly_messages(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        weekly_messages = {}
        messages_dir = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")

        if not os.path.exists(messages_dir):
            return weekly_messages

        for conversation_dir in os.listdir(messages_dir):
            conversation_path = os.path.join(messages_dir, conversation_dir)
            if not os.path.isdir(conversation_path):
                continue

            message_files = sorted([f for f in os.listdir(conversation_path) if f.startswith("message_") and f.endswith(".json")])

            for message_file in message_files:
                message_path = os.path.join(conversation_path, message_file)
                try:
                    with open(message_path, 'r') as f:
                        data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    raise ValueError(f"Error: Failed to read JSON file {message_path}. Reason: {str(e)}")

                for message in data.get("messages", []):
                    timestamp_ms = message.get("timestamp_ms")
                    if not timestamp_ms:
                        continue

                    timestamp = timestamp_ms / 1000
                    dt = datetime.fromtimestamp(timestamp)
                    week = dt.strftime('%Y-%W')
                    if week not in weekly_messages:
                        weekly_messages[week] = 0
                    weekly_messages[week] += 1

        return weekly_messages

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def save_to_csv(weekly_messages):
    try:
        os.makedirs("query_responses", exist_ok=True)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Week', 'Messages Sent']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for week, messages_sent in weekly_messages.items():
                writer.writerow({'Week': f"Week {week}", 'Messages Sent': messages_sent})

    except Exception as e:
        raise Exception(f"Error: Failed to save CSV file. Reason: {str(e)}")

if __name__ == "__main__":
    try:
        weekly_messages = get_weekly_messages(root_dir)
        save_to_csv(weekly_messages)
    except Exception as e:
        print(str(e))
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Week', 'Messages Sent']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()