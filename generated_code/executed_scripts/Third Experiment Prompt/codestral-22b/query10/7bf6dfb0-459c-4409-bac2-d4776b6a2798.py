import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

results = []

# Iterate over all accounts
for account in os.listdir(os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses')):
    account_dir = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', account)
    if os.path.isdir(account_dir):
        post_views = 0
        video_views = 0

        # Check if posts_viewed.json exists
        posts_viewed_file = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        if os.path.exists(posts_viewed_file):
            with open(posts_viewed_file, 'r') as f:
                data = json.load(f)
                for post in data['impressions_history_posts_seen']:
                    if post['string_map_data']['Author']['value'] == account:
                        post_views += 1

        # Check if stories directory exists
        stories_dir = os.path.join(root_dir, 'your_instagram_activity', 'content', 'stories')
        if os.path.exists(stories_dir):
            for story_file in os.listdir(stories_dir):
                if story_file.endswith('.json'):
                    with open(os.path.join(stories_dir, story_file), 'r') as f:
                        data = json.load(f)
                        for story in data['ig_stories']:
                            if 'cross_post_source' in story and story['cross_post_source']['source_app'] == account:
                                video_views += 1

        results.append({'Account': account, 'Post Views': post_views, 'Video Views': video_views})

# Write results to CSV
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['Account', 'Post Views', 'Video Views'])
    writer.writeheader()
    for row in results:
        writer.writerow(row)