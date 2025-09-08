import os
import json
import csv
from datetime import datetime, timedelta
from collections import defaultdict

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize dictionaries to store daily and weekly post views
daily_post_views = defaultdict(int)
weekly_post_views = defaultdict(int)

# Traverse the directory structure
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                data = json.load(f)
                if "impressions_history_posts_seen" in data:
                    for post in data["impressions_history_posts_seen"]:
                        timestamp = post["string_map_data"]["Timestamp"]["value"]
                        date = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')
                        week = datetime.fromtimestamp(int(timestamp)).strftime('Week %Y-%W')
                        daily_post_views[date] += 1
                        weekly_post_views[week] += 1

# Create a CSV file with the results
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for date, views in daily_post_views.items():
        writer.writerow({'Date/Week': date, 'Posts Viewed': views, 'Type': 'Daily'})
    for week, views in weekly_post_views.items():
        writer.writerow({'Date/Week': week, 'Posts Viewed': views, 'Type': 'Weekly'})