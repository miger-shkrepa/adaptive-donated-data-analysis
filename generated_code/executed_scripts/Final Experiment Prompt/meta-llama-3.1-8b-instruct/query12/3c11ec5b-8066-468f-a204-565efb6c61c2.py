import csv
import os
import datetime
import json

root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Week', 'Messages Sent'])

    # Iterate over each subfolder in the inbox directory
    for folder in os.listdir(os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox')):
        folder_path = os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox', folder)
        
        # Check if the folder is a directory
        if os.path.isdir(folder_path):
            # Initialize the message count for the current week
            messages_sent = 0
            
            # Initialize the current week
            current_week = None
            
            # Iterate over each message file in the folder
            for file in os.listdir(folder_path):
                if file.startswith('message_') and file.endswith('.json'):
                    file_path = os.path.join(folder_path, file)
                    
                    try:
                        # Load the message data from the JSON file
                        with open(file_path, 'r') as json_file:
                            message_data = json.load(json_file)
                            
                            # Check if the 'timestamp_ms' key exists in the message data
                            if 'timestamp_ms' in message_data:
                                # Get the timestamp of the message
                                timestamp_ms = message_data['timestamp_ms']
                                
                                # Convert the timestamp to a datetime object
                                timestamp = datetime.datetime.fromtimestamp(timestamp_ms / 1000)
                                
                                # Get the week of the message
                                week = timestamp.strftime('%Y-%W')
                                
                                # If the current week is different from the previous week, update the current week and reset the message count
                                if week != current_week:
                                    if current_week is not None:
                                        writer.writerow([current_week, messages_sent])
                                    current_week = week
                                    messages_sent = 0
                                
                                # Increment the message count for the current week
                                messages_sent += 1
                            else:
                                # If the 'timestamp_ms' key does not exist, treat its contribution as 0
                                pass
                    except FileNotFoundError:
                        # If the message file does not exist, treat its contribution as 0
                        pass
                    except json.JSONDecodeError:
                        # If the message file is not a valid JSON file, treat its contribution as 0
                        pass
            
            # Write the final message count for the current week
            if current_week is not None:
                writer.writerow([current_week, messages_sent])