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

def process_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        return
    except json.JSONDecodeError:
        raise ValueError("ValueError: Invalid JSON file.")

    for item in data:
        if 'string_map_data' in item and 'Time' in item['string_map_data']:
            timestamp = item['string_map_data']['Time']['timestamp']
            date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            week = datetime.fromtimestamp(timestamp).strftime('%Y-%W')
            daily_posts[date] += 1
            weekly_posts[week] += 1

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file == 'posts_viewed.json':
            process_json_file(os.path.join(root, file))

results = []
for date, count in daily_posts.items():
    results.append([date, count, 'Daily'])
for week, count in weekly_posts.items():
    results.append([week, count, 'Weekly'])

results.sort(key=lambda x: x[0])

with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
    writer.writerows(results)