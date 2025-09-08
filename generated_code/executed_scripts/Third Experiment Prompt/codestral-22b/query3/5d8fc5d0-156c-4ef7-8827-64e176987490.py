import os
import json
import csv
from datetime import datetime, timedelta
from collections import defaultdict

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

ads_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")

if not os.path.exists(ads_dir):
    print("Warning: The ads directory does not exist. Skipping this part of the analysis.")
    ads_data = defaultdict(int)
else:
    ads_data = defaultdict(int)
    for file_name in ["posts_viewed.json", "videos_watched.json"]:
        file_path = os.path.join(ads_dir, file_name)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                data = json.load(file)
                for item in data.get("structure", {}).get("impressions_history_posts_seen", []):
                    timestamp = item["string_map_data"]["Time"]["timestamp"]
                    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                    ads_data[date] += 1
        else:
            print(f"Warning: The file {file_name} does not exist. Skipping this file.")

weekly_data = defaultdict(int)
for date, count in ads_data.items():
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    week = date_obj.strftime('%Y-%W')
    weekly_data[week] += count

results = [["Date/Week", "Posts Viewed", "Type"]]
for date, count in ads_data.items():
    results.append([date, count, "Daily"])
for week, count in weekly_data.items():
    results.append([week, count, "Weekly"])

with open("query_responses/results.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(results)