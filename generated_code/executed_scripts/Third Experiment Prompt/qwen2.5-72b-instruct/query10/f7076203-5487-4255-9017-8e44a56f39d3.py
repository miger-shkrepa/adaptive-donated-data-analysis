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

    ads_and_topics_path = os.path.join(root_dir, "ads_information", "ads_and_topics")
    if os.path.exists(ads_and_topics_path):
        posts_viewed_path = os.path.join(ads_and_topics_path, "posts_viewed.json")
        videos_watched_path = os.path.join(ads_and_topics_path, "videos_watched.json")

        if os.path.exists(posts_viewed_path):
            posts_data = load_json(posts_viewed_path)
            posts_views = len(posts_data.get("impressions_history_posts_seen", []))

        if os.path.exists(videos_watched_path):
            videos_data = load_json(videos_watched_path)
            videos_views = len(videos_data.get("impressions_history_videos_watched", []))

        for file_path in [posts_viewed_path, videos_watched_path]:
            if os.path.exists(file_path):
                data = load_json(file_path)
                for entry in data.get("impressions_history_posts_seen", []) + data.get("impressions_history_videos_watched", []):
                    for string_map in entry.get("string_map_data", []):
                        author = string_map.get("Author", {}).get("value")
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
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        posts_views, videos_views, accounts = get_views_data(root_dir)
        write_csv(posts_views, videos_views, accounts)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()