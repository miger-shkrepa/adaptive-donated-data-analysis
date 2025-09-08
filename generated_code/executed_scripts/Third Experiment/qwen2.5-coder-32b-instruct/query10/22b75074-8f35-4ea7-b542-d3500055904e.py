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
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        videos_watched_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')
        
        posts_viewed_data = read_json_file(posts_viewed_path) if os.path.exists(posts_viewed_path) else []
        videos_watched_data = read_json_file(videos_watched_path) if os.path.exists(videos_watched_path) else []
        
        posts_viewed_data = posts_viewed_data.get('impressions_history_posts_seen', [])
        videos_watched_data = videos_watched_data.get('impressions_history_videos_watched', [])
        
        posts_account_views = get_account_views(posts_viewed_data)
        videos_account_views = get_account_views(videos_watched_data)
        
        all_accounts = set(posts_account_views.keys()).union(set(videos_account_views.keys()))
        
        results = []
        for account in all_accounts:
            post_views = posts_account_views.get(account, 0)
            video_views = videos_account_views.get(account, 0)
            results.append([account, post_views, video_views])
        
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Account', 'Post Views', 'Video Views'])
            csvwriter.writerows(results)
    
    except Exception as e:
        print(e)
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Account', 'Post Views', 'Video Views'])

if __name__ == "__main__":
    main()