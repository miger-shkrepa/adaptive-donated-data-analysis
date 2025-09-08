import csv
import os

# Declare the file input variable
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Week', 'Messages Sent']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Iterate over each subfolder in the inbox directory
    for folder in os.listdir(root_dir):
        if folder.startswith('inbox'):
            folder_path = os.path.join(root_dir, folder)
            # Iterate over each message file in the subfolder
            for file in os.listdir(folder_path):
                if file.startswith('message_') and file.endswith('.json'):
                    file_path = os.path.join(folder_path, file)
                    # Read the message file
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        # Extract the timestamp from the message
                        timestamp = data['timestamp_ms']
                        # Calculate the week from the timestamp
                        week = timestamp // (7 * 24 * 60 * 60 * 1000)
                        # Write the week and messages sent to the CSV file
                        writer.writerow({'Week': f'Week {week // 100}-{week % 100:02}', 'Messages Sent': 1})

# Check if the CSV file was written successfully
if not os.path.exists('query_responses/results.csv'):
    raise ValueError("ValueError: The CSV file was not written successfully.")