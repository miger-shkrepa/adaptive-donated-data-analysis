import csv
import os
import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the output CSV file
output_file = "query_responses/results.csv"

# Initialize the CSV writer
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Week", "Messages Sent"])

    # Iterate over all subdirectories in the root directory
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check if the subdirectory is an 'inbox' directory
        if 'inbox' in dirnames:
            dirnames.remove('inbox')
            inbox_dir = os.path.join(dirpath, 'inbox')

            # Initialize the week and message count
            week = None
            message_count = 0

            # Iterate over all message files in the inbox directory
            for filename in os.listdir(inbox_dir):
                if filename.startswith('message_') and filename.endswith('.json'):
                    # Extract the week from the filename
                    week_str = filename.split('_')[1].split('.')[0]
                    week = datetime.datetime.strptime(week_str, '%Y-%W')

                    # Read the message file
                    try:
                        with open(os.path.join(inbox_dir, filename), 'r') as file:
                            data = json.load(file)

                            # Extract the message count from the file
                            message_count += len(data['messages'])
                    except FileNotFoundError:
                        # If the file does not exist, treat its contribution as 0
                        pass

            # Write the week and message count to the output CSV file
            if week is not None:
                writer.writerow([week.strftime('%Y-%W'), message_count])