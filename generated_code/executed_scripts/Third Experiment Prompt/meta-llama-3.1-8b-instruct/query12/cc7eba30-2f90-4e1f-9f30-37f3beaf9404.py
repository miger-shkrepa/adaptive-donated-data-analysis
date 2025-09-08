import os
import csv
import json
from datetime import datetime

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

    # Iterate over the 'inbox' directory
    inbox_dir = os.path.join(root_dir, "connections", "contacts", "inbox")
    if os.path.exists(inbox_dir):
        for folder in os.listdir(inbox_dir):
            folder_path = os.path.join(inbox_dir, folder)
            
            # Check if the folder is a directory
            if os.path.isdir(folder_path):
                # Initialize the week and messages sent
                week = None
                messages_sent = 0
                
                # Iterate over the message_X.json files in the folder
                for file in os.listdir(folder_path):
                    if file.startswith("message_") and file.endswith(".json"):
                        file_path = os.path.join(folder_path, file)
                        
                        # Check if the file exists
                        if os.path.exists(file_path):
                            # Load the JSON file
                            try:
                                with open(file_path, 'r') as json_file:
                                    data = json.load(json_file)
                                    
                                    # Get the week from the file name
                                    week = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%W')
                                    
                                    # Get the messages sent
                                    messages_sent += len(data["messages"])
                            except json.JSONDecodeError as e:
                                # If the file is not a valid JSON, treat its contribution as 0
                                print(f"Error parsing JSON in file {file_path}: {e}")
                                messages_sent += 0
                        else:
                            # If the file does not exist, treat its contribution as 0
                            messages_sent += 0
                
                # Write the week and messages sent to the CSV file
                if week is not None:
                    writer.writerow([week, messages_sent])
    else:
        # If the 'inbox' directory does not exist, write the column headers only
        writer.writerow(["Week", "Messages Sent"])