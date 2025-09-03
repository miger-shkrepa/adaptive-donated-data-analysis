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
    """Process a single message file and return the count of messages sent."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            messages = data.get('messages', [])
            sent_messages = [msg for msg in messages if msg.get('sender_name') == 'YourUsername']  # Replace 'YourUsername' with the actual username
            return len(sent_messages)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while processing {file_path}: {e}")

def process_inbox_directory(inbox_dir):
    """Process all message files in the inbox directory and return a dictionary of week-wise message counts."""
    week_message_count = {}
    for conversation_dir in os.listdir(inbox_dir):
        conversation_path = os.path.join(inbox_dir, conversation_dir)
        if os.path.isdir(conversation_path):
            message_files = sorted([f for f in os.listdir(conversation_path) if f.startswith('message_') and f.endswith('.json')])
            for message_file in message_files:
                file_path = os.path.join(conversation_path, message_file)
                try:
                    message_count = process_message_file(file_path)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        messages = data.get('messages', [])
                        for msg in messages:
                            if msg.get('sender_name') == 'YourUsername':  # Replace 'YourUsername' with the actual username
                                week = get_week_number(msg['timestamp_ms'])
                                if week in week_message_count:
                                    week_message_count[week] += 1
                                else:
                                    week_message_count[week] = 1
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    return week_message_count

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        inbox_dir = os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox')
        if not os.path.exists(inbox_dir):
            raise FileNotFoundError("FileNotFoundError: The inbox directory does not exist.")
        
        week_message_count = process_inbox_directory(inbox_dir)
        
        # Save the results to a CSV file
        results_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(results_path), exist_ok=True)
        with open(results_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Week', 'Messages Sent'])
            for week, count in sorted(week_message_count.items()):
                writer.writerow([week, count])
    
    except Exception as e:
        print(e)
        # Save an empty CSV file with headers if an error occurs
        results_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(results_path), exist_ok=True)
        with open(results_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Week', 'Messages Sent'])

if __name__ == "__main__":
    main()