import os
import csv
import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the results list
results = []

# Iterate over each week in the 'media' directory
for week_dir in os.listdir(os.path.join(root_dir, "media")):
    week_dir_path = os.path.join(root_dir, "media", week_dir)
    
    # Check if the week directory exists
    if not os.path.exists(week_dir_path):
        continue
    
    # Initialize the messages sent for the current week
    messages_sent = 0
    
    # Iterate over each file in the week directory
    for file in os.listdir(week_dir_path):
        file_path = os.path.join(week_dir_path, file)
        
        # Check if the file is a JSON file
        if file.endswith(".json"):
            try:
                # Open the JSON file and read its contents
                with open(file_path, "r") as f:
                    data = json.load(f)
                    
                    # Check if the JSON file contains the required data
                    if "creation_timestamp" in data:
                        # Increment the messages sent for the current week
                        messages_sent += 1
            except json.JSONDecodeError:
                # If the JSON file is invalid, skip it
                continue
    
    # Add the results for the current week to the results list
    results.append((week_dir, messages_sent))

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Week", "Messages Sent"])
    writer.writerows(results)