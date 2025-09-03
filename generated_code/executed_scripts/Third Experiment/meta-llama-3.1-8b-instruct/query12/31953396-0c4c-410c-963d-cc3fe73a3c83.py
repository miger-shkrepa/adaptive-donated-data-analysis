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
            folder_path = os.path.join(root_dir, folder)
            week = folder.split('_')[-1]

            # Initialize the total messages sent for the week
            total_messages = 0

            # Iterate over each message file in the subfolder
            for file in os.listdir(folder_path):
                if file.startswith('message_') and file.endswith('.json'):
                    file_path = os.path.join(folder_path, file)
                    try:
                        with open(file_path, 'r') as json_file:
                            data = json.load(json_file)
                            if 'messages' in data:
                                total_messages += len(data['messages'])
                    except ValueError as e:
                        print(f"Error: {e}")
                    except FileNotFoundError as e:
                        print(f"Error: {e}")

            # Write the week and total messages to the CSV file
            writer.writerow([f"Week {week}", total_messages])