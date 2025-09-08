import csv
import os
import json

# Set the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize dictionaries to store the counts
post_likes = {}
story_likes = {}
comments = {}

# Process the liked posts JSON file
liked_posts_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
if os.path.exists(liked_posts_file):
    with open(liked_posts_file, 'r') as f:
        data = json.load(f)
        for entry in data["likes_media_likes"]:
            title = entry["title"]
            if title not in post_likes:
                post_likes[title] = 0
            post_likes[title] += 1
else:
    print("Warning: liked_posts.json file not found. Skipping post likes.")

# Process the story likes JSON file
story_likes_file = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
if os.path.exists(story_likes_file):
    with open(story_likes_file, 'r') as f:
        data = json.load(f)
        for entry in data["story_activities_story_likes"]:
            title = entry["title"]
            if title not in story_likes:
                story_likes[title] = 0
            story_likes[title] += 1
else:
    print("Warning: story_likes.json file not found. Skipping story likes.")

# Process the comments JSON file
comments_file = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")
if os.path.exists(comments_file):
    with open(comments_file, 'r') as f:
        data = json.load(f)
        for entry in data["comments_reels_comments"]:
            if "string_map_data" in entry and "Media Owner" in entry["string_map_data"]:
                media_owner = entry["string_map_data"]["Media Owner"]["value"]
                if media_owner not in comments:
                    comments[media_owner] = 0
                comments[media_owner] += 1
else:
    print("Warning: comments.json file not found. Skipping comments.")

# Create a list of tuples containing the user, post likes, story likes, and comments
data = []
for user in post_likes:
    data.append((user, post_likes.get(user, 0), story_likes.get(user, 0), comments.get(user, 0)))

# Sort the data by the sum of post likes, story likes, and comments in descending order
data.sort(key=lambda x: x[1] + x[2] + x[3], reverse=True)

# Write the data to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for row in data[:20]:
        writer.writerow(row)