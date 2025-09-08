import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

accounts_data = []

# Iterate over the 'posts' directory
posts_dir = os.path.join(root_dir, 'posts')
if os.path.exists(posts_dir):
    for filename in os.listdir(posts_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(posts_dir, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                for post in data:
                    account = post.get('title', 'Unknown')
                    post_views = 0  # Information not available in the structure
                    video_views = 0  # Information not available in the structure
                    accounts_data.append([account, post_views, video_views])

# Iterate over the 'videos' directory
videos_dir = os.path.join(root_dir, 'videos')
if os.path.exists(videos_dir):
    for filename in os.listdir(videos_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(videos_dir, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                for video in data:
                    account = video.get('title', 'Unknown')
                    post_views = 0  # Information not available in the structure
                    video_views = 0  # Information not available in the structure
                    accounts_data.append([account, post_views, video_views])

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Account', 'Post Views', 'Video Views'])
    writer.writerows(accounts_data)