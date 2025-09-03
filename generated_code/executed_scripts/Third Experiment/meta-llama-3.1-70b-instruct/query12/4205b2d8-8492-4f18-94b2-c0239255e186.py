import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_messages_sent_per_week(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store the messages sent per week
        messages_sent_per_week = {}

        # Iterate over the subfolders in the 'inbox' directory
        inbox_dir = os.path.join(root_dir, 'inbox')
        if os.path.exists(inbox_dir):
            for conversation_dir in os.listdir(inbox_dir):
                conversation_path = os.path.join(inbox_dir, conversation_dir)
                if os.path.isdir(conversation_path):
                    # Iterate over the message files in the conversation directory
                    message_files = [f for f in os.listdir(conversation_path) if f.startswith('message_') and f.endswith('.json')]
                    message_files.sort()
                    for message_file in message_files:
                        message_path = os.path.join(conversation_path, message_file)
                        with open(message_path, 'r') as f:
                            message_data = json.load(f)
                            # Get the timestamp of the message
                            timestamp = message_data.get('timestamp')
                            if timestamp:
                                # Convert the timestamp to a datetime object
                                dt = datetime.fromtimestamp(timestamp)
                                # Get the week number
                                week = dt.strftime('Week %Y-%U')
                                # Increment the messages sent for the week
                                messages_sent_per_week[week] = messages_sent_per_week.get(week, 0) + 1
        return messages_sent_per_week

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(messages_sent_per_week):
    try:
        # Save the results to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Week', 'Messages Sent'])
            for week, messages_sent in messages_sent_per_week.items():
                writer.writerow([week, messages_sent])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        messages_sent_per_week = get_messages_sent_per_week(root_dir)
        if messages_sent_per_week:
            save_to_csv(messages_sent_per_week)
        else:
            # Save a CSV file with only the column headers if no data is available
            with open('query_responses/results.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Week', 'Messages Sent'])
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()