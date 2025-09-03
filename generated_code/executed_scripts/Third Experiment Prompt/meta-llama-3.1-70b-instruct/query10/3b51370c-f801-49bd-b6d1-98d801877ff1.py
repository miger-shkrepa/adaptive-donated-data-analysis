import os
import json
import csv

root_dir = "root_dir"

def get_views(root_dir):
    views = {}
    try:
        ads_info_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        posts_viewed_file = os.path.join(ads_info_dir, "posts_viewed.json")
        videos_watched_file = os.path.join(ads_info_dir, "videos_watched.json")

        if os.path.exists(posts_viewed_file):
            with open(posts_viewed_file, "r") as f:
                posts_viewed_data = json.load(f)
                for post in posts_viewed_data["impressions_history_posts_seen"]:
                    author = post["string_map_data"]["Author"]["value"]
                    if author not in views:
                        views[author] = {"post_views": 0, "video_views": 0}
                    views[author]["post_views"] += 1

        if os.path.exists(videos_watched_file):
            with open(videos_watched_file, "r") as f:
                videos_watched_data = json.load(f)
                for video in videos_watched_data["impressions_history_videos_watched"]:
                    author = video["string_map_data"]["Author"]["value"]
                    if author not in views:
                        views[author] = {"post_views": 0, "video_views": 0}
                    views[author]["video_views"] += 1

    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory or required files do not exist.")

    return views

def save_to_csv(views):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        fieldnames = ["Account", "Post Views", "Video Views"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for account, view_counts in views.items():
            writer.writerow({"Account": account, "Post Views": view_counts["post_views"], "Video Views": view_counts["video_views"]})

def main():
    views = get_views(root_dir)
    save_to_csv(views)

if __name__ == "__main__":
    main()