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
        # Initialize the week and messages sent for the current directory
        week = None
        messages_sent = 0

        # Iterate over each file in the current directory
        for file in os.listdir(os.path.join(root_dir, filename)):
            # Check if the file is a JSON file
            if file.endswith(".json"):
                # Open the JSON file
                with open(os.path.join(root_dir, filename, file), 'r') as f:
                    # Read the JSON file
                    data = f.read()

                    # Try to parse the JSON file
                    try:
                        # Parse the JSON file
                        json_data = eval(data)

                        # Check if the JSON file contains the required data
                        if 'string_list_data' in json_data:
                            # Extract the week and messages sent from the JSON file
                            week = json_data['string_list_data'][0]['timestamp']
                            messages_sent += 1
                    except Exception as e:
                        # Handle any exceptions that occur while parsing the JSON file
                        print(f"Error parsing JSON file: {e}")

        # Add the results for the current directory to the list
        results.append((week, messages_sent))

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Week", "Messages Sent"])  # Write the column headers
    for result in results:
        writer.writerow(result)