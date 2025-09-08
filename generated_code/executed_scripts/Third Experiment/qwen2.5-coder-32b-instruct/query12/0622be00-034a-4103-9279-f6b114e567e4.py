import os
import json
from datetime import datetime, timedelta

root_dir = "root_dir"

def get_week_number(timestamp_ms):
    timestamp_s = timestamp_ms / 1000
    dt = datetime.fromtimestamp(timestamp_s)
    year, week_number, _ = dt.isocalendar()
    return f"Week {year}-{week_number:02}"

def count_messages_per_week(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.isdir(root_dir):
        raise ValueError("ValueError: The root directory is not a valid directory.")
    
    week_message_count = {}

    try:
        for conversation_dir in os.listdir(root_dir):
            conversation_path = os.path.join(root_dir, conversation_dir)
            if os.path.isdir(conversation_path):
                for message_file in sorted(os.listdir(conversation_path)):
                    if message_file.startswith("message_") and message_file.endswith(".json"):
                        message_path = os.path.join(conversation_path, message_file)
                        with open(message_path, 'r', encoding='utf-8') as file:
                            message_data = json.load(file)
                            if 'timestamp_ms' in message_data and 'sender_name' in message_data:
                                week = get_week_number(message_data['timestamp_ms'])
                                if message_data['sender_name'] == 'YourUserName':  # Replace 'YourUserName' with the actual user's name
                                    if week in week_message_count:
                                        week_message_count[week] += 1
                                    else:
                                        week_message_count[week] = 1
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while processing the files: {str(e)}")

    return week_message_count

def write_to_csv(week_message_count, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write("Week,Messages Sent\n")
            for week, count in sorted(week_message_count.items()):
                file.write(f"{week},{count}\n")
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while writing to the CSV file: {str(e)}")

week_message_count = count_messages_per_week(root_dir)
write_to_csv(week_message_count, 'query_responses/results.csv')