import os
import json
import csv

root_dir = "root_dir"

def get_views(root_dir):
    views = {}
    try:
        # Get post views
        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        if os.path.exists(posts_viewed_path):
            with open(posts_viewed_path, "r") as f:
                data = json.load(f)
                for post in data["impressions_history_posts_seen"]:
                    author = post["string_map_data"]["Author"]["value"]
                    if author not in views:
                        views[author] = {"Post Views": 0, "Video Views": 0}
                    views[author]["Post Views"] += 1
        else:
            raise FileNotFoundError("Error: posts_viewed.json file not found.")

        # Get video views
        videos_watched_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")
        if os.path.exists(videos_watched_path):
            with open(videos_watched_path, "r") as f:
                data = json.load(f)
                for video in data["impressions_history_videos_watched"]:
                    author = video["string_map_data"]["Author"]["value"]
                    if author not in views:
                        views[author] = {"Post Views": 0, "Video Views": 0}
                    views[author]["Video Views"] += 1
        else:
            raise FileNotFoundError("Error: videos_watched.json file not found.")

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")

    return views

def write_to_csv(views):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        fieldnames = ["Account", "Post Views", "Video Views"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, view_counts in views.items():
            writer.writerow({"Account": account, "Post Views": view_counts["Post Views"], "Video Views": view_counts["Video Views"]})

def main():
    try:
        views = get_views(root_dir)
        write_to_csv(views)
    except FileNotFoundError as e:
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            fieldnames = ["Account", "Post Views", "Video Views"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

if __name__ == "__main__":
    main()