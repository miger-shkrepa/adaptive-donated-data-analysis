import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def get_views_data(root_dir):
    posts_views = {}
    videos_views = {}

    ads_and_topics_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics')
    if not os.path.exists(ads_and_topics_path):
        return posts_views, videos_views

    posts_viewed_file = os.path.join(ads_and_topics_path, 'posts_viewed.json')
    videos_watched_file = os.path.join(ads_and_topics_path, 'videos_watched.json')

    if os.path.exists(posts_viewed_file):
        posts_data = load_json(posts_viewed_file)
        for entry in posts_data.get('impressions_history_posts_seen', []):
            author = entry.get('string_map_data', {}).get('Author', {}).get('value')
            if author:
                posts_views[author] = posts_views.get(author, 0) + 1

    if os.path.exists(videos_watched_file):
        videos_data = load_json(videos_watched_file)
        for entry in videos_data.get('impressions_history_videos_watched', []):
            author = entry.get('string_map_data', {}).get('Author', {}).get('value')
            if author:
                videos_views[author] = videos_views.get(author, 0) + 1

    return posts_views, videos_views

def write_csv(posts_views, videos_views):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        all_accounts = set(posts_views.keys()).union(videos_views.keys())
        for account in all_accounts:
            post_views = posts_views.get(account, 0)
            video_views = videos_views.get(account, 0)
            writer.writerow({'Account': account, 'Post Views': post_views, 'Video Views': video_views})

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    try:
        posts_views, videos_views = get_views_data(root_dir)
        write_csv(posts_views, videos_views)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()