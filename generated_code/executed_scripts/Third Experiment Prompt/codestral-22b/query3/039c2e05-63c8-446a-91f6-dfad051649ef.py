import os
import json
import csv
from datetime import datetime, timedelta
from collections import defaultdict

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

def get_posts_viewed(root_dir):
    posts_viewed = defaultdict(int)
    ads_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
    posts_file = os.path.join(ads_dir, "posts_viewed.json")

    if not os.path.exists(posts_file):
        return posts_viewed

    with open(posts_file, "r") as f:
        data = json.load(f)

    for post in data.get("impressions_history_posts_seen", []):
        timestamp = post["string_map_data"].get("Time", {}).get("timestamp", 0)
        if timestamp:
            date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            week = datetime.fromtimestamp(timestamp).strftime('%Y-%W')
            posts_viewed[date] += 1
            posts_viewed[week] += 1

    return posts_viewed

def write_to_csv(posts_viewed):
    with open("query_responses/results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        for date_week, count in posts_viewed.items():
            if "-" in date_week:
                writer.writerow([date_week, count, "Daily"])
            else:
                writer.writerow([date_week, count, "Weekly"])

posts_viewed = get_posts_viewed(root_dir)
write_to_csv(posts_viewed)