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

def process_message_file(file_path):
    """Process a single message file and return the count of messages sent per week."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")
    
    week_message_count = {}
    for message in data.get('messages', []):
        if 'timestamp_ms' in message:
            week = get_week_number(message['timestamp_ms'])
            if week in week_message_count:
                week_message_count[week] += 1
            else:
                week_message_count[week] = 1
    
    return week_message_count

def aggregate_messages_sent(root_dir):
    """Aggregate the number of messages sent per week from all message files in the inbox directory."""
    try:
        inbox_dir = os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox')
        if not os.path.exists(inbox_dir):
            raise FileNotFoundError(f"FileNotFoundError: The inbox directory does not exist.")
    except FileNotFoundError as e:
        print(e)
        return {}
    
    week_message_count = {}
    for conversation_dir in os.listdir(inbox_dir):
        conversation_path = os.path.join(inbox_dir, conversation_dir)
        if os.path.isdir(conversation_path):
            message_files = sorted([f for f in os.listdir(conversation_path) if f.startswith('message_') and f.endswith('.json')])
            for message_file in message_files:
                file_path = os.path.join(conversation_path, message_file)
                try:
                    file_week_count = process_message_file(file_path)
                    for week, count in file_week_count.items():
                        if week in week_message_count:
                            week_message_count[week] += count
                        else:
                            week_message_count[week] = count
                except (FileNotFoundError, ValueError) as e:
                    print(e)
    
    return week_message_count

def save_to_csv(week_message_count, output_path):
    """Save the aggregated message counts to a CSV file."""
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Week', 'Messages Sent'])
            for week, count in sorted(week_message_count.items()):
                writer.writerow([week, count])
    except IOError as e:
        raise IOError(f"IOError: Failed to write to {output_path}. {e}")

def main():
    week_message_count = aggregate_messages_sent(root_dir)
    save_to_csv(week_message_count, 'query_responses/results.csv')

if __name__ == "__main__":
    main()