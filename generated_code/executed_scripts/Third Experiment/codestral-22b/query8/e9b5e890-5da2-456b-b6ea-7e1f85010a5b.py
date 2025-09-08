import os
import json
import csv
from collections import Counter

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a counter for user interactions
user_interactions = Counter()

# Define the paths to the relevant files
liked_posts_path = os.path.join(root_dir, "likes", "liked_posts.json")
liked_comments_path = os.path.join(root_dir, "likes", "liked_comments.json")
story_activities_path = os.path.join(root_dir, "story_activities", "story_likes")

# Process the liked posts file
if os.path.exists(liked_posts_path):
    with open(liked_posts_path, "r") as f:
        data = json.load(f)
        for post in data["likes_media_likes"]:
            for interaction in post["string_list_data"]:
                user_interactions[interaction["value"]] += 1

# Process the liked comments file
if os.path.exists(liked_comments_path):
    with open(liked_comments_path, "r") as f:
        data = json.load(f)
        for comment in data["likes_comment_likes"]:
            for interaction in comment["string_list_data"]:
                user_interactions[interaction["value"]] += 1

# Process the story activities files
if os.path.exists(story_activities_path):
    for filename in os.listdir(story_activities_path):
        if filename.endswith(".json"):
            with open(os.path.join(story_activities_path, filename), "r") as f:
                data = json.load(f)
                for story in data["story_activities_story_likes"]:
                    for interaction in story["string_list_data"]:
                        user_interactions[story["title"]] += 1

# Get the top 20 users
top_users = user_interactions.most_common(20)

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Interactions"])
    for user, interactions in top_users:
        writer.writerow([user, interactions])