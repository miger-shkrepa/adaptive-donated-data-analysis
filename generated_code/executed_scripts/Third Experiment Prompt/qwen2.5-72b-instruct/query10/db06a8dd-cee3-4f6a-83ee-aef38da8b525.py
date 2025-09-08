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
    posts_views = 0
    videos_views = 0
    accounts = set()

    ads_and_topics_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics')
    if not os.path.exists(ads_and_topics_path):
        return posts_views, videos_views, accounts

    posts_viewed_file = os.path.join(ads_and_topics_path, 'posts_viewed.json')
    videos_watched_file = os.path.join(ads_and_topics_path, 'videos_watched.json')

    if os.path.exists(posts_viewed_file):
        posts_data = load_json(posts_viewed_file)
        posts_views = len(posts_data.get('impressions_history_posts_seen', []))
        for post in posts_data.get('impressions_history_posts_seen', []):
            author = post.get('string_map_data', {}).get('Author', {}).get('value')
            if author:
                accounts.add(author)

    if os.path.exists(videos_watched_file):
        videos_data = load_json(videos_watched_file)
        videos_views = len(videos_data.get('impressions_history_videos_watched', []))
        for video in videos_data.get('impressions_history_videos_watched', []):
            author = video.get('string_map_data', {}).get('Author', {}).get('value')
            if author:
                accounts.add(author)

    return posts_views, videos_views, accounts

def write_csv(posts_views, videos_views, accounts):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        if not accounts:
            return

        for account in accounts:
            writer.writerow({
                'Account': account,
                'Post Views': posts_views,
                'Video Views': videos_views
            })

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    try:
        posts_views, videos_views, accounts = get_views_data(root_dir)
        write_csv(posts_views, videos_views, accounts)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()