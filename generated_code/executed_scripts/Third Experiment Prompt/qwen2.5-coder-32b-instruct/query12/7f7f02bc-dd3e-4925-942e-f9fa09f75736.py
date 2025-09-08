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

def process_messages_in_file(file_path):
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
        if 'timestamp_ms' in message and 'sender_name' in message:
            week_number = get_week_number(message['timestamp_ms'])
            if message['sender_name'] == 'YourUsername':  # Replace 'YourUsername' with the actual username
                if week_number in messages_sent_per_week:
                    messages_sent_per_week[week_number] += 1
                else:
                    messages_sent_per_week[week_number] = 1
    return messages_sent_per_week

def aggregate_messages_sent_per_week(root_dir):
    """Aggregate the number of messages sent per week from all message files."""
    messages_sent_per_week = {}
    inbox_dir = os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox')
    
    if not os.path.exists(inbox_dir):
        return messages_sent_per_week
    
    for conversation_dir in os.listdir(inbox_dir):
        conversation_path = os.path.join(inbox_dir, conversation_dir)
        if os.path.isdir(conversation_path):
            message_files = sorted([f for f in os.listdir(conversation_path) if f.startswith('message_') and f.endswith('.json')])
            for message_file in message_files:
                file_path = os.path.join(conversation_path, message_file)
                try:
                    weekly_counts = process_messages_in_file(file_path)
                    for week, count in weekly_counts.items():
                        if week in messages_sent_per_week:
                            messages_sent_per_week[week] += count
                        else:
                            messages_sent_per_week[week] = count
                except (FileNotFoundError, ValueError) as e:
                    print(f"Error processing {file_path}: {e}")
    
    return messages_sent_per_week

def save_results_to_csv(messages_sent_per_week, output_path):
    """Save the aggregated messages sent per week to a CSV file."""
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Week', 'Messages Sent'])
            for week, count in sorted(messages_sent_per_week.items()):
                writer.writerow([week, count])
    except IOError as e:
        raise IOError(f"IOError: Failed to write to {output_path}. {e}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        messages_sent_per_week = aggregate_messages_sent_per_week(root_dir)
        save_results_to_csv(messages_sent_per_week, 'query_responses/results.csv')
    
    except (FileNotFoundError, ValueError, IOError) as e:
        print(e)
        # Create an empty CSV file with headers if there's an error
        save_results_to_csv({}, 'query_responses/results.csv')

if __name__ == "__main__":
    main()