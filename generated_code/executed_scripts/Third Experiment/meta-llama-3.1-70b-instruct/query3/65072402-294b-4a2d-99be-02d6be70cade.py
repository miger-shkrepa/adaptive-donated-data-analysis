import os
import csv
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
                    # Parse posts_viewed.json file
                    with open(posts_viewed_file, "r") as file:
                        # Assuming the file contains a list of dictionaries with "Time" and "Author" keys
                        import json
                        data = json.load(file)
                        for post in data["impressions_history_posts_seen"]:
                            timestamp = post["string_map_data"]["Time"]["timestamp"]
                            date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
                            week = datetime.fromtimestamp(timestamp).strftime("Week %Y-%W")
                            if date not in daily_posts_viewed:
                                daily_posts_viewed[date] = 1
                            else:
                                daily_posts_viewed[date] += 1
                            if week not in weekly_posts_viewed:
                                weekly_posts_viewed[week] = 1
                            else:
                                weekly_posts_viewed[week] += 1

        # Write results to CSV file
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            fieldnames = ["Date/Week", "Posts Viewed", "Type"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for date, count in daily_posts_viewed.items():
                writer.writerow({"Date/Week": date, "Posts Viewed": count, "Type": "Daily"})
            for week, count in weekly_posts_viewed.items():
                writer.writerow({"Date/Week": week, "Posts Viewed": count, "Type": "Weekly"})

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

get_posts_viewed(root_dir)