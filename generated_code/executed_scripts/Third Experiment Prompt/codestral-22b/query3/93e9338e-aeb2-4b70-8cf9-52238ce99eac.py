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
    ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")

    for file_name in ["ads_viewed.json", "posts_viewed.json", "videos_watched.json"]:
        file_path = os.path.join(ads_and_topics_dir, file_name)
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
                for post in data.get("structure", {}).get("impressions_history_ads_seen", []):
                    timestamp = post["string_map_data"]["Time"]["timestamp"]
                    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                    week = datetime.fromtimestamp(timestamp).strftime('%Y-%W')
                    posts_viewed[(date, 'Daily')] += 1
                    posts_viewed[(week, 'Weekly')] += 1

    return posts_viewed

def save_to_csv(posts_viewed, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for (date_week, type), count in posts_viewed.items():
            writer.writerow({'Date/Week': date_week, 'Posts Viewed': count, 'Type': type})

posts_viewed = get_posts_viewed(root_dir)
save_to_csv(posts_viewed, 'query_responses/results.csv')