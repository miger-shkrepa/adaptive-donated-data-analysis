import os
import json
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"
output_file = "query_responses/results.csv"

def get_posts_viewed(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    posts_viewed = {}

    ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
    for filename in ["posts_viewed.json", "videos_watched.json"]:
        filepath = os.path.join(ads_and_topics_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                data = json.load(f)
                for post in data.get("structure", {}).get("impressions_history_posts_seen", []):
                    timestamp = post["string_map_data"]["Time"]["timestamp"]
                    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                    week = datetime.fromtimestamp(timestamp).strftime('%Y-%W')

                    if date not in posts_viewed:
                        posts_viewed[date] = {"Daily": 0, "Weekly": 0}
                    posts_viewed[date]["Daily"] += 1

                    if week not in posts_viewed:
                        posts_viewed[week] = {"Daily": 0, "Weekly": 0}
                    posts_viewed[week]["Weekly"] += 1

    return posts_viewed

def save_to_csv(posts_viewed, output_file):
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        for date_week, counts in posts_viewed.items():
            writer.writerow([date_week, counts["Daily"], "Daily"])
            writer.writerow([date_week, counts["Weekly"], "Weekly"])

posts_viewed = get_posts_viewed(root_dir)
save_to_csv(posts_viewed, output_file)