import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Function to process messages and count per week
def count_messages_per_week(root_dir):
    message_counts = {}
    
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Path to the inbox directory
        inbox_dir = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")
        
        # Check if the inbox directory exists
        if not os.path.exists(inbox_dir):
            return message_counts
        
        # Iterate over each conversation directory in the inbox
        for conversation_dir in os.listdir(inbox_dir):
            conversation_path = os.path.join(inbox_dir, conversation_dir)
            
            if not os.path.isdir(conversation_path):
                continue
            
            # Iterate over message_X.json files in the conversation directory
            message_files = sorted([f for f in os.listdir(conversation_path) if f.startswith("message_") and f.endswith(".json")])
            
            for message_file in message_files:
                message_file_path = os.path.join(conversation_path, message_file)
                
                try:
                    with open(message_file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        
                        # Check if the required structure exists
                        if 'messages' not in data:
                            continue
                        
                        for message in data['messages']:
                            if 'timestamp_ms' not in message:
                                continue
                            
                            timestamp_ms = message['timestamp_ms']
                            timestamp = timestamp_ms / 1000  # Convert to seconds
                            dt = datetime.fromtimestamp(timestamp)
                            week = dt.strftime('%Y-%W')
                            
                            if 'sender_name' in message and message['sender_name'] == 'username_placeholder':
                                if week not in message_counts:
                                    message_counts[week] = 0
                                message_counts[week] += 1
                except (json.JSONDecodeError, KeyError) as e:
                    raise ValueError(f"Error: Failed to parse JSON file {message_file_path}. Reason: {str(e)}")
    
    except Exception as e:
        raise e
    
    return message_counts

# Function to write the results to a CSV file
def write_to_csv(message_counts):
    csv_path = 'query_responses/results.csv'
    
    try:
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Week', 'Messages Sent']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for week, count in message_counts.items():
                writer.writerow({'Week': f"Week {week}", 'Messages Sent': count})
    
    except Exception as e:
        raise e

# Main function to execute the script
def main():
    try:
        message_counts = count_messages_per_week(root_dir)
        write_to_csv(message_counts)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()