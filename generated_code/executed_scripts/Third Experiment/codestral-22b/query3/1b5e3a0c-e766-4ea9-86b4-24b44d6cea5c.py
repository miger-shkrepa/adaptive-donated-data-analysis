import os
import json
import csv
from datetime import datetime, timedelta

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the results
results = []

# Define the path to the posts_viewed.json file
posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

# Check if the posts_viewed.json file exists
if not os.path.exists(posts_viewed_file):
    # If the file does not exist, add a header row to the results list and skip the rest of the processing
    results.append(["Date/Week", "Posts Viewed", "Type"])
else:
    # Open the posts_viewed.json file and load its contents
    with open(posts_viewed_file, "r") as f:
        posts_viewed_data = json.load(f)

    # Extract the timestamps from the posts_viewed_data
    timestamps = [int(post["string_map_data"]["Time"]["timestamp"]) for post in posts_viewed_data["impressions_history_posts_seen"]]

    # Convert the timestamps to datetime objects
    dates = [datetime.fromtimestamp(timestamp) for timestamp in timestamps]

    # Initialize a dictionary to store the daily and weekly post counts
    daily_counts = {}
    weekly_counts = {}

    # Iterate over the dates and count the number of posts viewed per day and per week
    for date in dates:
        # Extract the date and week from the datetime object
        date_str = date.strftime("%Y-%m-%d")
        week_str = date.strftime("Week %Y-%W")

        # Increment the daily count for the current date
        if date_str in daily_counts:
            daily_counts[date_str] += 1
        else:
            daily_counts[date_str] = 1

        # Increment the weekly count for the current week
        if week_str in weekly_counts:
            weekly_counts[week_str] += 1
        else:
            weekly_counts[week_str] = 1

    # Add the daily counts to the results list
    for date_str, count in daily_counts.items():
        results.append([date_str, count, "Daily"])

    # Add the weekly counts to the results list
    for week_str, count in weekly_counts.items():
        results.append([week_str, count, "Weekly"])

# Save the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(results)