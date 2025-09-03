import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Initialize data structures to store the results
account_post_views = {}
account_video_views = {}

# Function to process JSON files
def process_json_file(file_path, data_type):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for entry in data.get(data_type, []):
                author = entry['string_map_data']['Author']['value']
                timestamp = entry['string_map_data']['Time']['timestamp']
                if data_type == 'impressions_history_posts_seen':
                    if author in account_post_views:
                        account_post_views[author] += 1
                    else:
                        account_post_views[author] = 1
                elif data_type == 'impressions_history_videos_watched':
                    if author in account_video_views:
                        account_video_views[author] += 1
                    else:
                        account_video_views[author] = 1
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Process the directory structure
try:
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == 'posts_viewed.json':
                process_json_file(os.path.join(root, file), 'impressions_history_posts_seen')
            elif file == 'videos_watched.json':
                process_json_file(os.path.join(root, file), 'impressions_history_videos_watched')
except FileNotFoundError:
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Write the results to a CSV file
try:
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for account in set(account_post_views.keys()).union(account_video_views.keys()):
            writer.writerow({
                'Account': account,
                'Post Views': account_post_views.get(account, 0),
                'Video Views': account_video_views.get(account, 0)
            })
except Exception as e:
    raise ValueError(f"ValueError: Failed to write to the CSV file. {str(e)}")