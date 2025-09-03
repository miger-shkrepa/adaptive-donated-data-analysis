import os
import csv
import json
from datetime import datetime

root_dir = "root_dir"

def get_posts_viewed(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize variables to store posts viewed
        daily_posts_viewed = {}
        weekly_posts_viewed = {}

        # Iterate over ads_information directory
        ads_info_dir = os.path.join(root_dir, "ads_information")
        if os.path.exists(ads_info_dir):
            ads_and_topics_dir = os.path.join(ads_info_dir, "ads_and_topics")
            if os.path.exists(ads_and_topics_dir):
                posts_viewed_file = os.path.join(ads_and_topics_dir, "posts_viewed.json")
                if os.path.exists(posts_viewed_file):
                    with open(posts_viewed_file, "r") as file:
                        data = json.load(file)
                        for post in data["impressions_history_posts_seen"]:
                            timestamp = post["string_map_data"]["Time"]["timestamp"]
                            date = datetime.fromtimestamp(timestamp / 1000).date()
                            week = date.isocalendar()[0:2]
                            if date not in daily_posts_viewed:
                                daily_posts_viewed[date] = 1
                            else:
                                daily_posts_viewed[date] += 1
                            week_key = f"Week {week[0]}-{week[1]:02d}"
                            if week_key not in weekly_posts_viewed:
                                weekly_posts_viewed[week_key] = 1
                            else:
                                weekly_posts_viewed[week_key] += 1

        # Create CSV file
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            fieldnames = ["Date/Week", "Posts Viewed", "Type"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for date, count in daily_posts_viewed.items():
                writer.writerow({"Date/Week": date.strftime("%Y-%m-%d"), "Posts Viewed": count, "Type": "Daily"})
            for week, count in weekly_posts_viewed.items():
                writer.writerow({"Date/Week": week, "Posts Viewed": count, "Type": "Weekly"})

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: {e}")
    except Exception as e:
        raise Exception(f"Error: {e}")

get_posts_viewed(root_dir)