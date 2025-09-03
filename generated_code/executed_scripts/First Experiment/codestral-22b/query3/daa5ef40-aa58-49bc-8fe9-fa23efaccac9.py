import os
import json
from datetime import datetime, timedelta
import csv

# Declare the variable referring to the file input
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
    raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")

# Load the data from the posts_viewed.json file
with open(posts_viewed_file, 'r') as f:
    posts_viewed_data = json.load(f)

# Iterate over the impressions_history_posts_seen list
for post in posts_viewed_data["impressions_history_posts_seen"]:
    # Extract the timestamp
    timestamp = post["string_map_data"]["Time"]["timestamp"]
    # Convert the timestamp to a datetime object
    date = datetime.fromtimestamp(timestamp)
    # Extract the year, week, and day
    year, week, day = date.isocalendar()
    # Append the data to the list
    data.append([f"Week {year}-{week:02d}", 1, "Weekly"])
    data.append([date.strftime("%Y-%m-%d"), 1, "Daily"])

# Sort the data by date
data.sort(key=lambda x: x[0])

# Initialize an empty list to store the aggregated data
aggregated_data = []

# Initialize variables to store the current week and day
current_week = data[0][0]
current_day = data[0][0]
weekly_count = 0
daily_count = 0

# Iterate over the data
for row in data:
    # If the week is the same
    if row[0].startswith("Week") and row[0] == current_week:
        weekly_count += row[1]
    # If the week is different
    elif row[0].startswith("Week"):
        aggregated_data.append([current_week, weekly_count, "Weekly"])
        current_week = row[0]
        weekly_count = row[1]
    # If the day is the same
    elif row[0] == current_day:
        daily_count += row[1]
    # If the day is different
    else:
        aggregated_data.append([current_day, daily_count, "Daily"])
        current_day = row[0]
        daily_count = row[1]

# Append the last week and day
aggregated_data.append([current_week, weekly_count, "Weekly"])
aggregated_data.append([current_day, daily_count, "Daily"])

# Save the data to a CSV file
with open("query_responses/results.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Date/Week", "Posts Viewed", "Type"])
    writer.writerows(aggregated_data)