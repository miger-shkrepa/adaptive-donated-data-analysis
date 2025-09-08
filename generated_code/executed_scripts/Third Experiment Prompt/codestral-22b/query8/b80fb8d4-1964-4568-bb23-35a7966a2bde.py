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
        for item in data["likes_media_likes"]:
            for interaction in item["string_list_data"]:
                user = interaction["value"]
                if user not in interactions:
                    interactions[user] = {"Post Likes": 1, "Story Likes": 0, "Comments": 0}
                else:
                    interactions[user]["Post Likes"] += 1

# Process story likes
story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
if os.path.exists(story_likes_path):
    with open(story_likes_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data["story_activities_story_likes"]:
            user = item["title"]
            if user not in interactions:
                interactions[user] = {"Post Likes": 0, "Story Likes": len(item["string_list_data"]), "Comments": 0}
            else:
                interactions[user]["Story Likes"] += len(item["string_list_data"])

# Process comments
comments_path = os.path.join(root_dir, "your_instagram_activity", "comments", "post_comments_1.json")
if os.path.exists(comments_path):
    with open(comments_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data:
            user = item["string_map_data"]["Media Owner"]["value"]
            if user not in interactions:
                interactions[user] = {"Post Likes": 0, "Story Likes": 0, "Comments": 1}
            else:
                interactions[user]["Comments"] += 1

# Sort by total interactions
sorted_interactions = sorted(interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)

# Write to CSV
with open("query_responses/results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for user, interaction in sorted_interactions[:20]:
        writer.writerow([user, interaction["Post Likes"], interaction["Story Likes"], interaction["Comments"]])