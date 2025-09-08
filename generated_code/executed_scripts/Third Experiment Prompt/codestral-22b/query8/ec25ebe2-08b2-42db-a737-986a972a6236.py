import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the interaction counts
interactions = {}

# Define the paths to the JSON files
likes_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
saved_file = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")

# Process the likes file
if os.path.exists(likes_file):
    with open(likes_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data["likes_media_likes"]:
            for like in item["string_list_data"]:
                account = like["value"]
                if account in interactions:
                    interactions[account]["Post Likes"] += 1
                else:
                    interactions[account] = {"Post Likes": 1, "Story Likes": 0}

# Process the saved file
if os.path.exists(saved_file):
    with open(saved_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data["saved_saved_media"]:
            account = item["title"]
            if account in interactions:
                interactions[account]["Story Likes"] += 1
            else:
                interactions[account] = {"Post Likes": 0, "Story Likes": 1}

# Sort the interactions dictionary by the sum of post likes and story likes
sorted_interactions = sorted(interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Post Likes", "Story Likes"])
    for account, counts in sorted_interactions[:20]:
        writer.writerow([account, counts["Post Likes"], counts["Story Likes"]])