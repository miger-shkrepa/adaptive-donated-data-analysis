import os
import json
import csv
from datetime import datetime, timedelta
from collections import defaultdict

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

daily_counts = defaultdict(int)
weekly_counts = defaultdict(int)

def process_media_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            for item in data:
                if 'creation_timestamp' in item:
                    timestamp = item['creation_timestamp']
                    date = datetime.fromtimestamp(timestamp)
                    daily_counts[date.strftime('%Y-%m-%d')] += 1
                    weekly_counts[date.strftime('Week %Y-%W')] += 1
    except FileNotFoundError:
        pass

media_dirs = ['your_instagram_activity/media/posts_1.json', 'your_instagram_activity/media/reels.json', 'your_instagram_activity/media/stories.json']

for media_dir in media_dirs:
    process_media_file(os.path.join(root_dir, media_dir))

with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for date, count in daily_counts.items():
        writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})
    for week, count in weekly_counts.items():
        writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})