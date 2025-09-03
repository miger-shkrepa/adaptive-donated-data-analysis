import csv
import os
import json
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the results list
results = []

# Iterate over each conversation folder
for conversation_folder in os.listdir(root_dir):
    conversation_folder_path = os.path.join(root_dir, conversation_folder)
    
    # Check if the conversation folder is a directory
    if not os.path.isdir(conversation_folder_path):
        continue
    
    # Initialize the week and messages sent for this conversation
    week = None
    messages_sent = 0
    
    # Iterate over each message file
    for message_file in os.listdir(conversation_folder_path):
        message_file_path = os.path.join(conversation_folder_path, message_file)
        
        # Check if the message file is a JSON file
        if not message_file.endswith(".json"):
            continue
        
        # Load the message file
        try:
            with open(message_file_path, "r") as f:
                message_data = json.load(f)
        except json.JSONDecodeError:
            # If the message file is not a valid JSON file, skip it
            continue
        
        # Get the timestamp of the message
        timestamp = message_data.get("timestamp")
        
        # If the timestamp is not present, skip this message
        if timestamp is None:
            continue
        
        # Convert the timestamp to a datetime object
        message_datetime = datetime.fromtimestamp(timestamp)
        
        # Get the week of the message
        message_week = message_datetime.strftime("%Y-%W")
        
        # If this is the first message in the conversation, set the week
        if week is None:
            week = message_week
        
        # Increment the messages sent for this week
        if week == message_week:
            messages_sent += 1
    
    # Add the results for this conversation to the list
    results.append((week, messages_sent))

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Week", "Messages Sent"])  # Write the column headers
    writer.writerows(results)