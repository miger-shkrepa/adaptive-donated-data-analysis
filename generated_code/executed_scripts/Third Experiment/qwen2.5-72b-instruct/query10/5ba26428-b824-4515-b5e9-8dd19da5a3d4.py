import os
import json
import csv

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def process_posts_viewed(posts_viewed_data):
    post_views = {}
    for entry in posts_viewed_data.get("impressions_history_posts_seen", []):
        author = entry["string_map_data"]["Author"]["value"]
        if author not in post_views:
            post_views[author] = 0
        post_views[author] += 1
    return post_views

def process_videos_watched(videos_watched_data):
    video_views = {}
    for entry in videos_watched_data.get("impressions_history_videos_watched", []):
        author = entry["string_map_data"]["Author"]["value"]
        if author not in video_views:
            video_views[author] = 0
        video_views[author] += 1
    return video_views

def aggregate_views(post_views, video_views):
    aggregated_views = {}
    for author, count in post_views.items():
        if author not in aggregated_views:
            aggregated_views[author] = {"Post Views": 0, "Video Views": 0}
        aggregated_views[author]["Post Views"] += count

    for author, count in video_views.items():
        if author not in aggregated_views:
            aggregated_views[author] = {"Post Views": 0, "Video Views": 0}
        aggregated_views[author]["Video Views"] += count

    return aggregated_views

def write_to_csv(aggregated_views):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, views in aggregated_views.items():
            writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    videos_watched_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")

    posts_viewed_data = {}
    videos_watched_data = {}

    if os.path.exists(posts_viewed_path):
        posts_viewed_data = load_json_data(posts_viewed_path)
    if os.path.exists(videos_watched_path):
        videos_watched_data = load_json_data(videos_watched_path)

    post_views = process_posts_viewed(posts_viewed_data)
    video_views = process_videos_watched(videos_watched_data)

    aggregated_views = aggregate_views(post_views, video_views)
    write_to_csv(aggregated_views)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)