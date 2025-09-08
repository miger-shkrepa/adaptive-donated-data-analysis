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

def get_views(data, key):
    views = 0
    if key in data:
        for item in data[key]:
            views += len(item.get('string_map_data', {}).get('Author', {}).get('value', ''))
    return views

def process_directory(root_dir):
    post_views = 0
    video_views = 0
    accounts = set()

    ads_info_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics')
    if os.path.exists(ads_info_path):
        posts_viewed_path = os.path.join(ads_info_path, 'posts_viewed.json')
        if os.path.exists(posts_viewed_path):
            posts_data = load_json(posts_viewed_path)
            post_views += get_views(posts_data['impressions_history_posts_seen'], 'Author')
            for item in posts_data['impressions_history_posts_seen']:
                author = item.get('string_map_data', {}).get('Author', {}).get('value', '')
                if author:
                    accounts.add(author)

        videos_watched_path = os.path.join(ads_info_path, 'videos_watched.json')
        if os.path.exists(videos_watched_path):
            videos_data = load_json(videos_watched_path)
            video_views += get_views(videos_data['impressions_history_videos_watched'], 'Author')
            for item in videos_data['impressions_history_videos_watched']:
                author = item.get('string_map_data', {}).get('Author', {}).get('value', '')
                if author:
                    accounts.add(author)

    return accounts, post_views, video_views

def write_csv(accounts, post_views, video_views):
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        if not accounts:
            return
        for account in accounts:
            writer.writerow({'Account': account, 'Post Views': post_views, 'Video Views': video_views})

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    try:
        accounts, post_views, video_views = process_directory(root_dir)
        write_csv(accounts, post_views, video_views)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()