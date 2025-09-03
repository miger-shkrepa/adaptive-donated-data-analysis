import os
import json
import csv
from datetime import datetime, timedelta
from collections import defaultdict

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

daily_posts = defaultdict(int)
weekly_posts = defaultdict(int)

ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
posts_viewed_file = os.path.join(ads_and_topics_dir, "posts_viewed.json")

if os.path.exists(posts_viewed_file):
    with open(posts_viewed_file, "r") as f:
        data = json.load(f)
        for post in data["impressions_history_posts_seen"]:
            timestamp = post["string_map_data"]["Time"]["timestamp"]
            date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            week = datetime.fromtimestamp(timestamp).strftime('%Y-%W')
            daily_posts[date] += 1
            weekly_posts[week] += 1

results = []
for date, count in daily_posts.items():
    results.append([date, count, 'Daily'])
for week, count in weekly_posts.items():
    results.append([week, count, 'Weekly'])

results.sort(key=lambda x: x[0])

with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Date/Week", "Posts Viewed", "Type"])
    writer.writerows(results)