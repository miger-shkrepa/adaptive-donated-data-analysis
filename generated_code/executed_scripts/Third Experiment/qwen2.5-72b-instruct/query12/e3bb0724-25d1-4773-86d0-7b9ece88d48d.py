import os
import json
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

def get_week(timestamp_ms):
    dt = datetime.fromtimestamp(timestamp_ms / 1000)
    return f"Week {dt.strftime('%Y-%W')}"

def count_messages_per_week(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        message_counts = {}
        
        inbox_path = os.path.join(root_dir, "messages", "inbox")
        if not os.path.exists(inbox_path):
            return message_counts
        
        for conversation_dir in os.listdir(inbox_path):
            conversation_path = os.path.join(inbox_path, conversation_dir)
            if not os.path.isdir(conversation_path):
                continue
            
            message_files = sorted([f for f in os.listdir(conversation_path) if f.startswith("message_") and f.endswith(".json")])
            
            for message_file in message_files:
                message_path = os.path.join(conversation_path, message_file)
                with open(message_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    messages = data.get("messages", [])
                    for message in messages:
                        sender_name = message.get("sender_name")
                        timestamp_ms = message.get("timestamp_ms")
                        if sender_name and timestamp_ms:
                            week = get_week(timestamp_ms)
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
            for week, count in message_counts.items():
                writer.writerow({'Week': week, 'Messages Sent': count})
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

if __name__ == "__main__":
    try:
        message_counts = count_messages_per_week(root_dir)
        save_to_csv(message_counts)
    except Exception as e:
        print(str(e))