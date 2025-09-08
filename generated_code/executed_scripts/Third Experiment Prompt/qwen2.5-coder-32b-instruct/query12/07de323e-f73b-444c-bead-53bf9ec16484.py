import os
import json
import csv
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

def get_week_number(timestamp_ms):
    """Convert timestamp in milliseconds to 'Week YYYY-WW' format."""
    timestamp_s = timestamp_ms / 1000
    dt = datetime.fromtimestamp(timestamp_s)
    return dt.strftime('Week %Y-%W')

def process_messages(root_dir):
    """Process messages in the 'inbox' directory and count messages sent per week."""
    messages_sent_per_week = {}

    try:
        inbox_dir = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")
        if not os.path.exists(inbox_dir):
            raise FileNotFoundError("FileNotFoundError: The 'inbox' directory does not exist.")
        
        for conversation_dir in os.listdir(inbox_dir):
            conversation_path = os.path.join(inbox_dir, conversation_dir)
            if os.path.isdir(conversation_path):
                for message_file in sorted(os.listdir(conversation_path)):
                    if message_file.startswith("message_") and message_file.endswith(".json"):
                        message_file_path = os.path.join(conversation_path, message_file)
                        try:
                            with open(message_file_path, 'r', encoding='utf-8') as f:
                                messages = json.load(f)
                                for message in messages.get("messages", []):
                                    if "sender_name" in message and "timestamp_ms" in message:
                                        if message["sender_name"] == "Your Username":  # Assuming "Your Username" is the user's name
                                            week = get_week_number(message["timestamp_ms"])
                                            if week in messages_sent_per_week:
                                                messages_sent_per_week[week] += 1
                                            else:
                                                messages_sent_per_week[week] = 1
                        except (FileNotFoundError, ValueError) as e:
                            print(f"Error processing {message_file_path}: {e}")
    
    except FileNotFoundError as e:
        print(e)
    
    return messages_sent_per_week

def save_to_csv(messages_sent_per_week, output_path):
    """Save the messages sent per week to a CSV file."""
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Week", "Messages Sent"])
            for week, count in sorted(messages_sent_per_week.items()):
                writer.writerow([week, count])
    except IOError as e:
        print(f"Error writing to CSV file: {e}")

def main():
    messages_sent_per_week = process_messages(root_dir)
    save_to_csv(messages_sent_per_week, "query_responses/results.csv")

if __name__ == "__main__":
    main()