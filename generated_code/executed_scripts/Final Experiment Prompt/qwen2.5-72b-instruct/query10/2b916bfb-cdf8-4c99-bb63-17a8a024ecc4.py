import json
import os
import csv

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def count_views(data, key):
    view_counts = {}
    if key in data:
        for entry in data[key]:
            author = entry.get("string_map_data", {}).get("Author", {}).get("value")
            if author:
                view_counts[author] = view_counts.get(author, 0) + 1
    return view_counts

def process_data(posts_file, videos_file):
    post_views = {}
    video_views = {}

    if os.path.exists(posts_file):
        posts_data = load_json_data(posts_file)
        post_views = count_views(posts_data, "impressions_history_posts_seen")

    if os.path.exists(videos_file):
        videos_data = load_json_data(videos_file)
        video_views = count_views(videos_data, "impressions_history_videos_watched")

    return post_views, video_views

def generate_csv(post_views, video_views, output_path):
    all_accounts = set(list(post_views.keys()) + list(video_views.keys()))
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Account', 'Post Views', 'Video Views'])
        for account in all_accounts:
            post_count = post_views.get(account, 0)
            video_count = video_views.get(account, 0)
            csvwriter.writerow([account, post_count, video_count])

def main():
    posts_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    videos_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")
    output_path = 'query_responses/results.csv'

    try:
        post_views, video_views = process_data(posts_file, videos_file)
        generate_csv(post_views, video_views, output_path)
    except Exception as e:
        print(f"Error: {e}")
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Account', 'Post Views', 'Video Views'])

if __name__ == "__main__":
    main()