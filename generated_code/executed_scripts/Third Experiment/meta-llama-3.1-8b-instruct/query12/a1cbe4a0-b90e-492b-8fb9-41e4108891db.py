import csv
import os

# Declare the file input variable
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
        if os.path.isdir(os.path.join(root_dir, folder)):
            folder_path = os.path.join(root_dir, folder)
            message_files = [f for f in os.listdir(folder_path) if f.startswith('message_') and f.endswith('.json')]

            # Check if there are any message files in the subfolder
            if not message_files:
                continue

            # Sort the message files by their sequential digit
            message_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

            # Initialize the week and message count
            week = None
            message_count = 0

            # Iterate over each message file
            for file in message_files:
                with open(os.path.join(folder_path, file), 'r') as json_file:
                    data = json.load(json_file)
                    timestamp_ms = data['messages'][0]['timestamp_ms']

                    # Calculate the week from the timestamp
                    week = timestamp_ms // (7 * 24 * 60 * 60 * 1000)

                    # Increment the message count
                    message_count += 1

                    # Write the week and message count to the CSV file
                    with open('query_responses/results.csv', 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([f'Week {week}', message_count])

            # If the week was not updated, write the current week and message count
            if week is None:
                with open('query_responses/results.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([f'Week {week}', message_count])