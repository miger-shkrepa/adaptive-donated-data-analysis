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
    if os.path.exists(ads_and_topics_path):
        posts_viewed_path = os.path.join(ads_and_topics_path, 'posts_viewed.json')
        if os.path.exists(posts_viewed_path):
            posts_viewed_data = load_json(posts_viewed_path)
            posts_views = len(posts_viewed_data['impressions_history_posts_seen'])

        videos_watched_path = os.path.join(ads_and_topics_path, 'videos_watched.json')
        if os.path.exists(videos_watched_path):
            videos_watched_data = load_json(videos_watched_path)
            videos_views = len(videos_watched_data['impressions_history_videos_watched'])

    followers_and_following_path = os.path.join(root_dir, 'connections', 'followers_and_following')
    if os.path.exists(followers_and_following_path):
        followers_path = os.path.join(followers_and_following_path, 'followers_1.json')
        if os.path.exists(followers_path):
            followers_data = load_json(followers_path)
            for entry in followers_data:
                for string_data in entry['string_list_data']:
                    accounts.add(string_data['value'])

        following_path = os.path.join(followers_and_following_path, 'following.json')
        if os.path.exists(following_path):
            following_data = load_json(following_path)
            for entry in following_data['relationships_following']:
                for string_data in entry['string_list_data']:
                    accounts.add(string_data['value'])

    return accounts, posts_views, videos_views

def write_csv(accounts, posts_views, videos_views):
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
        accounts, posts_views, videos_views = get_views_data(root_dir)
        write_csv(accounts, posts_views, videos_views)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()