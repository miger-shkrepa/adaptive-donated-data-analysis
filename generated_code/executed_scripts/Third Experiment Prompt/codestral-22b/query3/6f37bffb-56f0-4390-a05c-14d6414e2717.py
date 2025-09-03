import os
import json
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the results list
results = [["Date/Week", "Posts Viewed", "Type"]]

# Define the paths to the JSON files
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")

# Process the liked posts
if os.path.exists(liked_posts_path):
    with open(liked_posts_path, "r") as f:
        liked_posts = json.load(f)

    # Initialize a dictionary to store the daily and weekly counts
    daily_counts = {}
    weekly_counts = {}

    # Iterate over the liked posts
    for post in liked_posts["likes_media_likes"]:
        for data in post["string_list_data"]:
            # Convert the timestamp to a datetime object
            dt = datetime.fromtimestamp(data["timestamp"])

            # Increment the daily count
            daily_key = dt.strftime("%Y-%m-%d")
            if daily_key not in daily_counts:
                daily_counts[daily_key] = 0
            daily_counts[daily_key] += 1

            # Increment the weekly count
            weekly_key = dt.strftime("%Y-%W")
            if weekly_key not in weekly_counts:
                weekly_counts[weekly_key] = 0
            weekly_counts[weekly_key] += 1

    # Add the daily counts to the results
    for date, count in daily_counts.items():
        results.append([date, count, "Daily"])

    # Add the weekly counts to the results
    for week, count in weekly_counts.items():
        results.append([week, count, "Weekly"])

# Process the saved posts
if os.path.exists(saved_posts_path):
    with open(saved_posts_path, "r") as f:
        saved_posts = json.load(f)

    # Initialize a dictionary to store the daily and weekly counts
    daily_counts = {}
    weekly_counts = {}

    # Iterate over the saved posts
    for post in saved_posts["saved_saved_media"]:
        for data in post["string_map_data"].values():
            # Convert the timestamp to a datetime object
            dt = datetime.fromtimestamp(data["timestamp"])

            # Increment the daily count
            daily_key = dt.strftime("%Y-%m-%d")
            if daily_key not in daily_counts:
                daily_counts[daily_key] = 0
            daily_counts[daily_key] += 1

            # Increment the weekly count
            weekly_key = dt.strftime("%Y-%W")
            if weekly_key not in weekly_counts:
                weekly_counts[weekly_key] = 0
            weekly_counts[weekly_key] += 1

    # Add the daily counts to the results
    for date, count in daily_counts.items():
        results.append([date, count, "Daily"])

    # Add the weekly counts to the results
    for week, count in weekly_counts.items():
        results.append([week, count, "Weekly"])

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(results)