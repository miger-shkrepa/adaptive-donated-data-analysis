import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

results = []

# Iterate over all accounts
for account in os.listdir(os.path.join(root_dir, 'ads_information', 'ads_and_topics')):
    account_dir = os.path.join(root_dir, 'ads_information', 'ads_and_topics', account)

    # Initialize counters
    post_views = 0
    video_views = 0

    # Check if posts_viewed.json exists
    if os.path.exists(os.path.join(account_dir, 'posts_viewed.json')):
        with open(os.path.join(account_dir, 'posts_viewed.json'), 'r') as f:
            data = json.load(f)
            post_views = len(data['impressions_history_posts_seen'])

    # Check if videos_watched.json exists
    if os.path.exists(os.path.join(account_dir, 'videos_watched.json')):
        with open(os.path.join(account_dir, 'videos_watched.json'), 'r') as f:
            data = json.load(f)
            video_views = len(data['impressions_history_videos_watched'])

    results.append({'Account': account, 'Post Views': post_views, 'Video Views': video_views})

# Write results to CSV
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['Account', 'Post Views', 'Video Views'])
    writer.writeheader()
    for row in results:
        writer.writerow(row)