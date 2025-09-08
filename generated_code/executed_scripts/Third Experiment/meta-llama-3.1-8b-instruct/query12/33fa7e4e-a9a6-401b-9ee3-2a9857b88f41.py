import csv
import os

def process_directory(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize the list to store the results
        results = []

        # Iterate over each subdirectory in the root directory
        for dir in os.listdir(root_dir):
            # Construct the full path to the subdirectory
            dir_path = os.path.join(root_dir, dir)

            # Check if the subdirectory is a directory
            if os.path.isdir(dir_path):
                # Initialize the week and messages sent for the current directory
                week = None
                messages_sent = 0

                # Iterate over each file in the subdirectory
                for file in os.listdir(dir_path):
                    # Construct the full path to the file
                    file_path = os.path.join(dir_path, file)

                    # Check if the file is a JSON file
                    if file.endswith(".json"):
                        # Open the JSON file and read its contents
                        with open(file_path, 'r') as f:
                            data = json.load(f)

                        # Check if the JSON file contains the required data
                        if 'messages' in data and data['messages']:
                            # Extract the week from the JSON file
                            week = data['title']

                            # Iterate over each message in the JSON file
                            for message in data['messages']:
                                # Check if the message is a share
                                if 'share' in message:
                                    # Increment the messages sent for the current week
                                    messages_sent += 1

                # Check if the week was extracted from the JSON file
                if week:
                    # Append the results for the current directory to the list
                    results.append([week, messages_sent])

        # Write the results to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Week", "Messages Sent"])  # header
            writer.writerows(results)

    except Exception as e:
        raise ValueError("ValueError: " + str(e))

# Declare the variable referring to the file input
root_dir = "root_dir"

# Call the function to process the directory
process_directory(root_dir)