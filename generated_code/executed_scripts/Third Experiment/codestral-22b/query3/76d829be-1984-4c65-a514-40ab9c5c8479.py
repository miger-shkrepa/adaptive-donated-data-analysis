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
posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

# Check if the posts_viewed.json file exists
if not os.path.exists(posts_viewed_file):
    # If the file does not exist, create a CSV file with only the column headers
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
else:
    # If the file exists, open it and load the data
    with open(posts_viewed_file, 'r') as f:
        posts_viewed_data = json.load(f)

    # Extract the relevant data from the posts_viewed_data
    for post in posts_viewed_data['impressions_history_posts_seen']:
        timestamp = post['string_map_data']['Time']['timestamp']
        date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        data.append([date, 1, 'Daily'])

    # Calculate the weekly data
    weekly_data = {}
    for item in data:
        week = datetime.strptime(item[0], '%Y-%m-%d').strftime('Week %Y-%W')
        if week in weekly_data:
            weekly_data[week] += 1
        else:
            weekly_data[week] = 1

    # Add the weekly data to the data list
    for week, count in weekly_data.items():
        data.append([week, count, 'Weekly'])

    # Write the data to a CSV file
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
        writer.writerows(data)