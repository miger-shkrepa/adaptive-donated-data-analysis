import os
import csv
import json

root_dir = "root_dir"

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

def get_account_views(data):
    account_views = {}
    for entry in data:
        author = entry['string_map_data']['Author']['value']
        if author not in account_views:
            account_views[author] = 0
        account_views[author] += 1
    return account_views

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
    videos_watched_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')
    
    if not os.path.exists(posts_viewed_path):
        raise FileNotFoundError(f"FileNotFoundError: The file {posts_viewed_path} does not exist.")
    if not os.path.exists(videos_watched_path):
        raise FileNotFoundError(f"FileNotFoundError: The file {videos_watched_path} does not exist.")
    
    posts_data = read_json_file(posts_viewed_path)
    videos_data = read_json_file(videos_watched_path)
    
    posts_views = get_account_views(posts_data['impressions_history_posts_seen'])
    videos_views = get_account_views(videos_data['impressions_history_videos_watched'])
    
    all_accounts = set(posts_views.keys()).union(set(videos_views.keys()))
    
    results = []
    for account in all_accounts:
        post_views = posts_views.get(account, 0)
        video_views = videos_views.get(account, 0)
        results.append([account, post_views, video_views])
    
    results_dir = os.path.dirname('query_responses/results.csv')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Account', 'Post Views', 'Video Views'])
        csvwriter.writerows(results)

if __name__ == "__main__":
    main()