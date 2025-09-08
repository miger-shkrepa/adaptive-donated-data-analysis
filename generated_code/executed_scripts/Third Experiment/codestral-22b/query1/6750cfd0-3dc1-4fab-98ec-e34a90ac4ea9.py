import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store topics of interest
topics_of_interest = []

# Define the path to the liked posts JSON file
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

# Check if the liked posts JSON file exists
if os.path.exists(liked_posts_path):
    # Open the liked posts JSON file
    with open(liked_posts_path, 'r') as f:
        # Load the JSON data
        data = json.load(f)
        # Extract the titles of the liked posts and add them to the topics of interest list
        for post in data["likes_media_likes"]:
            topics_of_interest.append(post["title"])

# Define the path to the saved posts JSON file
saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")

# Check if the saved posts JSON file exists
if os.path.exists(saved_posts_path):
    # Open the saved posts JSON file
    with open(saved_posts_path, 'r') as f:
        # Load the JSON data
        data = json.load(f)
        # Extract the titles of the saved posts and add them to the topics of interest list
        for post in data["saved_saved_media"]:
            topics_of_interest.append(post["title"])

# Define the path to the results CSV file
results_path = "query_responses/results.csv"

# Write the topics of interest to the results CSV file
with open(results_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Topics of Interest"])
    for topic in topics_of_interest:
        writer.writerow([topic])