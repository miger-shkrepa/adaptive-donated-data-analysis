import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_week_number(timestamp_ms):
    timestamp_s = timestamp_ms / 1000
    dt = datetime.fromtimestamp(timestamp_s)
    return dt.strftime("Week %Y-%W")

def count_messages_per_week(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        messages_per_week = {}
        
        inbox_dir = os.path.join(root_dir, "messages", "inbox")
        if not os.path.exists(inbox_dir):
            return messages_per_week
        
        for conversation_dir in os.listdir(inbox_dir):
            conversation_path = os.path.join(inbox_dir, conversation_dir)
            if os.path.isdir(conversation_path):
                for message_file in sorted(os.listdir(conversation_path)):
                    if message_file.startswith("message_") and message_file.endswith(".json"):
                        message_path = os.path.join(conversation_path, message_file)
                        with open(message_path, 'r', encoding='utf-8') as file:
                            import json
                            data = json.load(file)
                            for message in data.get("messages", []):
                                if "sender_name" in message and "timestamp_ms" in message:
                                    week = get_week_number(message["timestamp_ms"])
                                    if message["sender_name"] == "YourUserName":  # Replace 'YourUserName' with the actual user's name
                                        if week in messages_per_week:
                                            messages_per_week[week] += 1
                                        else:
                                            messages_per_week[week] = 1
        return messages_per_week
    
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while processing the files: {str(e)}")

def save_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Week", "Messages Sent"])
            for week, count in sorted(data.items()):
                writer.writerow([week, count])
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while writing to the CSV file: {str(e)}")

messages_per_week = count_messages_per_week(root_dir)
save_to_csv(messages_per_week, "query_responses/results.csv")