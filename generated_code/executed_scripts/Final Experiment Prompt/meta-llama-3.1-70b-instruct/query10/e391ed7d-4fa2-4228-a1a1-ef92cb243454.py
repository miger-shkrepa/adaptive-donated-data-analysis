import os
import json
import csv

root_dir = "root_dir"

def get_views(root_dir):
    views = {"Post Views": {}, "Video Views": {}}
    required_files = [
        ("posts_viewed.json", "impressions_history_posts_seen", "Post Views"),
        ("videos_watched.json", "impressions_history_videos_watched", "Video Views")
    ]

    for file_name, key, view_type in required_files:
        file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", file_name)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                data = json.load(file)
                for entry in data[key]:
                    author = entry["string_map_data"]["Author"]["value"]
                    if author not in views[view_type]:
                        views[view_type][author] = 0
                    views[view_type][author] += 1

    return views

def save_to_csv(views):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account", "Post Views", "Video Views"])
        for author in set(list(views["Post Views"].keys()) + list(views["Video Views"].keys())):
            post_views = views["Post Views"].get(author, 0)
            video_views = views["Video Views"].get(author, 0)
            writer.writerow([author, post_views, video_views])

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    views = get_views(root_dir)
    save_to_csv(views)
except FileNotFoundError as e:
    print(e)
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account", "Post Views", "Video Views"])