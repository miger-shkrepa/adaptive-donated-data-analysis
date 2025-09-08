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
            for user in item.get("string_list_data", []):
                username = user.get("value", "")
                if username:
                    interactions[username] = interactions.get(username, {"Post Likes": 0, "Story Likes": 0, "Comments": 0})
                    interactions[username]["Post Likes"] += 1

# Process story likes
story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
if os.path.exists(story_likes_path):
    with open(story_likes_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data.get("story_activities_story_likes", []):
            for user in item.get("string_list_data", []):
                username = user.get("value", "")
                if username:
                    interactions[username] = interactions.get(username, {"Post Likes": 0, "Story Likes": 0, "Comments": 0})
                    interactions[username]["Story Likes"] += 1

# Process comments
comments_path = os.path.join(root_dir, "your_instagram_activity", "comments", "post_comments_1.json")
if os.path.exists(comments_path):
    with open(comments_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data:
            username = item.get("string_map_data", {}).get("Media Owner", {}).get("value", "")
            if username:
                interactions[username] = interactions.get(username, {"Post Likes": 0, "Story Likes": 0, "Comments": 0})
                interactions[username]["Comments"] += 1

# Sort by total interactions and get top 20
sorted_interactions = sorted(interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)[:20]

# Write to CSV
with open("query_responses/results.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for user, counts in sorted_interactions:
        writer.writerow([user, counts["Post Likes"], counts["Story Likes"], counts["Comments"]])