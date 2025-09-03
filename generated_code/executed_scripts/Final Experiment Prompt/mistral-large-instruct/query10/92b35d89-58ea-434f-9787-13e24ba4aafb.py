import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON.")

def count_views(data, key):
    count = {}
    try:
        for entry in data.get(key, []):
            author = entry.get("string_map_data", {}).get("Author", {}).get("value")
            if author:
                count[author] = count.get(author, 0) + 1
    except (TypeError, AttributeError) as e:
        raise ValueError(f"Error: ValueError: Invalid data structure in {key}: {e}")
    return count

def main():
    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    videos_watched_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")

    try:
        posts_data = load_json(posts_viewed_path)
        post_views = count_views(posts_data, "impressions_history_posts_seen")
    except FileNotFoundError:
        post_views = {}

    try:
        videos_data = load_json(videos_watched_path)
        video_views = count_views(videos_data, "impressions_history_videos_watched")
    except FileNotFoundError:
        video_views = {}

    accounts = set(post_views.keys()).union(set(video_views.keys()))

    results = []
    for account in accounts:
        results.append({
            "Account": account,
            "Post Views": post_views.get(account, 0),
            "Video Views": video_views.get(account, 0)
        })

    output_path = "query_responses/results.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ["Account", "Post Views", "Video Views"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    main()