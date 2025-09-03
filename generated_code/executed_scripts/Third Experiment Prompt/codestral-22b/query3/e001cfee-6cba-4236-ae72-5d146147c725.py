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
    ads_info_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
    posts_viewed_file = os.path.join(ads_info_dir, "posts_viewed.json")

    if not os.path.exists(posts_viewed_file):
        return posts_viewed

    with open(posts_viewed_file, 'r') as f:
        data = json.load(f)

    for post in data.get("impressions_history_posts_seen", []):
        timestamp = post["string_map_data"]["Time"]["timestamp"]
        date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        posts_viewed[date] += 1

    return posts_viewed

def aggregate_posts_viewed(posts_viewed):
    weekly_posts_viewed = defaultdict(int)
    for date, count in posts_viewed.items():
        week = datetime.strptime(date, '%Y-%m-%d').strftime('Week %Y-%W')
        weekly_posts_viewed[week] += count

    return posts_viewed, weekly_posts_viewed

def save_to_csv(daily_posts_viewed, weekly_posts_viewed):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for date, count in daily_posts_viewed.items():
            writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})
        for week, count in weekly_posts_viewed.items():
            writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

posts_viewed = get_posts_viewed(root_dir)
daily_posts_viewed, weekly_posts_viewed = aggregate_posts_viewed(posts_viewed)
save_to_csv(daily_posts_viewed, weekly_posts_viewed)