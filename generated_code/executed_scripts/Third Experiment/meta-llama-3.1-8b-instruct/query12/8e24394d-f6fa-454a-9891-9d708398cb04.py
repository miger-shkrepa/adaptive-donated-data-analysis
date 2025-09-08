import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the results
results = []

# Iterate over each file in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a directory
    if os.path.isdir(os.path.join(root_dir, filename)):
        # Iterate over each file in the directory
        for file in os.listdir(os.path.join(root_dir, filename)):
            # Check if the file is a JSON file
            if file.endswith(".json"):
                # Open the JSON file
                with open(os.path.join(root_dir, filename, file), 'r') as f:
                    # Load the JSON data
                    data = json.load(f)
                    # Check if the JSON data contains the required information
                    if 'string_map_data' in data and 'Time' in data['string_map_data']:
                        # Extract the week and messages sent from the JSON data
                        week = data['string_map_data']['Time']['value']
                        messages_sent = 1  # Assuming one message per file
                        # Append the result to the list
                        results.append([week, messages_sent])

# Check if any results were found
if not results:
    # If no results were found, write the column headers to the CSV file
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Week', 'Messages Sent'])
else:
    # If results were found, write them to the CSV file
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Week', 'Messages Sent'])
        writer.writerows(results)