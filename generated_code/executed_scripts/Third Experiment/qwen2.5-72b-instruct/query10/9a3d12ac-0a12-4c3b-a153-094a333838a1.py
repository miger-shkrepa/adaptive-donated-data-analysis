import os
import json
import csv

root_dir = "root_dir"

def process_data(directory):
    post_views = {}
    video_views = {}

    ads_and_topics_path = os.path.join(directory, "ads_information", "ads_and_topics")
    if not os.path.exists(ads_and_topics_path):
        return post_views, video_views

    try:
        with open(os.path.join(ads_and_topics_path, "posts_viewed.json"), 'r') as file:
            posts_data = json.load(file)
            for entry in posts_data.get("impressions_history_posts_seen", []):
                author = entry["string_map_data"]["Author"]["value"]
                post_views[author] = post_views.get(author, 0) + 1
    except FileNotFoundError:
        raise FileNotFoundError("Error: The posts_viewed.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: posts_viewed.json is not a valid JSON file.")

    try:
        with open(os.path.join(ads_and_topics_path, "videos_watched.json"), 'r') as file:
            videos_data = json.load(file)
            for entry in videos_data.get("impressions_history_videos_watched", []):
                author = entry["string_map_data"]["Author"]["value"]
                video_views[author] = video_views.get(author, 0) + 1
    except FileNotFoundError:
        raise FileNotFoundError("Error: The videos_watched.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: videos_watched.json is not a valid JSON file.")

    return post_views, video_views

def write_to_csv(post_views, video_views):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account in set(list(post_views.keys()) + list(video_views.keys())):
            writer.writerow({
                'Account': account,
                'Post Views': post_views.get(account, 0),
                'Video Views': video_views.get(account, 0)
            })

if __name__ == "__main__":
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    try:
        post_views, video_views = process_data(root_dir)
        write_to_csv(post_views, video_views)
    except Exception as e:
        print(e)