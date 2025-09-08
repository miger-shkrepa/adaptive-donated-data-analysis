import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

interactions = {}

# Process post likes
post_likes_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
if os.path.exists(post_likes_path):
    with open(post_likes_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data.get("likes_media_likes", []):
            for like in item.get("string_list_data", []):
                user = like.get("value", "")
                if user:
                    interactions[user] = interactions.get(user, {"Post Likes": 0, "Story Likes": 0, "Comments": 0})
                    interactions[user]["Post Likes"] += 1

# Process story likes
story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
if os.path.exists(story_likes_path):
    with open(story_likes_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data.get("story_activities_story_likes", []):
            for like in item.get("string_list_data", []):
                user = item.get("title", "")
                if user:
                    interactions[user] = interactions.get(user, {"Post Likes": 0, "Story Likes": 0, "Comments": 0})
                    interactions[user]["Story Likes"] += 1

# Process comments
comments_path = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")
if os.path.exists(comments_path):
    with open(comments_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data.get("comments_reels_comments", []):
            user = item.get("string_map_data", {}).get("Media Owner", {}).get("value", "")
            if user:
                interactions[user] = interactions.get(user, {"Post Likes": 0, "Story Likes": 0, "Comments": 0})
                interactions[user]["Comments"] += 1

# Sort and write to CSV
sorted_interactions = sorted(interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)[:20]
with open("query_responses/results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for user, counts in sorted_interactions:
        writer.writerow([user, counts["Post Likes"], counts["Story Likes"], counts["Comments"]])