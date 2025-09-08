import os
import json
import csv

root_dir = "root_dir"

def get_views(root_dir):
    views = {}
    try:
        ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if not os.path.exists(ads_and_topics_dir):
            raise FileNotFoundError("Error: The ads_and_topics directory does not exist.")

        posts_viewed_file = os.path.join(ads_and_topics_dir, "posts_viewed.json")
        if not os.path.exists(posts_viewed_file):
            posts_viewed_data = []
        else:
            with open(posts_viewed_file, "r") as f:
                posts_viewed_data = json.load(f)["impressions_history_posts_seen"]

        videos_watched_file = os.path.join(ads_and_topics_dir, "videos_watched.json")
        if not os.path.exists(videos_watched_file):
            videos_watched_data = []
        else:
            with open(videos_watched_file, "r") as f:
                videos_watched_data = json.load(f)["impressions_history_videos_watched"]

        for post in posts_viewed_data:
            author = post["string_map_data"]["Author"]["value"]
            if author not in views:
                views[author] = {"post_views": 0, "video_views": 0}
            views[author]["post_views"] += 1

        for video in videos_watched_data:
            author = video["string_map_data"]["Author"]["value"]
            if author not in views:
                views[author] = {"post_views": 0, "video_views": 0}
            views[author]["video_views"] += 1

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")

    return views

def write_csv(views):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        fieldnames = ["Account", "Post Views", "Video Views"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for account, views_data in views.items():
            writer.writerow({"Account": account, "Post Views": views_data["post_views"], "Video Views": views_data["video_views"]})

def main():
    try:
        views = get_views(root_dir)
        write_csv(views)
    except FileNotFoundError as e:
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            fieldnames = ["Account", "Post Views", "Video Views"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

if __name__ == "__main__":
    main()