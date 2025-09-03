import os
import json
from collections import Counter
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a Counter to keep track of the interactions
interactions = Counter()

# Define the path to the liked posts JSON file
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

# Check if the liked posts JSON file exists
if os.path.exists(liked_posts_path):
    with open(liked_posts_path, 'r') as f:
        data = json.load(f)
        for post in data["likes_media_likes"]:
            for like in post["string_list_data"]:
                # Extract the account name from the href
                account = like["href"].split("/")[-2]
                interactions[account] += 1

# Define the path to the saved posts JSON file
saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")

# Check if the saved posts JSON file exists
if os.path.exists(saved_posts_path):
    with open(saved_posts_path, 'r') as f:
        data = json.load(f)
        for post in data["saved_saved_media"]:
            # Extract the account name from the title
            account = post["title"].split("'s")[0]
            interactions[account] += 1

# Get the top 20 accounts with the most interactions
top_accounts = interactions.most_common(20)

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for account, count in top_accounts:
        writer.writerow([account, count, 0, 0])