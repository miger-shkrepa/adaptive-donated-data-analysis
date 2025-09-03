import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def extract_views(file_path):
    try:
        data = load_json(file_path)
        views = {}
        for entry in data.get('impressions_history_posts_seen', []):
            author = entry['string_map_data']['Author']['value']
            views[author] = views.get(author, 0) + 1
        return views
    except Exception as e:
        return {}

def extract_video_views(file_path):
    try:
        data = load_json(file_path)
        views = {}
        for entry in data.get('impressions_history_videos_watched', []):
            author = entry['string_map_data']['Author']['value']
            views[author] = views.get(author, 0) + 1
        return views
    except Exception as e:
        return {}

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
    videos_watched_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')

    post_views = extract_views(posts_viewed_path)
    video_views = extract_video_views(videos_watched_path)

    accounts = set(post_views.keys()).union(set(video_views.keys()))

    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account", "Post Views", "Video Views"])
        for account in accounts:
            writer.writerow([account, post_views.get(account, 0), video_views.get(account, 0)])

if __name__ == "__main__":
    main()