import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_posts_viewed(root_dir):
    posts_viewed = {}
    try:
        ads_information_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        posts_viewed_file = os.path.join(ads_information_dir, "posts_viewed.json")
        if os.path.exists(posts_viewed_file):
            with open(posts_viewed_file, "r") as f:
                data = json.load(f)
                for post in data["impressions_history_posts_seen"]:
                    timestamp = post["string_map_data"]["Time"]["timestamp"]
                    date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
                    if date not in posts_viewed:
                        posts_viewed[date] = 0
                    posts_viewed[date] += 1
    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except Exception as e:
        raise ValueError("Error: " + str(e))
    return posts_viewed

def get_weekly_posts_viewed(posts_viewed):
    weekly_posts_viewed = {}
    for date, count in posts_viewed.items():
        week = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%W")
        if week not in weekly_posts_viewed:
            weekly_posts_viewed[week] = 0
        weekly_posts_viewed[week] += count
    return weekly_posts_viewed

def write_csv(posts_viewed, weekly_posts_viewed):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        for date, count in posts_viewed.items():
            writer.writerow([date, count, "Daily"])
        for week, count in weekly_posts_viewed.items():
            writer.writerow([f"Week {week}", count, "Weekly"])

def main():
    posts_viewed = get_posts_viewed(root_dir)
    weekly_posts_viewed = get_weekly_posts_viewed(posts_viewed)
    write_csv(posts_viewed, weekly_posts_viewed)

if __name__ == "__main__":
    main()