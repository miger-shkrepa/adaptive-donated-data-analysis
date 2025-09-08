import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Function to read JSON file and handle errors
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to extract account and view counts from posts and reels
def extract_account_views(data):
    account_views = {}
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                account = item.get('title', 'Unknown')
                if account not in account_views:
                    account_views[account] = {'post_views': 0, 'video_views': 0}
                media_list = item.get('media', [])
                if isinstance(media_list, list):
                    for media in media_list:
                        if isinstance(media, dict):
                            uri = media.get('uri', '')
                            if uri.endswith('.mp4'):
                                account_views[account]['video_views'] += 1
                            else:
                                account_views[account]['post_views'] += 1
    return account_views

# Initialize the dictionary to store account views
account_views = {}

# Path to posts_1.json
posts_file_path = os.path.join(root_dir, 'your_instagram_activity', 'media', 'posts_1.json')
# Path to reels.json
reels_file_path = os.path.join(root_dir, 'your_instagram_activity', 'media', 'reels.json')

# Read posts_1.json if it exists
if os.path.exists(posts_file_path):
    try:
        posts_data = read_json_file(posts_file_path)
        account_views.update(extract_account_views(posts_data))
    except (FileNotFoundError, ValueError) as e:
        print(f"Error processing {posts_file_path}: {e}")

# Read reels.json if it exists
if os.path.exists(reels_file_path):
    try:
        reels_data = read_json_file(reels_file_path)
        account_views.update(extract_account_views(reels_data))
    except (FileNotFoundError, ValueError) as e:
        print(f"Error processing {reels_file_path}: {e}")

# Prepare the CSV data
csv_data = [['Account', 'Post Views', 'Video Views']]
for account, views in account_views.items():
    csv_data.append([account, views['post_views'], views['video_views']])

# Write the CSV file
output_path = 'query_responses/results.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(csv_data)