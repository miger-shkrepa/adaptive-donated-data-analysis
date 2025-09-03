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
        if os.path.isdir(os.path.join(root_dir, folder)):
            # Initialize the week and message count
            week = None
            message_count = 0

            # Iterate over each message file in the subfolder
            for file in os.listdir(os.path.join(root_dir, folder)):
                if file.startswith('message_') and file.endswith('.json'):
                    # Extract the week from the file name
                    week_match = os.path.splitext(file)[0].split('_')[-1]
                    if week is None or week_match != week:
                        if week is not None:
                            writer.writerow([week, message_count])
                        week = week_match
                        message_count = 0

                    # Read the message file
                    with open(os.path.join(root_dir, folder, file), 'r') as f:
                        data = json.load(f)

                    # Increment the message count
                    message_count += len(data['messages'])

            # Write the final week and message count
            if week is not None:
                writer.writerow([week, message_count])