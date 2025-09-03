import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def process_ads_information():
    post_views = 0
    video_views = 0
    accounts = set()

    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    posts_viewed_data = load_json(posts_viewed_path)
    if posts_viewed_data:
        for entry in posts_viewed_data.get("impressions_history_posts_seen", []):
            string_map = entry.get("string_map_data", {})
            author = string_map.get("Author", {}).get("value", "")
            if author:
                accounts.add(author)
                post_views += 1

    videos_watched_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")
    videos_watched_data = load_json(videos_watched_path)
    if videos_watched_data:
        for entry in videos_watched_data.get("impressions_history_videos_watched", []):
            string_map = entry.get("string_map_data", {})
            author = string_map.get("Author", {}).get("value", "")
            if author:
                accounts.add(author)
                video_views += 1

    return accounts, post_views, video_views

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        accounts, post_views, video_views = process_ads_information()

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account", "Post Views", "Video Views"])
            if accounts:
                for account in accounts:
                    writer.writerow([account, post_views, video_views])
            else:
                writer.writerow(["", 0, 0])

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()