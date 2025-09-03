import os
import csv
import datetime
import json

root_dir = "root_dir"

def get_posts_viewed(root_dir):
    posts_viewed_daily = {}
    posts_viewed_weekly = {}

    ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
    if os.path.exists(ads_and_topics_dir):
        posts_viewed_file = os.path.join(ads_and_topics_dir, "posts_viewed.json")
        if os.path.exists(posts_viewed_file):
            with open(posts_viewed_file, "r") as f:
                data = json.load(f)
                for post in data["impressions_history_posts_seen"]:
                    timestamp = post["string_map_data"]["Time"]["timestamp"]
                    date = datetime.datetime.fromtimestamp(timestamp)
                    date_str = date.strftime("%Y-%m-%d")
                    posts_viewed_daily[date_str] = posts_viewed_daily.get(date_str, 0) + 1
                    week_str = date.strftime("Week %Y-%W")
                    posts_viewed_weekly[week_str] = posts_viewed_weekly.get(week_str, 0) + 1
        else:
            raise FileNotFoundError("FileNotFoundError: posts_viewed.json does not exist.")
    else:
        raise FileNotFoundError("FileNotFoundError: ads_information/ads_and_topics directory does not exist.")

    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        for date_str, count in posts_viewed_daily.items():
            writer.writerow([date_str, count, "Daily"])
        for week_str, count in posts_viewed_weekly.items():
            writer.writerow([week_str, count, "Weekly"])

try:
    get_posts_viewed(root_dir)
except FileNotFoundError as e:
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date/Week", "Posts Viewed", "Type"])
    print(e)
except Exception as e:
    print(f"Error: {e}")