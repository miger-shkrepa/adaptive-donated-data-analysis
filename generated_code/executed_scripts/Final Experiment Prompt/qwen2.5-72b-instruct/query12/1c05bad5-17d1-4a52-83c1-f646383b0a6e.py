import os
import json
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

def get_weekly_messages(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        message_counts = {}
        inbox_path = os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox')

        if not os.path.exists(inbox_path):
            return message_counts

        for conversation_dir in os.listdir(inbox_path):
            conversation_path = os.path.join(inbox_path, conversation_dir)
            if os.path.isdir(conversation_path):
                for file_name in os.listdir(conversation_path):
                    if file_name.startswith('message_') and file_name.endswith('.json'):
                        file_path = os.path.join(conversation_path, file_name)
                        with open(file_path, 'r', encoding='utf-8') as file:
                            data = json.load(file)
                            for message in data.get('messages', []):
                                timestamp_ms = message.get('timestamp_ms')
                                if timestamp_ms:
                                    timestamp = datetime.fromtimestamp(timestamp_ms / 1000)
                                    week = timestamp.strftime('%Y-%W')
                                    if week not in message_counts:
                                        message_counts[week] = 0
                                    message_counts[week] += 1

        return message_counts

    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def save_to_csv(message_counts):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Week', 'Messages Sent']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for week, count in sorted(message_counts.items(), key=lambda x: datetime.strptime(x[0] + '-1', '%Y-%W-%w')):
                writer.writerow({'Week': f"Week {week}", 'Messages Sent': count})
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

if __name__ == "__main__":
    try:
        weekly_messages = get_weekly_messages(root_dir)
        save_to_csv(weekly_messages)
    except Exception as e:
        print(str(e))