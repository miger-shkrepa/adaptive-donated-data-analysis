import os
import csv

root_dir = "root_dir"

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return eval(file.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: Error reading the file {file_path}. {str(e)}")

def get_account_views(data, key):
    views = {}
    if key in data:
        for entry in data[key]:
            author = entry['string_map_data']['Author']['value']
            if author not in views:
                views[author] = 0
            views[author] += 1
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
        
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account', 'Post Views', 'Video Views'])
            for account in all_accounts:
                post_views = posts_views.get(account, 0)
                video_views = videos_views.get(account, 0)
                writer.writerow([account, post_views, video_views])
    
    except Exception as e:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account', 'Post Views', 'Video Views'])

if __name__ == "__main__":
    main()