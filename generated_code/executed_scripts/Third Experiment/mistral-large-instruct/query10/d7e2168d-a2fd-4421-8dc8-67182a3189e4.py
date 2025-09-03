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

# Function to process JSON files and extract data
def process_json_file(file_path, data_type):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for entry in data.get(data_type, []):
                author = entry.get('string_map_data', {}).get('Author', {}).get('value', 'Unknown')
                if data_type == 'impressions_history_posts_seen':
                    if author not in account_post_views:
                        account_post_views[author] = 0
                    account_post_views[author] += 1
                elif data_type == 'impressions_history_videos_watched':
                    if author not in account_video_views:
                        account_video_views[author] = 0
                    account_video_views[author] += 1
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

# Function to traverse the directory and process files
def traverse_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file == 'posts_viewed.json':
                process_json_file(os.path.join(root, file), 'impressions_history_posts_seen')
            elif file == 'videos_watched.json':
                process_json_file(os.path.join(root, file), 'impressions_history_videos_watched')

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# Traverse the directory and process files
try:
    traverse_directory(root_dir)
except Exception as e:
    print(e)
    # Create an empty CSV file with headers if an error occurs
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Account', 'Post Views', 'Video Views'])
    exit()

# Write the results to the CSV file
with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Account', 'Post Views', 'Video Views'])
    all_accounts = set(account_post_views.keys()).union(set(account_video_views.keys()))
    for account in all_accounts:
        post_views = account_post_views.get(account, 0)
        video_views = account_video_views.get(account, 0)
        writer.writerow([account, post_views, video_views])