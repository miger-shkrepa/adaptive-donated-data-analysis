import os
import json
import csv
from datetime import datetime, timedelta

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the data
data = []

# Define the path to the posts_viewed.json file
posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

# Check if the posts_viewed.json file exists
if os.path.exists(posts_viewed_path):
    # Load the data from the posts_viewed.json file
    with open(posts_viewed_path, 'r') as f:
        posts_viewed_data = json.load(f)

    # Extract the timestamps from the posts_viewed_data
    timestamps = [item["string_map_data"]["Time"]["timestamp"] for item in posts_viewed_data["impressions_history_posts_seen"]]

    # Convert the timestamps to datetime objects
    dates = [datetime.fromtimestamp(timestamp) for timestamp in timestamps]

    # Calculate the daily and weekly counts
    daily_counts = {}
    weekly_counts = {}

    for date in dates:
        # Calculate the daily count
        daily_date = date.strftime('%Y-%m-%d')
        if daily_date in daily_counts:
            daily_counts[daily_date] += 1
        else:
            daily_counts[daily_date] = 1

        # Calculate the weekly count
        weekly_date = date.strftime('Week %Y-%W')
        if weekly_date in weekly_counts:
            weekly_counts[weekly_date] += 1
        else:
            weekly_counts[weekly_date] = 1

    # Append the daily counts to the data list
    for date, count in daily_counts.items():
        data.append([date, count, 'Daily'])

    # Append the weekly counts to the data list
    for date, count in weekly_counts.items():
        data.append([date, count, 'Weekly'])

# Define the path to the output CSV file
output_path = "query_responses/results.csv"

# Write the data to the output CSV file
with open(output_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
    writer.writerows(data)