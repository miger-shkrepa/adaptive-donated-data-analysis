import csv
import os
import json
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the output CSV file
output_file = "query_responses/results.csv"

# Initialize the CSV writer
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Date/Week", "Posts Viewed", "Type"])

    # Iterate over the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".json"):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r') as file:
                        data = json.load(file)
                except json.JSONDecodeError:
                    print(f"Error: Failed to parse JSON file {filepath}")
                    continue

                # Check if the file contains the required structure
                if "ads_and_topics" in data and "ads_viewed.json" in data["ads_and_topics"]:
                    ads_viewed_data = data["ads_and_topics"]["ads_viewed.json"]["structure"]["impressions_history_ads_seen"]
                    posts_viewed_data = data["ads_and_topics"]["posts_viewed.json"]["structure"]["impressions_history_posts_seen"]
                    videos_watched_data = data["ads_and_topics"]["videos_watched.json"]["structure"]["impressions_history_videos_watched"]

                    # Calculate the total posts viewed
                    total_posts_viewed = len(ads_viewed_data) + len(posts_viewed_data) + len(videos_watched_data)

                    # Iterate over the data and write to the CSV file
                    for data in ads_viewed_data + posts_viewed_data + videos_watched_data:
                        timestamp = data["string_map_data"]["Time"]["timestamp"]
                        date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
                        week = datetime.fromtimestamp(timestamp).strftime("%Y-%W")
                        writer.writerow([date, 1, "Daily"])
                        writer.writerow([week, 1, "Weekly"])

                elif "ads_and_topics" in data and "posts_viewed.json" in data["ads_and_topics"]:
                    posts_viewed_data = data["ads_and_topics"]["posts_viewed.json"]["structure"]["impressions_history_posts_seen"]

                    # Calculate the total posts viewed
                    total_posts_viewed = len(posts_viewed_data)

                    # Iterate over the data and write to the CSV file
                    for data in posts_viewed_data:
                        timestamp = data["string_map_data"]["Time"]["timestamp"]
                        date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
                        week = datetime.fromtimestamp(timestamp).strftime("%Y-%W")
                        writer.writerow([date, 1, "Daily"])
                        writer.writerow([week, 1, "Weekly"])

                elif "ads_and_topics" in data and "videos_watched.json" in data["ads_and_topics"]:
                    videos_watched_data = data["ads_and_topics"]["videos_watched.json"]["structure"]["impressions_history_videos_watched"]

                    # Calculate the total posts viewed
                    total_posts_viewed = len(videos_watched_data)

                    # Iterate over the data and write to the CSV file
                    for data in videos_watched_data:
                        timestamp = data["string_map_data"]["Time"]["timestamp"]
                        date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
                        week = datetime.fromtimestamp(timestamp).strftime("%Y-%W")
                        writer.writerow([date, 1, "Daily"])
                        writer.writerow([week, 1, "Weekly"])

                else:
                    # If the file does not contain the required structure, treat its contribution as 0
                    writer.writerow(["", 0, ""])