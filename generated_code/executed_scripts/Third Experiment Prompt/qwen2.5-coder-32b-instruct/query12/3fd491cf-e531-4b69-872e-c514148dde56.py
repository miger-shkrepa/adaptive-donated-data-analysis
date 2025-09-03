import os
import json
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

def get_week_number(timestamp):
    """Convert a timestamp to a week number in the format 'Week YYYY-WW'."""
    return datetime.fromtimestamp(timestamp).strftime('Week %Y-%W')

def count_messages_per_week(root_dir):
    """Count the number of messages sent per week."""
    message_counts = {}

    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Check if the 'inbox' directory exists
        inbox_dir = os.path.join(root_dir, 'inbox')
        if not os.path.exists(inbox_dir):
            # If 'inbox' directory does not exist, return an empty result
            return []
        
        # Iterate over each conversation subfolder in the 'inbox' directory
        for conversation in os.listdir(inbox_dir):
            conversation_path = os.path.join(inbox_dir, conversation)
            if os.path.isdir(conversation_path):
                # Iterate over each message file in the conversation subfolder
                message_files = sorted([f for f in os.listdir(conversation_path) if f.startswith('message_') and f.endswith('.json')])
                for message_file in message_files:
                    message_file_path = os.path.join(conversation_path, message_file)
                    try:
                        with open(message_file_path, 'r', encoding='utf-8') as file:
                            messages = json.load(file)
                            for message in messages:
                                if 'sender' in message and 'timestamp' in message:
                                    # Assuming 'sender' is a key that indicates the user sent the message
                                    if message['sender'] == 'user':  # Adjust this condition based on actual data structure
                                        week = get_week_number(message['timestamp'])
                                        if week in message_counts:
                                            message_counts[week] += 1
                                        else:
                                            message_counts[week] = 1
                    except (FileNotFoundError, ValueError) as e:
                        print(f"Error: Failed to read or parse {message_file_path}. {e}")
    
    except FileNotFoundError as e:
        print(e)
        return []

    # Convert the message counts to a list of tuples
    result = [(week, count) for week, count in message_counts.items()]
    result.sort(key=lambda x: x[0])  # Sort by week
    return result

def write_csv(data, output_path):
    """Write the data to a CSV file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write("Week,Messages Sent\n")
            for week, count in data:
                file.write(f"{week},{count}\n")
    except IOError as e:
        print(f"Error: Failed to write to {output_path}. {e}")

# Main execution
if __name__ == "__main__":
    result = count_messages_per_week(root_dir)
    write_csv(result, 'query_responses/results.csv')