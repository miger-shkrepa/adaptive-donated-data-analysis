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

# Function to update the interaction counts
def update_interactions(username, post_likes=0, story_likes=0, comments=0):
    if username not in interactions:
        interactions[username] = {"Post Likes": 0, "Story Likes": 0, "Comments": 0}
    interactions[username]["Post Likes"] += post_likes
    interactions[username]["Story Likes"] += story_likes
    interactions[username]["Comments"] += comments

# Process the liked posts
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
if os.path.exists(liked_posts_path):
    with open(liked_posts_path, "r") as f:
        liked_posts = json.load(f)
    for post in liked_posts["likes_media_likes"]:
        try:
            for item in post["string_list_data"]:
                username = item["value"].split("/")[-2]
                update_interactions(username, post_likes=1)
        except IndexError:
            continue

# Process the story likes
story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
if os.path.exists(story_likes_path):
    with open(story_likes_path, "r") as f:
        story_likes = json.load(f)
    for story in story_likes["story_activities_story_likes"]:
        try:
            username = story["title"].split("/")[-2]
            story_likes_count = len(story["string_list_data"])
            update_interactions(username, story_likes=story_likes_count)
        except IndexError:
            continue

# Process the comments
comments_path = os.path.join(root_dir, "your_instagram_activity", "comments", "post_comments_1.json")
if os.path.exists(comments_path):
    with open(comments_path, "r") as f:
        comments = json.load(f)
    for comment in comments:
        try:
            username = comment["string_map_data"]["Media Owner"]["value"]
            update_interactions(username, comments=1)
        except IndexError:
            continue

# Sort the interactions by total count and get the top 20
sorted_interactions = sorted(interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)[:20]

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for username, counts in sorted_interactions:
        writer.writerow([username, counts["Post Likes"], counts["Story Likes"], counts["Comments"]])