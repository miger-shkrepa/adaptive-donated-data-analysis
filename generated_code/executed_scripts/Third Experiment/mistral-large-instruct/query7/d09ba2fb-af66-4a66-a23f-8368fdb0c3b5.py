import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Initialize a dictionary to store engagement counts
engagement_counts = {}

# Function to process JSON files and count story engagements
def process_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if 'messages' in data:
                for message in data['messages']:
                    if 'content' in message and 'sender_name' in message:
                        sender_name = message['sender_name']
                        if sender_name in engagement_counts:
                            engagement_counts[sender_name] += 1
                        else:
                            engagement_counts[sender_name] = 1
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

# Walk through the directory structure and process JSON files
try:
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(subdir, file)
                process_json_file(file_path)
except FileNotFoundError:
    raise FileNotFoundError("Error: The root directory does not exist.")

# Write the results to a CSV file
try:
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['User', 'Times Engaged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user, count in engagement_counts.items():
            writer.writerow({'User': user, 'Times Engaged': count})
except Exception as e:
    raise ValueError(f"Error: {str(e)}")