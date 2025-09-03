import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the messages sent per week
messages_per_week = {}

# Iterate over each file in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a directory
    if os.path.isdir(os.path.join(root_dir, filename)):
        # Check if the directory is the 'inbox' directory
        if filename == 'inbox':
            # Iterate over each file in the 'inbox' directory
            for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, filename)):
                # Iterate over each file in the current directory
                for filename in filenames:
                    # Check if the file is a JSON file
                    if filename.endswith('.json'):
                        # Extract the week from the filename
                        week = filename.split('_')[0]
                        # Check if the week is already in the dictionary
                        if week in messages_per_week:
                            # Increment the messages sent for the week
                            messages_per_week[week] += 1
                        else:
                            # Add the week to the dictionary with a count of 1
                            messages_per_week[week] = 1

# Create a CSV file to store the results
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create a CSV writer
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(['Week', 'Messages Sent'])
    # Iterate over each week in the dictionary
    for week, messages in messages_per_week.items():
        # Write the week and messages sent to the CSV file
        writer.writerow([week, messages])