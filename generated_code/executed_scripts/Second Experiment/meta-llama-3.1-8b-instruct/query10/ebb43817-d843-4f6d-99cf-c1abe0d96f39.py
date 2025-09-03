import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Account', 'Post Views', 'Video Views']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Initialize the counters
    post_views = 0
    video_views = 0

    # Iterate over the JSON files
    for filename in os.listdir(root_dir):
        if filename.endswith('.json'):
            with open(os.path.join(root_dir, filename), 'r') as json_file:
                data = json.load(json_file)

                # Check if the file contains post views data
                if 'impressions_history_posts_seen' in data['structure']:
                    post_views += len(data['structure']['impressions_history_posts_seen'])

                # Check if the file contains video views data
                if 'impressions_history_videos_watched' in data['structure']:
                    video_views += len(data['structure']['impressions_history_videos_watched'])

                # Check if the file contains account information
                if 'profile_account_insights' in data['structure']:
                    account = data['structure']['profile_account_insights'][0]['string_map_data']['Username']['value']
                    writer.writerow({'Account': account, 'Post Views': post_views, 'Video Views': video_views})

    # If no files were found, write the header and return
    if post_views == 0 and video_views == 0:
        writer.writerow({'Account': '', 'Post Views': '', 'Video Views': ''})