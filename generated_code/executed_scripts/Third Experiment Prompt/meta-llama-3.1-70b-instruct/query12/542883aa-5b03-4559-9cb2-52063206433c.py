import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_messages_sent_per_week(root_dir):
    messages_sent_per_week = {}
    inbox_dir = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")
    
    if not os.path.exists(inbox_dir):
        raise FileNotFoundError("Error: The inbox directory does not exist.")
    
    for conversation_dir in os.listdir(inbox_dir):
        conversation_dir_path = os.path.join(inbox_dir, conversation_dir)
        
        if not os.path.isdir(conversation_dir_path):
            continue
        
        for message_file in os.listdir(conversation_dir_path):
            if not message_file.startswith("message_") or not message_file.endswith(".json"):
                continue
            
            message_file_path = os.path.join(conversation_dir_path, message_file)
            
            try:
                with open(message_file_path, "r") as file:
                    message_data = json.load(file)
            except json.JSONDecodeError:
                raise ValueError("Error: Failed to parse JSON file.")
            
            for message in message_data["messages"]:
                timestamp_ms = message["timestamp_ms"]
                timestamp = datetime.fromtimestamp(timestamp_ms / 1000)
                week = timestamp.strftime("%Y-%W")
                
                if week not in messages_sent_per_week:
                    messages_sent_per_week[week] = 0
                
                messages_sent_per_week[week] += 1
    
    return messages_sent_per_week

def save_to_csv(messages_sent_per_week):
    csv_file_path = "query_responses/results.csv"
    
    with open(csv_file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Week", "Messages Sent"])
        
        for week, messages_sent in messages_sent_per_week.items():
            writer.writerow([week, messages_sent])

try:
    messages_sent_per_week = get_messages_sent_per_week(root_dir)
    save_to_csv(messages_sent_per_week)
except FileNotFoundError as e:
    print(e)
    with open("query_responses/results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Week", "Messages Sent"])
except ValueError as e:
    print(e)
    with open("query_responses/results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Week", "Messages Sent"])