import os
import json
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("Error: The root directory does not exist.")

posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

if not os.path.exists(posts_viewed_file):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date/Week", "Posts Viewed", "Type"])
    raise FileNotFoundError("Error: The posts_viewed.json file does not exist.")

with open(posts_viewed_file, 'r') as f:
    data = json.load(f)

posts_viewed = data["impressions_history_posts_seen"]

daily_posts = {}
weekly_posts = {}

for post in posts_viewed:
    timestamp = post["string_map_data"]["Time"]["timestamp"]
    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    week = datetime.fromtimestamp(timestamp).strftime('Week %Y-%W')

    if date in daily_posts:
        daily_posts[date] += 1
    else:
        daily_posts[date] = 1

    if week in weekly_posts:
        weekly_posts[week] += 1
    else:
        weekly_posts[week] = 1

with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Date/Week", "Posts Viewed", "Type"])

    for date, count in daily_posts.items():
        writer.writerow([date, count, "Daily"])

    for week, count in weekly_posts.items():
        writer.writerow([week, count, "Weekly"])