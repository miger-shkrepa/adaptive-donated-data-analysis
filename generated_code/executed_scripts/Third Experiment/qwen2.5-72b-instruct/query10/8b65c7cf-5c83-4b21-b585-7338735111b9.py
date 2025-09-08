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

def get_views_data():
    post_views = {}
    video_views = {}

    try:
        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        if os.path.exists(posts_viewed_path):
            posts_data = load_json_data(posts_viewed_path)
            for entry in posts_data["impressions_history_posts_seen"]:
                author = entry["string_map_data"]["Author"]["value"]
                if author in post_views:
                    post_views[author] += 1
                else:
                    post_views[author] = 1
        else:
            print("Warning: posts_viewed.json not found, treating post views as 0.")

        videos_watched_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")
        if os.path.exists(videos_watched_path):
            videos_data = load_json_data(videos_watched_path)
            for entry in videos_data["impressions_history_videos_watched"]:
                author = entry["string_map_data"]["Author"]["value"]
                if author in video_views:
                    video_views[author] += 1
                else:
                    video_views[author] = 1
        else:
            print("Warning: videos_watched.json not found, treating video views as 0.")
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

    return post_views, video_views

def write_to_csv(post_views, video_views):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Account', 'Post Views', 'Video Views']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            all_accounts = set(list(post_views.keys()) + list(video_views.keys()))
            for account in all_accounts:
                post_view_count = post_views.get(account, 0)
                video_view_count = video_views.get(account, 0)
                writer.writerow({'Account': account, 'Post Views': post_view_count, 'Video Views': video_view_count})
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

if __name__ == "__main__":
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    post_views, video_views = get_views_data()
    write_to_csv(post_views, video_views)