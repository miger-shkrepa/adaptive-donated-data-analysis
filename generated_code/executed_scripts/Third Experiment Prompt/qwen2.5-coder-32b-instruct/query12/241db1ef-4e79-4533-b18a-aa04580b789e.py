import os
import csv
import json
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

def get_messages_sent_per_week(root_dir):
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Initialize a dictionary to store the count of messages per week
    messages_per_week = {}

    # Path to the inbox directory
    inbox_dir = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")
    
    # Check if the inbox directory exists
    if not os.path.exists(inbox_dir):
        # If the inbox directory does not exist, return an empty CSV with headers
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Week', 'Messages Sent'])
        return

    # Iterate over each subfolder in the inbox directory
    for conversation_dir in os.listdir(inbox_dir):
        conversation_path = os.path.join(inbox_dir, conversation_dir)
        
        # Check if the path is a directory
        if os.path.isdir(conversation_path):
            # Iterate over each message file in the conversation directory
            message_files = sorted([f for f in os.listdir(conversation_path) if f.startswith("message_") and f.endswith(".json")])
            
            for message_file in message_files:
                message_file_path = os.path.join(conversation_path, message_file)
                
                # Check if the message file exists
                if not os.path.exists(message_file_path):
                    continue
                
                # Read the message file
                with open(message_file_path, 'r') as file:
                    try:
                        message_data = json.load(file)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"ValueError: Failed to parse JSON file {message_file_path}: {e}")
                    
                    # Iterate over each message in the message data
                    for message in message_data.get("messages", []):
                        # Get the timestamp of the message
                        timestamp_ms = message.get("timestamp_ms")
                        
                        if timestamp_ms is not None:
                            # Convert timestamp from milliseconds to seconds
                            timestamp_s = timestamp_ms / 1000.0
                            
                            # Convert timestamp to datetime object
                            dt = datetime.fromtimestamp(timestamp_s)
                            
                            # Get the week number in the format 'Week YYYY-WW'
                            week = dt.strftime('Week %Y-%W')
                            
                            # Increment the message count for the week
                            if week in messages_per_week:
                                messages_per_week[week] += 1
                            else:
                                messages_per_week[week] = 1

    # Write the results to a CSV file
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Week', 'Messages Sent'])
        for week, count in sorted(messages_per_week.items()):
            writer.writerow([week, count])

# Call the function to generate the CSV file
get_messages_sent_per_week(root_dir)