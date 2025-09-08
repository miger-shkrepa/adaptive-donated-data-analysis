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
    for filename in ["ads_viewed.json", "posts_viewed.json", "videos_watched.json"]:
        filepath = os.path.join(ads_and_topics_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                data = json.load(f)
                for key in data.keys():
                    if key.endswith("_seen"):
                        for post in data[key]:
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

def write_to_csv(data, output_file):
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        for date_week, counts in data.items():
            writer.writerow([date_week, counts["Daily"], "Daily"])
            writer.writerow([date_week, counts["Weekly"], "Weekly"])

try:
    posts_viewed = get_posts_viewed(root_dir)
    write_to_csv(posts_viewed, output_file)
except Exception as e:
    print(f"Error: {str(e)}")