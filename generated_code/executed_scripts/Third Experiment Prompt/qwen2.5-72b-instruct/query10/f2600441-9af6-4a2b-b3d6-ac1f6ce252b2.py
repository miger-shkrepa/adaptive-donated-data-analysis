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

def process_ads_information(data_dir):
    posts_viewed = []
    videos_watched = []

    posts_viewed_path = os.path.join(data_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
    videos_watched_path = os.path.join(data_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')

    if os.path.exists(posts_viewed_path):
        posts_data = load_json(posts_viewed_path)
        posts_viewed = posts_data.get('impressions_history_posts_seen', [])
    
    if os.path.exists(videos_watched_path):
        videos_data = load_json(videos_watched_path)
        videos_watched = videos_data.get('impressions_history_videos_watched', [])
    
    return posts_viewed, videos_watched

def extract_views(posts_viewed, videos_watched):
    view_counts = {}
    
    for entry in posts_viewed + videos_watched:
        string_map_data = entry.get('string_map_data', {})
        author = string_map_data.get('Author', {}).get('value', 'Unknown')
        if author not in view_counts:
            view_counts[author] = {'Post Views': 0, 'Video Views': 0}
        view_counts[author]['Post Views'] += 1
    
    for entry in videos_watched:
        string_map_data = entry.get('string_map_data', {})
        author = string_map_data.get('Author', {}).get('value', 'Unknown')
        if author not in view_counts:
            view_counts[author] = {'Post Views': 0, 'Video Views': 0}
        view_counts[author]['Video Views'] += 1
    
    return view_counts

def write_to_csv(view_counts):
    csv_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for account, counts in view_counts.items():
            writer.writerow({
                'Account': account,
                'Post Views': counts['Post Views'],
                'Video Views': counts['Video Views']
            })

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    try:
        posts_viewed, videos_watched = process_ads_information(root_dir)
        view_counts = extract_views(posts_viewed, videos_watched)
        write_to_csv(view_counts)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()