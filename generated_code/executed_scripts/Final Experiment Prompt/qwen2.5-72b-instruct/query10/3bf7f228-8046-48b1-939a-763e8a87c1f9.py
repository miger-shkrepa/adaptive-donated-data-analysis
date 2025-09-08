import json
import os
import csv

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def count_views(data, key):
    view_counts = {}
    if data and key in data:
        for entry in data[key]:
            author = entry.get("string_map_data", {}).get("Author", {}).get("value")
            if author:
                view_counts[author] = view_counts.get(author, 0) + 1
    return view_counts

def process_data(root_dir):
    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    videos_watched_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")

    posts_viewed_data = {}
    videos_watched_data = {}

    try:
        if os.path.exists(posts_viewed_path):
            posts_viewed_data = load_json_data(posts_viewed_path)
        if os.path.exists(videos_watched_path):
            videos_watched_data = load_json_data(videos_watched_path)
    except (FileNotFoundError, ValueError) as e:
        print(e)

    post_views = count_views(posts_viewed_data, "impressions_history_posts_seen")
    video_views = count_views(videos_watched_data, "impressions_history_videos_watched")

    return post_views, video_views

def generate_csv(post_views, video_views):
    all_accounts = set(list(post_views.keys()) + list(video_views.keys()))
    data = [["Account", "Post Views", "Video Views"]]
    for account in all_accounts:
        post_view_count = post_views.get(account, 0)
        video_view_count = video_views.get(account, 0)
        data.append([account, post_view_count, video_view_count])

    with open('query_responses/results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    post_views, video_views = process_data(root_dir)
    generate_csv(post_views, video_views)

if __name__ == "__main__":
    main()