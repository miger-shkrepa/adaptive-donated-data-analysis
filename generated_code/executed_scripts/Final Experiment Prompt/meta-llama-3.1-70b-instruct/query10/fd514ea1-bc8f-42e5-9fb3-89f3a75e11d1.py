import os
import json
import csv

root_dir = "root_dir"

def get_views(root_dir):
    views = {}
    required_files = [
        os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json"),
        os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")
    ]

    for file_path in required_files:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"FileNotFoundError: The file '{file_path}' does not exist.")

    for file_path in required_files:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if file_path.endswith("posts_viewed.json"):
                views["Post Views"] = {}
                for post in data.get("impressions_history_posts_seen", []):
                    string_map_data = post.get("string_map_data", {})
                    author = string_map_data.get("Author", {}).get("value")
                    if author:
                        if author not in views["Post Views"]:
                            views["Post Views"][author] = 0
                        views["Post Views"][author] += 1
            elif file_path.endswith("videos_watched.json"):
                views["Video Views"] = {}
                for video in data.get("impressions_history_videos_watched", []):
                    string_map_data = video.get("string_map_data", {})
                    author = string_map_data.get("Author", {}).get("value")
                    if author:
                        if author not in views["Video Views"]:
                            views["Video Views"][author] = 0
                        views["Video Views"][author] += 1

    return views

def save_to_csv(views):
    with open("query_responses/results.csv", 'w', newline='') as csvfile:
        fieldnames = ["Account", "Post Views", "Video Views"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for account in set(list(views.get("Post Views", {}).keys()) + list(views.get("Video Views", {}).keys())):
            writer.writerow({
                "Account": account,
                "Post Views": views.get("Post Views", {}).get(account, 0),
                "Video Views": views.get("Video Views", {}).get(account, 0)
            })

try:
    views = get_views(root_dir)
    save_to_csv(views)
except FileNotFoundError as e:
    print(e)
    with open("query_responses/results.csv", 'w', newline='') as csvfile:
        fieldnames = ["Account", "Post Views", "Video Views"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()