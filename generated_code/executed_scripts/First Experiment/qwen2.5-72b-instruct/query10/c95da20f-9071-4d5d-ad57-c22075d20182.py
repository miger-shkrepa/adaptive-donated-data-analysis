import os
import json
import csv

root_dir = "root_dir"

def process_data():
    post_views = {}
    video_views = {}

    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        ads_info_path = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if not os.path.exists(ads_info_path):
            raise FileNotFoundError("FileNotFoundError: The ads_and_topics directory does not exist.")

        for file_name in ["posts_viewed.json", "videos_watched.json"]:
            file_path = os.path.join(ads_info_path, file_name)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"FileNotFoundError: The file {file_name} does not exist.")

            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if file_name == "posts_viewed.json":
                    for entry in data["impressions_history_posts_seen"]:
                        author = entry["string_map_data"]["Author"]["value"]
                        if author not in post_views:
                            post_views[author] = 0
                        post_views[author] += 1
                elif file_name == "videos_watched.json":
                    for entry in data["impressions_history_videos_watched"]:
                        author = entry["string_map_data"]["Author"]["value"]
                        if author not in video_views:
                            video_views[author] = 0
                        video_views[author] += 1

        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Account', 'Post Views', 'Video Views']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for account in set(list(post_views.keys()) + list(video_views.keys())):
                writer.writerow({
                    'Account': account,
                    'Post Views': post_views.get(account, 0),
                    'Video Views': video_views.get(account, 0)
                })

    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding failed. Reason: {str(e)}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred. Reason: {str(e)}")

process_data()