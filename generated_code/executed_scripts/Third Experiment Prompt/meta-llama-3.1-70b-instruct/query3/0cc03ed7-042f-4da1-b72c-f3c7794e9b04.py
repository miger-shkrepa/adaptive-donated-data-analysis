import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_post_views(root_dir):
    post_views = {"daily": {}, "weekly": {}}
    try:
        instagram_activity_dir = os.path.join(root_dir, "your_instagram_activity")
        if not os.path.exists(instagram_activity_dir):
            raise FileNotFoundError("Error: The 'your_instagram_activity' directory does not exist.")

        likes_dir = os.path.join(instagram_activity_dir, "likes")
        if not os.path.exists(likes_dir):
            raise FileNotFoundError("Error: The 'likes' directory does not exist.")

        liked_posts_file = os.path.join(likes_dir, "liked_posts.json")
        if not os.path.exists(liked_posts_file):
            raise FileNotFoundError("Error: The 'liked_posts.json' file does not exist.")

        with open(liked_posts_file, "r") as f:
            liked_posts_data = json.load(f)

        for post in liked_posts_data["likes_media_likes"]:
            for like in post["string_list_data"]:
                timestamp = like["timestamp"]
                date = datetime.fromtimestamp(timestamp)
                week = date.strftime("%Y-%W")
                post_views["daily"][date.strftime("%Y-%m-%d")] = post_views["daily"].get(date.strftime("%Y-%m-%d"), 0) + 1
                post_views["weekly"][week] = post_views["weekly"].get(week, 0) + 1

    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise ValueError("Error: An unexpected error occurred - {}".format(str(e)))

    return post_views

def write_to_csv(post_views):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        for date, views in post_views["daily"].items():
            writer.writerow([date, views, "Daily"])
        for week, views in post_views["weekly"].items():
            writer.writerow([f"Week {week}", views, "Weekly"])

try:
    post_views = get_post_views(root_dir)
    write_to_csv(post_views)
except FileNotFoundError as e:
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date/Week", "Posts Viewed", "Type"])
    print(e)
except Exception as e:
    print(e)