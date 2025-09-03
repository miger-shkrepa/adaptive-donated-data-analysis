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
    for filename in os.listdir(ads_dir):
        if filename.endswith("_viewed.json"):
            filepath = os.path.join(ads_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    for post in data.get("impressions_history_ads_seen", []) + data.get("impressions_history_posts_seen", []) + data.get("impressions_history_videos_watched", []):
                        timestamp = post["string_map_data"]["Time"]["timestamp"]
                        date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                        week = datetime.fromtimestamp(timestamp).strftime('%Y-%W')
                        posts_viewed[date] += 1
                        posts_viewed[week] += 1
            except FileNotFoundError:
                continue
    return posts_viewed

def write_to_csv(posts_viewed):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key, value in posts_viewed.items():
            if '-' in key:
                writer.writerow({'Date/Week': key, 'Posts Viewed': value, 'Type': 'Daily'})
            else:
                writer.writerow({'Date/Week': key, 'Posts Viewed': value, 'Type': 'Weekly'})

posts_viewed = get_posts_viewed(root_dir)
write_to_csv(posts_viewed)