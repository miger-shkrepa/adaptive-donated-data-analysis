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
    return dt.strftime('%Y-%W')

def process_messages(root_dir):
    """Process messages in the inbox directory and count messages sent per week."""
    messages_sent_per_week = {}

    try:
        inbox_dir = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")
        if not os.path.exists(inbox_dir):
            raise FileNotFoundError("FileNotFoundError: The inbox directory does not exist.")
        
        for conversation_dir in os.listdir(inbox_dir):
            conversation_path = os.path.join(inbox_dir, conversation_dir)
            if os.path.isdir(conversation_path):
                message_files = sorted([f for f in os.listdir(conversation_path) if f.startswith("message_") and f.endswith(".json")])
                for message_file in message_files:
                    message_file_path = os.path.join(conversation_path, message_file)
                    if not os.path.exists(message_file_path):
                        raise FileNotFoundError(f"FileNotFoundError: The message file {message_file_path} does not exist.")
                    
                    with open(message_file_path, 'r', encoding='utf-8') as file:
                        try:
                            data = json.load(file)
                        except json.JSONDecodeError as e:
                            raise ValueError(f"ValueError: The file {message_file_path} is not a valid JSON file.") from e
                        
                        for message in data.get("messages", []):
                            if message.get("sender_name") == "YourUsername":  # Replace "YourUsername" with the actual username
                                timestamp_ms = message.get("timestamp_ms")
                                if timestamp_ms:
                                    week_number = get_week_number(timestamp_ms)
                                    if week_number in messages_sent_per_week:
                                        messages_sent_per_week[week_number] += 1
                                    else:
                                        messages_sent_per_week[week_number] = 1

    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
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
        raise IOError(f"IOError: Failed to write to the CSV file {output_path}.") from e

def main():
    messages_sent_per_week = process_messages(root_dir)
    output_path = "query_responses/results.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    save_to_csv(messages_sent_per_week, output_path)

if __name__ == "__main__":
    main()