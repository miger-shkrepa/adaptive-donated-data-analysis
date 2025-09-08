import csv
import os

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty dictionary to store the weekly message count
weekly_message_count = {}

# Iterate over each subfolder in the inbox directory
for folder in os.listdir(root_dir):
    if os.path.isdir(os.path.join(root_dir, folder)):
        # Initialize the message count for the current week to 0
        weekly_message_count[folder] = 0

        # Iterate over each message file in the subfolder
        for file in os.listdir(os.path.join(root_dir, folder)):
            if file.startswith('message_') and file.endswith('.json'):
                # Extract the week number from the file name
                week_number = int(file.split('_')[1].split('.')[0])

                # Check if the week number is valid (i.e., between 1 and 52)
                if 1 <= week_number <= 52:
                    # Increment the message count for the current week
                    weekly_message_count[folder] += 1

# Create a CSV writer to write the results to a file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the column headers
    writer.writerow(['Week', 'Messages Sent'])

    # Write the weekly message count to the CSV file
    for folder, count in weekly_message_count.items():
        writer.writerow([folder, count])