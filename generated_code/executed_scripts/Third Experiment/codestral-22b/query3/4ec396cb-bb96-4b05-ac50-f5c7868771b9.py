import os
import json
from datetime import datetime, timedelta
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("Error: The root directory does not exist.")

results = []

# Process liked posts
liked_posts_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
if os.path.exists(liked_posts_file):
    with open(liked_posts_file, "r") as f:
        liked_posts = json.load(f)

    for post in liked_posts["likes_media_likes"]:
        for like in post["string_list_data"]:
            timestamp = like["timestamp"]
            date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
            results.append([date, 1, "Daily"])

# Process saved posts
saved_posts_file = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")
if os.path.exists(saved_posts_file):
    with open(saved_posts_file, "r") as f:
        saved_posts = json.load(f)

    for post in saved_posts["saved_saved_media"]:
        timestamp = post["string_map_data"]["Saved on"]["timestamp"]
        date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
        results.append([date, 1, "Daily"])

# Calculate weekly counts
weekly_counts = {}
for result in results:
    date = datetime.strptime(result[0], "%Y-%m-%d")
    week = date.strftime("%Y-%W")
    if week not in weekly_counts:
        weekly_counts[week] = 0
    weekly_counts[week] += 1

# Add weekly counts to results
for week, count in weekly_counts.items():
    results.append([week, count, "Weekly"])

# Save results to CSV file
output_file = "query_responses/results.csv"
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Date/Week", "Posts Viewed", "Type"])
    writer.writerows(results)