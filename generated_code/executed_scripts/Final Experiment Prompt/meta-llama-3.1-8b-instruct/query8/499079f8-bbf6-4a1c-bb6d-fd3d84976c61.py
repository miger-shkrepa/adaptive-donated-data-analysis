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
            media_owner = entry["string_map_data"]["Media Owner"]["value"]
            if media_owner not in comments:
                comments[media_owner] = 0
            comments[media_owner] += 1
else:
    print("Warning: comments.json file not found. Skipping comments.")

# Create a list of tuples with the counts
counts = []
for title in post_likes:
    counts.append((title, post_likes[title], story_likes.get(title, 0), comments.get(title, 0)))
for title in story_likes:
    if title not in post_likes:
        counts.append((title, 0, story_likes[title], comments.get(title, 0)))
for media_owner in comments:
    if media_owner not in post_likes and media_owner not in story_likes:
        counts.append((media_owner, 0, 0, comments[media_owner]))

# Sort the counts in descending order
counts.sort(key=lambda x: (x[1] + x[2] + x[3]), reverse=True)

# Write the counts to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for count in counts[:20]:
        writer.writerow(count)