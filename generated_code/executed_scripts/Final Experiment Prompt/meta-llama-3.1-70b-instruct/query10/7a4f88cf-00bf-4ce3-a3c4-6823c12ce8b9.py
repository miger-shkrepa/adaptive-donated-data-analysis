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
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                if file_path.endswith("posts_viewed.json"):
                    for post in data["impressions_history_posts_seen"]:
                        author = post["string_map_data"]["Author"]["value"]
                        if author not in views["Post Views"]:
                            views["Post Views"][author] = 0
                        views["Post Views"][author] += 1
                elif file_path.endswith("videos_watched.json"):
                    for video in data["impressions_history_videos_watched"]:
                        author = video["string_map_data"]["Author"]["value"]
                        if author not in views["Video Views"]:
                            views["Video Views"][author] = 0
                        views["Video Views"][author] += 1
        else:
            print(f"Warning: The file '{file_path}' does not exist. Treating its contribution as 0.")

    return views

def save_to_csv(views):
    with open("query_responses/results.csv", 'w', newline='') as csvfile:
        fieldnames = ["Account", "Post Views", "Video Views"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for author in set(list(views["Post Views"].keys()) + list(views["Video Views"].keys())):
            writer.writerow({
                "Account": author,
                "Post Views": views["Post Views"].get(author, 0),
                "Video Views": views["Video Views"].get(author, 0)
            })

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    views = get_views(root_dir)
    save_to_csv(views)
except FileNotFoundError as e:
    raise FileNotFoundError(f"Error: {e}")
except Exception as e:
    raise ValueError(f"Error: {e}")