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

    # Write the header row
    writer.writerow(['Week', 'Messages Sent'])

    # Iterate over each subfolder in the inbox directory
    for folder in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, folder)):
            # Initialize the week and message count
            week = None
            message_count = 0

            # Iterate over each message file in the subfolder
            for file in os.listdir(os.path.join(root_dir, folder)):
                if file.startswith('message_') and file.endswith('.json'):
                    # Extract the week from the file name
                    week_str = file.split('_')[1].split('.')[0]
                    week = f'Week {week_str[:4]}-{week_str[4:]}'

                    # Read the message file
                    with open(os.path.join(root_dir, folder, file), 'r') as f:
                        data = json.load(f)

                    # Increment the message count
                    message_count += len(data['messages'])

            # Write the week and message count to the CSV file
            if week:
                writer.writerow([week, message_count])