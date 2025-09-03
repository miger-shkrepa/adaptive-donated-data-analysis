import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_posts_viewed(root_dir):
    posts_viewed = {}
    try:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename == "posts_viewed.json":
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for post in data["impressions_history_posts_seen"]:
                            timestamp = post["string_map_data"]["Time"]["timestamp"]
                            date = datetime.fromtimestamp(timestamp)
                            date_str = date.strftime("%Y-%m-%d")
                            if date_str not in posts_viewed:
                                posts_viewed[date_str] = 0
                            posts_viewed[date_str] += 1
    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    return posts_viewed

def get_weekly_posts_viewed(posts_viewed):
    weekly_posts_viewed = {}
    for date, count in posts_viewed.items():
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        week_str = date_obj.strftime("Week %Y-%W")
        if week_str not in weekly_posts_viewed:
            weekly_posts_viewed[week_str] = 0
        weekly_posts_viewed[week_str] += count
    return weekly_posts_viewed

def write_csv(posts_viewed, weekly_posts_viewed):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        for date, count in posts_viewed.items():
            writer.writerow([date, count, "Daily"])
        for week, count in weekly_posts_viewed.items():
            writer.writerow([week, count, "Weekly"])

def main():
    posts_viewed = get_posts_viewed(root_dir)
    weekly_posts_viewed = get_weekly_posts_viewed(posts_viewed)
    write_csv(posts_viewed, weekly_posts_viewed)

if __name__ == "__main__":
    main()