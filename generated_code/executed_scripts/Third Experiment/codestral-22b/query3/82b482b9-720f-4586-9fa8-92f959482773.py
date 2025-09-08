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
posts_viewed_file = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')

# Check if the posts_viewed.json file exists
if os.path.exists(posts_viewed_file):
    # Load the data from the posts_viewed.json file
    with open(posts_viewed_file, 'r') as f:
        data = json.load(f)

    # Extract the posts viewed data
    posts_viewed = data['impressions_history_posts_seen']

    # Initialize dictionaries to store daily and weekly counts
    daily_counts = {}
    weekly_counts = {}

    # Iterate over the posts viewed data
    for post in posts_viewed:
        # Extract the timestamp
        timestamp = post['string_map_data']['Time']['timestamp']

        # Convert the timestamp to a datetime object
        date = datetime.fromtimestamp(timestamp)

        # Extract the daily and weekly keys
        daily_key = date.strftime('%Y-%m-%d')
        weekly_key = date.strftime('Week %Y-%W')

        # Increment the daily count
        daily_counts[daily_key] = daily_counts.get(daily_key, 0) + 1

        # Increment the weekly count
        weekly_counts[weekly_key] = weekly_counts.get(weekly_key, 0) + 1

    # Convert the daily counts to a list of tuples
    daily_results = [(key, value, 'Daily') for key, value in daily_counts.items()]

    # Convert the weekly counts to a list of tuples
    weekly_results = [(key, value, 'Weekly') for key, value in weekly_counts.items()]

    # Combine the daily and weekly results
    results = daily_results + weekly_results

# Define the path to the output CSV file
output_file = 'query_responses/results.csv'

# Write the results to the output CSV file
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])

    # Write the results
    writer.writerows(results)