import os
import json
import csv

root_dir = "root_dir"

def get_views(root_dir):
    views = {"Post Views": {}, "Video Views": {}}
    required_files = [
        os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json"),
        os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")
    ]

    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"Warning: The file {file_path} does not exist. Skipping...")
            if file_path.endswith("posts_viewed.json"):
                views["Post Views"] = {}
            elif file_path.endswith("videos_watched.json"):
                views["Video Views"] = {}
        else:
            with open(file_path, "r") as file:
                data = json.load(file)
                if file_path.endswith("posts_viewed.json"):
                    for entry in data["impressions_history_posts_seen"]:
                        author = entry["string_map_data"]["Author"]["value"]
                        if author not in views["Post Views"]:
                            views["Post Views"][author] = 0
                        views["Post Views"][author] += 1
                elif file_path.endswith("videos_watched.json"):
                    for entry in data["impressions_history_videos_watched"]:
                        author = entry["string_map_data"]["Author"]["value"]
                        if author not in views["Video Views"]:
                            views["Video Views"][author] = 0
                        views["Video Views"][author] += 1

    return views

def save_to_csv(views):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account", "Post Views", "Video Views"])
        for author in set(list(views.get("Post Views", {}).keys()) + list(views.get("Video Views", {}).keys())):
            post_views = views.get("Post Views", {}).get(author, 0)
            video_views = views.get("Video Views", {}).get(author, 0)
            writer.writerow([author, post_views, video_views])

try:
    views = get_views(root_dir)
    save_to_csv(views)
except Exception as e:
    raise Exception(f"Error: {str(e)}")