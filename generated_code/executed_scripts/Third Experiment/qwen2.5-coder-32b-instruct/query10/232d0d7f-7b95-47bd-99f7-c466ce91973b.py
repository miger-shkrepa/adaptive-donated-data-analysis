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

def get_account_views(data, key):
    views = {}
    if data and key in data:
        for entry in data[key]:
            author = entry['string_map_data']['Author']['value']
            views[author] = views.get(author, 0) + 1
    return views

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        videos_watched_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')
        
        posts_data = read_json_file(posts_viewed_path) if os.path.exists(posts_viewed_path) else {}
        videos_data = read_json_file(videos_watched_path) if os.path.exists(videos_watched_path) else {}
        
        posts_views = get_account_views(posts_data, 'impressions_history_posts_seen')
        videos_views = get_account_views(videos_data, 'impressions_history_videos_watched')
        
        all_accounts = set(posts_views.keys()).union(set(videos_views.keys()))
        
        results = []
        for account in all_accounts:
            post_views = posts_views.get(account, 0)
            video_views = videos_views.get(account, 0)
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