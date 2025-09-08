import os
import json
import csv
from datetime import datetime, timedelta

# Declare the root directory variable
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the data
data = []

# Define the path to the liked_posts.json file
liked_posts_path = os.path.join(root_dir, "likes", "liked_posts.json")

# Check if the liked_posts.json file exists
if os.path.exists(liked_posts_path):
    # Load the JSON data from the file
    with open(liked_posts_path, "r") as f:
        liked_posts_data = json.load(f)

    # Extract the relevant data and calculate daily and weekly counts
    daily_counts = {}
    weekly_counts = {}

    for post in liked_posts_data["likes_media_likes"]:
        for item in post["string_list_data"]:
            timestamp = item["timestamp"]
            date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
            week = datetime.fromtimestamp(timestamp).strftime("Week %Y-%W")

            # Increment the daily count
            if date in daily_counts:
                daily_counts[date] += 1
            else:
                daily_counts[date] = 1

            # Increment the weekly count
            if week in weekly_counts:
                weekly_counts[week] += 1
            else:
                weekly_counts[week] = 1

    # Add the daily counts to the data list
    for date, count in daily_counts.items():
        data.append([date, count, "Daily"])

    # Add the weekly counts to the data list
    for week, count in weekly_counts.items():
        data.append([week, count, "Weekly"])

# Define the path to the output CSV file
output_path = "query_responses/results.csv"

# Write the data to the CSV file
with open(output_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Date/Week", "Posts Viewed", "Type"])
    writer.writerows(data)