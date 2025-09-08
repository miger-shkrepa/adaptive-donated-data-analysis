import csv
import json
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

    # Iterate over the directory structure
    for key, value in json.loads(open(os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')).read()).items():
        if key == 'impressions_history_ads_seen':
            for item in value:
                if 'string_map_data' in item:
                    account = item['string_map_data'].get('Author', '')
                    post_views = 0
                    video_views = 0
                    for post in json.loads(open(os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')).read())['impressions_history_posts_seen']:
                        if 'string_map_data' in post:
                            if post['string_map_data'].get('Author', '') == account:
                                post_views += 1
                    for video in json.loads(open(os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')).read())['impressions_history_videos_watched']:
                        if 'string_map_data' in video:
                            if video['string_map_data'].get('Author', '') == account:
                                video_views += 1
                    writer.writerow({'Account': account, 'Post Views': post_views, 'Video Views': video_views})

    # Iterate over the directory structure
    for key, value in json.loads(open(os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')).read()).items():
        if key == 'impressions_history_videos_watched':
            for item in value:
                if 'string_map_data' in item:
                    account = item['string_map_data'].get('Author', '')
                    post_views = 0
                    video_views = 0
                    for post in json.loads(open(os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')).read())['impressions_history_posts_seen']:
                        if 'string_map_data' in post:
                            if post['string_map_data'].get('Author', '') == account:
                                post_views += 1
                    for video in json.loads(open(os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')).read())['impressions_history_videos_watched']:
                        if 'string_map_data' in video:
                            if video['string_map_data'].get('Author', '') == account:
                                video_views += 1
                    writer.writerow({'Account': account, 'Post Views': post_views, 'Video Views': video_views})

    # Iterate over the directory structure
    for key, value in json.loads(open(os.path.join(root_dir, 'connections', 'followers_and_following', 'following.json')).read()).items():
        if key == 'relationships_following':
            for item in value:
                if 'string_list_data' in item:
                    account = item['string_list_data'][0]['value']
                    post_views = 0
                    video_views = 0
                    for post in json.loads(open(os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')).read())['impressions_history_posts_seen']:
                        if 'string_map_data' in post:
                            if post['string_map_data'].get('Author', '') == account:
                                post_views += 1
                    for video in json.loads(open(os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')).read())['impressions_history_videos_watched']:
                        if 'string_map_data' in video:
                            if video['string_map_data'].get('Author', '') == account:
                                video_views += 1
                    writer.writerow({'Account': account, 'Post Views': post_views, 'Video Views': video_views})