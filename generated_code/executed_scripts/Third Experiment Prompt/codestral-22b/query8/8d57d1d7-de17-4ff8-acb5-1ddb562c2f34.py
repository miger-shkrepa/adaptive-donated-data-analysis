import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the interaction counts
interactions = {}

# Define the paths to the relevant files
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
comments_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_comments.json")

# Process the liked posts file
if os.path.exists(liked_posts_path):
    with open(liked_posts_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data["likes_media_likes"]:
            for interaction in item["string_list_data"]:
                if "value" in interaction:
                    user = interaction["value"]
                    if user not in interactions:
                        interactions[user] = {"Post Likes": 1, "Story Likes": 0, "Comments": 0}
                    else:
                        interactions[user]["Post Likes"] += 1

# Process the story likes file
if os.path.exists(story_likes_path):
    with open(story_likes_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data["story_activities_story_likes"]:
            for interaction in item["string_list_data"]:
                if "value" in interaction:
                    user = interaction["value"]
                    if user not in interactions:
                        interactions[user] = {"Post Likes": 0, "Story Likes": 1, "Comments": 0}
                    else:
                        interactions[user]["Story Likes"] += 1

# Process the comments file
if os.path.exists(comments_path):
    with open(comments_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data["likes_comment_likes"]:
            for interaction in item["string_list_data"]:
                if "value" in interaction:
                    user = interaction["value"]
                    if user not in interactions:
                        interactions[user] = {"Post Likes": 0, "Story Likes": 0, "Comments": 1}
                    else:
                        interactions[user]["Comments"] += 1

# Sort the interactions dictionary by the sum of post likes, story likes, and comments
sorted_interactions = sorted(interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for user, counts in sorted_interactions[:20]:
        writer.writerow([user, counts["Post Likes"], counts["Story Likes"], counts["Comments"]])