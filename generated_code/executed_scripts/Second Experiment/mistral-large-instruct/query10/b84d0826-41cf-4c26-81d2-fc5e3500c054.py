import os
import json
import csv

def extract_views(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            views = {}
            for entry in data.get('impressions_history_posts_seen', []) + data.get('impressions_history_videos_watched', []):
                author = entry['string_map_data'].get('Author', {}).get('value', 'Unknown')
                if author not in views:
                    views[author] = {'Post Views': 0, 'Video Views': 0}
                if 'impressions_history_posts_seen' in file_path:
                    views[author]['Post Views'] += 1
                elif 'impressions_history_videos_watched' in file_path:
                    views[author]['Video Views'] += 1
            return views
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def main():
    root_dir = "root_dir"

    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
    videos_watched_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')

    views = {}

    try:
        posts_views = extract_views(posts_viewed_path)
        for account, data in posts_views.items():
            if account not in views:
                views[account] = {'Post Views': 0, 'Video Views': 0}
            views[account]['Post Views'] += data['Post Views']
    except FileNotFoundError:
        pass

    try:
        videos_views = extract_views(videos_watched_path)
        for account, data in videos_views.items():
            if account not in views:
                views[account] = {'Post Views': 0, 'Video Views': 0}
            views[account]['Video Views'] += data['Video Views']
    except FileNotFoundError:
        pass

    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, data in views.items():
            writer.writerow({'Account': account, 'Post Views': data['Post Views'], 'Video Views': data['Video Views']})

if __name__ == "__main__":
    main()