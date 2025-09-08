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
        # Iterate over each file in the subdirectory
        for subfilename in os.listdir(os.path.join(root_dir, filename)):
            # Check if the file is a JSON file
            if subfilename.endswith(".json"):
                # Open the JSON file
                with open(os.path.join(root_dir, filename, subfilename), 'r') as file:
                    # Load the JSON data
                    data = eval(file.read())
                    # Check if the JSON data contains the required information
                    if 'messages' in data and 'timestamp_ms' in data['messages'][0]:
                        # Extract the week from the timestamp
                        week = data['messages'][0]['timestamp_ms'] // (7 * 24 * 60 * 60 * 1000)
                        # Increment the messages sent for the week
                        messages_per_week[week] = messages_per_week.get(week, 0) + len(data['messages'])

# Create a CSV file to store the results
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create a CSV writer
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(['Week', 'Messages Sent'])
    # Write the results
    for week, messages in messages_per_week.items():
        writer.writerow([f'Week {week}', messages])