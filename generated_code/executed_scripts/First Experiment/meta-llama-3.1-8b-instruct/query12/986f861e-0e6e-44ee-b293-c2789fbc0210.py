import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Week', 'Messages Sent'])

    # Iterate over each subfolder in the inbox directory
    for folder in os.listdir(root_dir):
        if folder == 'inbox':
            folder_path = os.path.join(root_dir, folder)
            for filename in os.listdir(folder_path):
                if filename.startswith('message_') and filename.endswith('.json'):
                    message_file_path = os.path.join(folder_path, filename)
                    with open(message_file_path, 'r') as message_file:
                        # Parse the JSON file
                        data = json.load(message_file)
                        # Extract the timestamp
                        timestamp = data['timestamp_ms']
                        # Calculate the week
                        week = timestamp // (7 * 24 * 60 * 60 * 1000)
                        # Extract the messages
                        messages = data['messages']
                        # Count the messages
                        message_count = len(messages)
                        # Write the result to the CSV file
                        writer.writerow([f'Week {week:04d}-{(week % 52 + 1):02d}', message_count])