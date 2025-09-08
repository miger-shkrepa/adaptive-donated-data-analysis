import csv
import os
import datetime

# Define the root directory
root_dir = "root_dir"

try:
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
except FileNotFoundError as e:
    print(e)
    exit()

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Week', 'Messages Sent'])

    # Iterate over each conversation folder
    for conversation_folder in os.listdir(root_dir):
        conversation_folder_path = os.path.join(root_dir, conversation_folder)
        if not os.path.isdir(conversation_folder_path):
            continue

        # Initialize the week and messages sent for this conversation
        week = None
        messages_sent = 0

        # Iterate over each message file in the conversation folder
        for message_file in os.listdir(conversation_folder_path):
            message_file_path = os.path.join(conversation_folder_path, message_file)
            if not message_file.startswith('message_') or not message_file.endswith('.json'):
                continue

            try:
                # Load the message file
                with open(message_file_path, 'r') as f:
                    message_data = json.load(f)

                # Get the timestamp of the message
                timestamp = message_data['timestamp']

                # Get the week of the message
                week = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%W')

                # Increment the messages sent for this week
                messages_sent += 1
            except FileNotFoundError:
                # If the message file does not exist, treat its contribution as 0
                pass
            except json.JSONDecodeError:
                # If the message file is not valid JSON, treat its contribution as 0
                pass

        # Write the week and messages sent to the CSV file
        if week is not None:
            writer.writerow([week, messages_sent])