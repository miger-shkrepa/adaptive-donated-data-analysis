import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the topics of interest
topics_of_interest = []

# Define the paths to the JSON files
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")

# Process the liked posts
if os.path.exists(liked_posts_path):
    with open(liked_posts_path, 'r') as f:
        data = json.load(f)
        for post in data["likes_media_likes"]:
            topics_of_interest.append(post["title"])

# Process the saved posts
if os.path.exists(saved_posts_path):
    with open(saved_posts_path, 'r') as f:
        data = json.load(f)
        for post in data["saved_saved_media"]:
            topics_of_interest.append(post["title"])

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Topics of Interest"])
    for topic in topics_of_interest:
        writer.writerow([topic])