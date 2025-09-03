import os
import json
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

def get_message_files(directory):
    message_files = []
    for filename in sorted(os.listdir(directory)):
        if filename.startswith("message_") and filename.endswith(".json"):
            message_files.append(os.path.join(directory, filename))
    return message_files

def parse_timestamp(timestamp_ms):
    return datetime.fromtimestamp(timestamp_ms / 1000.0)

def count_messages_per_week(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        inbox_dir = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")
        if not os.path.exists(inbox_dir):
            raise FileNotFoundError("FileNotFoundError: The inbox directory does not exist.")
        
        weekly_messages = {}
        
        for conversation_dir in os.listdir(inbox_dir):
            conversation_path = os.path.join(inbox_dir, conversation_dir)
            if os.path.isdir(conversation_path):
                message_files = get_message_files(conversation_path)
                for message_file in message_files:
                    try:
                        with open(message_file, 'r', encoding='utf-8') as file:
                            data = json.load(file)
                            for message in data.get("messages", []):
                                if message.get("sender_name") == "Your Name":  # Replace "Your Name" with the actual user's name
                                    timestamp = parse_timestamp(message["timestamp_ms"])
                                    week = timestamp.strftime('%Y-%W')
                                    if week in weekly_messages:
                                        weekly_messages[week] += 1
                                    else:
                                        weekly_messages[week] = 1
                    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
                        print(f"Error processing file {message_file}: {e}")
        
        # Prepare the CSV content
        csv_content = "Week,Messages Sent\n"
        for week, count in sorted(weekly_messages.items()):
            csv_content += f"Week {week},{count}\n"
        
        # Write the CSV file
        results_dir = os.path.dirname("query_responses/results.csv")
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        with open("query_responses/results.csv", 'w', encoding='utf-8') as csv_file:
            csv_file.write(csv_content)
    
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        # Write only the column headers if there's a FileNotFoundError
        with open("query_responses/results.csv", 'w', encoding='utf-8') as csv_file:
            csv_file.write("Week,Messages Sent\n")

# Execute the function
count_messages_per_week(root_dir)