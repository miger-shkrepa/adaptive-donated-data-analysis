import os
import json
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

def get_week(timestamp_ms):
    dt = datetime.fromtimestamp(timestamp_ms / 1000)
    return f"Week {dt.strftime('%Y-%W')}"

def process_messages(messages):
    week_messages = {}
    for message in messages:
        if 'sender_name' in message and 'timestamp_ms' in message:
            week = get_week(message['timestamp_ms'])
            if week not in week_messages:
                week_messages[week] = 0
            week_messages[week] += 1
    return week_messages

def read_message_files(conversation_dir):
    messages = []
    i = 1
    while True:
        file_path = os.path.join(conversation_dir, f"message_{i}.json")
        if not os.path.exists(file_path):
            break
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if 'messages' in data:
                    messages.extend(data['messages'])
        except json.JSONDecodeError:
            raise ValueError(f"Error: JSON decode error in {file_path}.")
        i += 1
    return messages

def process_conversations(inbox_dir):
    week_messages = {}
    for conversation in os.listdir(inbox_dir):
        conversation_dir = os.path.join(inbox_dir, conversation)
        if os.path.isdir(conversation_dir):
            messages = read_message_files(conversation_dir)
            conversation_week_messages = process_messages(messages)
            for week, count in conversation_week_messages.items():
                if week not in week_messages:
                    week_messages[week] = 0
                week_messages[week] += count
    return week_messages

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    inbox_dir = os.path.join(root_dir, "messages", "inbox")
    if not os.path.exists(inbox_dir):
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Week', 'Messages Sent'])
        return
    
    try:
        week_messages = process_conversations(inbox_dir)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Week', 'Messages Sent'])
            for week, count in sorted(week_messages.items()):
                writer.writerow([week, count])
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

if __name__ == "__main__":
    main()