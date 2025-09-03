import os
import json
import csv

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def process_data():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        videos_watched_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")

        posts_data = load_json_data(posts_viewed_path) if os.path.exists(posts_viewed_path) else {"impressions_history_posts_seen": []}
        videos_data = load_json_data(videos_watched_path) if os.path.exists(videos_watched_path) else {"impressions_history_videos_watched": []}

        account_views = {}
        for entry in posts_data["impressions_history_posts_seen"] + videos_data["impressions_history_videos_watched"]:
            for data in entry["string_map_data"]:
                if "Author" in data:
                    author = data["Author"]["value"]
                    if author not in account_views:
                        account_views[author] = {"Post Views": 0, "Video Views": 0}
                    if entry in posts_data["impressions_history_posts_seen"]:
                        account_views[author]["Post Views"] += 1
                    else:
                        account_views[author]["Video Views"] += 1

        return account_views

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

def save_to_csv(data):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, views in data.items():
            writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})

if __name__ == "__main__":
    try:
        processed_data = process_data()
        save_to_csv(processed_data)
    except Exception as e:
        print(f"An error occurred: {e}")