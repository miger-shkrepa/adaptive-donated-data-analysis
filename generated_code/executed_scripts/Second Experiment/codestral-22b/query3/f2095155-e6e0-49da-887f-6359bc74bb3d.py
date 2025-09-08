import os
import json
from datetime import datetime, timedelta
import csv

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
    # Open the posts_viewed.json file
    with open(posts_viewed_path, 'r') as f:
        # Load the JSON data
        posts_viewed_data = json.load(f)

        # Iterate over the impressions_history_posts_seen list
        for post in posts_viewed_data["impressions_history_posts_seen"]:
            # Extract the timestamp
            timestamp = post["string_map_data"]["Time"]["timestamp"]

            # Convert the timestamp to a datetime object
            date = datetime.fromtimestamp(timestamp)

            # Extract the daily and weekly data
            daily_data = [date.strftime('%Y-%m-%d'), 1, 'Daily']
            weekly_data = [f'Week {date.strftime("%Y-%W")}', 1, 'Weekly']

            # Append the data to the list
            data.append(daily_data)
            data.append(weekly_data)

# Define the path to the results.csv file
results_path = "query_responses/results.csv"

# Create the directory if it does not exist
os.makedirs(os.path.dirname(results_path), exist_ok=True)

# Write the data to the results.csv file
with open(results_path, 'w', newline='') as f:
    # Create a CSV writer object
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])

    # Write the data rows
    writer.writerows(data)