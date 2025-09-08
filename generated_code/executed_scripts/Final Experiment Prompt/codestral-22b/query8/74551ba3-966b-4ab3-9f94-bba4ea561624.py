import json
import csv
import os

# Declare the root directory
root_dir = "root_dir"

# Initialize a dictionary to store the interaction counts
interactions = {}

# Define the paths to the JSON files
liked_posts_path = os.path.join(root_dir, "your_instagram_activity/likes/liked_posts.json")
story_likes_path = os.path.join(root_dir, "your_instagram_activity/story_interactions/story_likes.json")
reels_comments_path = os.path.join(root_dir, "your_instagram_activity/comments/reels_comments.json")

# Process the liked posts file
try:
    with open(liked_posts_path, 'r') as f:
        data = json.load(f)
        for item in data["likes_media_likes"]:
            account = item["title"]
            if account not in interactions:
                interactions[account] = {"Post Likes": 1, "Story Likes": 0, "Comments": 0}
            else:
                interactions[account]["Post Likes"] += 1
except FileNotFoundError:
    print("Error: The liked posts file does not exist.")

# Process the story likes file
try:
    with open(story_likes_path, 'r') as f:
        data = json.load(f)
        for item in data["story_activities_story_likes"]:
            account = item["title"]
            if account not in interactions:
                interactions[account] = {"Post Likes": 0, "Story Likes": 1, "Comments": 0}
            else:
                interactions[account]["Story Likes"] += 1
except FileNotFoundError:
    print("Error: The story likes file does not exist.")

# Process the reels comments file
try:
    with open(reels_comments_path, 'r') as f:
        data = json.load(f)
        for item in data["comments_reels_comments"]:
            if "Media Owner" in item["string_map_data"]:
                account = item["string_map_data"]["Media Owner"]["value"]
                if account not in interactions:
                    interactions[account] = {"Post Likes": 0, "Story Likes": 0, "Comments": 1}
                else:
                    interactions[account]["Comments"] += 1
except FileNotFoundError:
    print("Error: The reels comments file does not exist.")

# Write the results to a CSV file
with open("query_responses/results.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for account, counts in sorted(interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)[:20]:
        writer.writerow([account, counts["Post Likes"], counts["Story Likes"], counts["Comments"]])