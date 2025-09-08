import os
import json
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

        # Iterate over ads_and_topics directory
        ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if os.path.exists(ads_and_topics_dir):
            for filename in os.listdir(ads_and_topics_dir):
                if filename == "posts_viewed.json":
                    posts_viewed_file = os.path.join(ads_and_topics_dir, filename)
                    with open(posts_viewed_file, "r") as file:
                        data = json.load(file)
                        for post in data["impressions_history_posts_seen"]:
                            time = post["string_map_data"]["Time"]["timestamp"]
                            date = datetime.fromtimestamp(time).strftime("%Y-%m-%d")
                            week = datetime.fromtimestamp(time).strftime("Week %Y-%W")

                            # Update daily posts viewed
                            if date in daily_posts_viewed:
                                daily_posts_viewed[date] += 1
                            else:
                                daily_posts_viewed[date] = 1

                            # Update weekly posts viewed
                            if week in weekly_posts_viewed:
                                weekly_posts_viewed[week] += 1
                            else:
                                weekly_posts_viewed[week] = 1

        # Write results to CSV file
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])

            # Write daily posts viewed
            for date, count in daily_posts_viewed.items():
                writer.writerow([date, count, "Daily"])

            # Write weekly posts viewed
            for week, count in weekly_posts_viewed.items():
                writer.writerow([week, count, "Weekly"])

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")

    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Error parsing JSON file: {e}")

    except Exception as e:
        raise ValueError(f"ValueError: An error occurred: {e}")

get_posts_viewed(root_dir)