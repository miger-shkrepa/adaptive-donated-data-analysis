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
def process_json_file(file_path, key):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for item in data.get(key, []):
                string_map_data = item.get('string_map_data', {})
                if key == 'impressions_history_posts_seen':
                    account = string_map_data.get('Author', {}).get('value', '')
                    if account:
                        account_post_views[account] = account_post_views.get(account, 0) + 1
                elif key == 'impressions_history_videos_watched':
                    account = string_map_data.get('Time', {}).get('value', '')
                    if account:
                        account_video_views[account] = account_video_views.get(account, 0) + 1
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Process the posts_viewed.json file
posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
if os.path.exists(posts_viewed_path):
    process_json_file(posts_viewed_path, 'impressions_history_posts_seen')

# Process the videos_watched.json file
videos_watched_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')
if os.path.exists(videos_watched_path):
    process_json_file(videos_watched_path, 'impressions_history_videos_watched')

# Write the results to the CSV file
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
    raise IOError(f"IOError: Failed to write to the CSV file. {str(e)}")

print(f"Results have been written to {output_csv}")