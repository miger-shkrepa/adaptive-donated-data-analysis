import os
import json
import csv

root_dir = "root_dir"

def get_views(root_dir):
    views = {}
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        # Iterate through 'ads_information' directory
        ads_info_dir = os.path.join(root_dir, 'ads_information', 'ads_and_topics')
        if os.path.exists(ads_info_dir):
            for filename in os.listdir(ads_info_dir):
                if filename == 'posts_viewed.json':
                    file_path = os.path.join(ads_info_dir, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        if 'impressions_history_posts_seen' in data:
                            for post in data['impressions_history_posts_seen']:
                                if 'string_map_data' in post and 'Author' in post['string_map_data']:
                                    author = post['string_map_data']['Author']['value']
                                    if author not in views:
                                        views[author] = {'post_views': 1, 'video_views': 0}
                                    else:
                                        views[author]['post_views'] += 1

                elif filename == 'videos_watched.json':
                    file_path = os.path.join(ads_info_dir, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        if 'impressions_history_videos_watched' in data:
                            for video in data['impressions_history_videos_watched']:
                                if 'string_map_data' in video and 'Author' in video['string_map_data']:
                                    author = video['string_map_data']['Author']['value']
                                    if author not in views:
                                        views[author] = {'post_views': 0, 'video_views': 1}
                                    else:
                                        views[author]['video_views'] += 1

        # Iterate through 'your_instagram_activity' directory
        activity_dir = os.path.join(root_dir, 'your_instagram_activity', 'media')
        if os.path.exists(activity_dir):
            for filename in os.listdir(activity_dir):
                if filename == 'posts_1.json':
                    file_path = os.path.join(activity_dir, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        if 'media' in data:
                            for post in data['media']:
                                if 'media_metadata' in post and 'camera_metadata' in post['media_metadata']:
                                    if post['media_metadata']['camera_metadata']['has_camera_metadata']:
                                        author = post['title']
                                        if author not in views:
                                            views[author] = {'post_views': 1, 'video_views': 0}
                                        else:
                                            views[author]['post_views'] += 1

    except FileNotFoundError as e:
        print(e)
        return None

    return views

def save_to_csv(views):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        if views is not None:
            for account, view_counts in views.items():
                writer.writerow({'Account': account, 'Post Views': view_counts['post_views'], 'Video Views': view_counts['video_views']})

views = get_views(root_dir)
save_to_csv(views)