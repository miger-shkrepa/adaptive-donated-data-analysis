import os
import json
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

def get_week_number(timestamp_ms):
    """Convert timestamp in milliseconds to 'Week YYYY-WW' format."""
    dt = datetime.fromtimestamp(timestamp_ms / 1000)
    return dt.strftime('%Y-%W')

def process_message_file(file_path):
    """Process a single message file and return the count of messages sent per week."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")
    
    messages_sent_per_week = {}
    for message in data.get('messages', []):
        if 'sender_name' in message and 'timestamp_ms' in message:
            week = get_week_number(message['timestamp_ms'])
            if message['sender_name'] == 'YourUsername':  # Replace 'YourUsername' with the actual username
                if week in messages_sent_per_week:
                    messages_sent_per_week[week] += 1
                else:
                    messages_sent_per_week[week] = 1
    return messages_sent_per_week

def aggregate_messages_sent(root_dir):
    """Aggregate the number of messages sent per week from all message files."""
    messages_sent_per_week = {}
    try:
        inbox_dir = os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox')
        if not os.path.exists(inbox_dir):
            raise FileNotFoundError(f"FileNotFoundError: The inbox directory does not exist.")
        
        for conversation_dir in os.listdir(inbox_dir):
            conversation_path = os.path.join(inbox_dir, conversation_dir)
            if os.path.isdir(conversation_path):
                message_files = sorted([f for f in os.listdir(conversation_path) if f.startswith('message_') and f.endswith('.json')])
                for message_file in message_files:
                    file_path = os.path.join(conversation_path, message_file)
                    try:
                        weekly_counts = process_message_file(file_path)
                        for week, count in weekly_counts.items():
                            if week in messages_sent_per_week:
                                messages_sent_per_week[week] += count
                            else:
                                messages_sent_per_week[week] = count
                    except (FileNotFoundError, ValueError) as e:
                        print(f"Error processing {file_path}: {e}")
    
    except FileNotFoundError as e:
        print(e)
    
    return messages_sent_per_week

def save_to_csv(messages_sent_per_week, output_path):
    """Save the aggregated messages sent per week to a CSV file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write("Week,Messages Sent\n")
            for week in sorted(messages_sent_per_week.keys()):
                file.write(f"{week},{messages_sent_per_week[week]}\n")
    except IOError as e:
        raise IOError(f"IOError: Failed to write to {output_path}. {e}")

def main():
    messages_sent_per_week = aggregate_messages_sent(root_dir)
    save_to_csv(messages_sent_per_week, 'query_responses/results.csv')

if __name__ == "__main__":
    main()