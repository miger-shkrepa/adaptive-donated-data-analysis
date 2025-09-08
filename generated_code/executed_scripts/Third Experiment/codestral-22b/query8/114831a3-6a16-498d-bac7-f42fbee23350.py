import os
import json
import csv
from collections import defaultdict

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the interaction counts
interactions = defaultdict(lambda: {"Post Likes": 0, "Story Likes": 0, "Comments": 0})

# Define the paths to the relevant JSON files
likes_path = os.path.join(root_dir, "likes_and_views", "likes.json")
comments_path = os.path.join(root_dir, "comments", "comments.json")
story_likes_path = os.path.join(root_dir, "story_interactions", "story_likes.json")

# Process the likes.json file
if os.path.exists(likes_path):
    with open(likes_path, "r") as f:
        data = json.load(f)
        for item in data["likes_media_likes"]:
            user = item["string_map_data"]["Username"]["value"]
            interactions[user]["Post Likes"] += 1
else:
    print("Warning: The likes.json file does not exist. Post Likes will be treated as 0.")

# Process the comments.json file
if os.path.exists(comments_path):
    with open(comments_path, "r") as f:
        data = json.load(f)
        for item in data["comments_media_comments"]:
            user = item["string_map_data"]["Username"]["value"]
            interactions[user]["Comments"] += 1
else:
    print("Warning: The comments.json file does not exist. Comments will be treated as 0.")

# Process the story_likes.json file
if os.path.exists(story_likes_path):
    with open(story_likes_path, "r") as f:
        data = json.load(f)
        for item in data["story_activities_story_likes"]:
            user = item["title"]
            interactions[user]["Story Likes"] += len(item["string_list_data"])
else:
    print("Warning: The story_likes.json file does not exist. Story Likes will be treated as 0.")

# Sort the interactions dictionary by total interactions in descending order
sorted_interactions = sorted(interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for user, counts in sorted_interactions[:20]:
        writer.writerow([user, counts["Post Likes"], counts["Story Likes"], counts["Comments"]])