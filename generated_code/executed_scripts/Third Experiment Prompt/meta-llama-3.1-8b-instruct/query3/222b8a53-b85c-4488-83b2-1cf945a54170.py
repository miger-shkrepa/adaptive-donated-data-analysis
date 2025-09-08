import os
import csv
import datetime
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the results list
results = []

# Iterate over the 'posts_viewed.json' files in the 'ads_and_topics' directory
for file in os.listdir(os.path.join(root_dir, "ads_information", "ads_and_topics")):
    if file == "posts_viewed.json":
        try:
            with open(os.path.join(root_dir, "ads_information", "ads_and_topics", file), 'r') as f:
                data = json.load(f)
                for item in data.get("structure", {}).get("impressions_history_posts_seen", []):
                    date = datetime.datetime.fromtimestamp(item.get("string_map_data", {}).get("Time", {}).get("timestamp", 0)).strftime('%Y-%m-%d')
                    results.append([date, 1, 'Daily'])
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON in {file}: {e}")

# Iterate over the 'posts' directory
for dir in os.listdir(os.path.join(root_dir, "media", "posts")):
    for file in os.listdir(os.path.join(root_dir, "media", "posts", dir)):
        if file == "image.jpg":
            date = datetime.datetime.strptime(dir, '%Y%m').strftime('%Y-%m-%d')
            results.append([date, 1, 'Daily'])

# Iterate over the 'stories' directory
for dir in os.listdir(os.path.join(root_dir, "media", "stories")):
    for file in os.listdir(os.path.join(root_dir, "media", "stories", dir)):
        if file == "image.jpg":
            date = datetime.datetime.strptime(dir, '%Y%m').strftime('%Y-%m-%d')
            results.append([date, 1, 'Daily'])

# Iterate over the 'posts_viewed.json' files in the 'ads_and_topics' directory
for file in os.listdir(os.path.join(root_dir, "ads_information", "ads_and_topics")):
    if file == "posts_viewed.json":
        try:
            with open(os.path.join(root_dir, "ads_information", "ads_and_topics", file), 'r') as f:
                data = json.load(f)
                for item in data.get("structure", {}).get("impressions_history_posts_seen", []):
                    date = datetime.datetime.fromtimestamp(item.get("string_map_data", {}).get("Time", {}).get("timestamp", 0)).strftime('%Y-%m')
                    week = datetime.datetime.fromtimestamp(item.get("string_map_data", {}).get("Time", {}).get("timestamp", 0)).strftime('%Y-%W')
                    results.append([week, 1, 'Weekly'])
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON in {file}: {e}")

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Date/Week", "Posts Viewed", "Type"])
    writer.writerows(results)