import os
import csv
import json
from datetime import datetime

root_dir = "root_dir"

def get_week_number(timestamp_ms):
    timestamp_s = timestamp_ms / 1000
    dt = datetime.fromtimestamp(timestamp_s)
    return dt.strftime('Week %Y-%W')

def count_messages_per_week(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.isdir(root_dir):
        raise ValueError("ValueError: The root directory is not a valid directory.")
    
    week_message_count = {}

    try:
        inbox_path = os.path.join(root_dir, 'inbox')
        if not os.path.exists(inbox_path):
            return week_message_count
        
        for conversation_folder in os.listdir(inbox_path):
            conversation_path = os.path.join(inbox_path, conversation_folder)
            if os.path.isdir(conversation_path):
                for message_file in sorted(os.listdir(conversation_path)):
                    if message_file.startswith('message_') and message_file.endswith('.json'):
                        message_path = os.path.join(conversation_path, message_file)
                        with open(message_path, 'r', encoding='utf-8') as file:
                            message_data = json.load(file)
                            if 'sender_name' in message_data and 'timestamp_ms' in message_data:
                                week = get_week_number(message_data['timestamp_ms'])
                                if week not in week_message_count:
                                    week_message_count[week] = 0
                                week_message_count[week] += 1
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while processing the files: {str(e)}")
    
    return week_message_count

def save_to_csv(week_message_count, output_path):
    if not week_message_count:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Week', 'Messages Sent'])
        return
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Week', 'Messages Sent'])
        for week, count in sorted(week_message_count.items()):
            writer.writerow([week, count])

try:
    week_message_count = count_messages_per_week(root_dir)
    save_to_csv(week_message_count, 'query_responses/results.csv')
except Exception as e:
    print(e)