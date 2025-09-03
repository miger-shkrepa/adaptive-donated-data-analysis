import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Initialize the CSV writer
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Account", "Post Views", "Video Views"])

    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    # Initialize dictionaries to store post and video views
    post_views = {}
    video_views = {}

    # Function to process JSON files
    def process_json_file(file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: The file {file_path} does not exist.")
        except json.JSONDecodeError:
            raise ValueError(f"Error: The file {file_path} is not a valid JSON file.")

    # Process messages JSON files
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(subdir, file)
                data = process_json_file(file_path)

                # Check if the file contains messages
                if 'messages' in data:
                    for message in data['messages']:
                        account = message.get('sender_name', 'Unknown')
                        if 'content' in message:
                            if account not in post_views:
                                post_views[account] = 0
                            post_views[account] += 1
                        if 'share' in message and 'link' in message['share']:
                            if account not in video_views:
                                video_views[account] = 0
                            video_views[account] += 1

    # Write the results to the CSV file
    for account in set(post_views.keys()).union(video_views.keys()):
        writer.writerow([account, post_views.get(account, 0), video_views.get(account, 0)])

print(f"Results have been saved to {output_csv}")