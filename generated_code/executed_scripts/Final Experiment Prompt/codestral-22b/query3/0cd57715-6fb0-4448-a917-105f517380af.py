import os
import json
from datetime import datetime
import csv

# Declare the root directory
root_dir = "root_dir"

# Define the path to the JSON file
json_file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

# Initialize an empty dictionary to store the results
results = {}

# Check if the JSON file exists
if not os.path.exists(json_file_path):
    raise FileNotFoundError("FileNotFoundError: The JSON file does not exist.")

# Open the JSON file
with open(json_file_path, 'r') as f:
    data = json.load(f)

# Iterate over the posts seen
for post in data.get("impressions_history_posts_seen", []):
    # Extract the timestamp
    timestamp = post["string_map_data"]["Time"]["timestamp"]

    # Convert the timestamp to a datetime object
    dt = datetime.fromtimestamp(timestamp)

    # Extract the date and week
    date = dt.strftime('%Y-%m-%d')
    week = dt.strftime('Week %Y-%W')

    # Update the results dictionary
    if date not in results:
        results[date] = {"Daily": 1, "Weekly": 0}
    else:
        results[date]["Daily"] += 1

    if week not in results:
        results[week] = {"Daily": 0, "Weekly": 1}
    else:
        results[week]["Weekly"] += 1

# Write the results to a CSV file
with open("query_responses/results.csv", 'w', newline='') as f:
    writer = csv.writer(f)

    # Write the header
    writer.writerow(["Date/Week", "Posts Viewed", "Type"])

    # Write the results
    for date_week, counts in results.items():
        writer.writerow([date_week, counts["Daily"], "Daily"])
        writer.writerow([date_week, counts["Weekly"], "Weekly"])