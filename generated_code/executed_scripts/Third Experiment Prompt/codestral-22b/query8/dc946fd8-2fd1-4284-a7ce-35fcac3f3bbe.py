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
    with open(post_likes_path, "r") as f:
        data = json.load(f)
        if "likes_media_likes" in data:
            for item in data["likes_media_likes"]:
                if "string_list_data" in item:
                    for interaction in item["string_list_data"]:
                        if "value" in interaction:
                            try:
                                username = interaction["value"].split("/")[-2]
                                if username:
                                    if username not in interactions:
                                        interactions[username] = {"Post Likes": 1, "Story Likes": 0, "Comments": 0}
                                    else:
                                        interactions[username]["Post Likes"] += 1
                            except IndexError:
                                pass

# Process story likes
story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
if os.path.exists(story_likes_path):
    with open(story_likes_path, "r") as f:
        data = json.load(f)
        if "story_activities_story_likes" in data:
            for item in data["story_activities_story_likes"]:
                if "title" in item:
                    try:
                        username = item["title"].split("/")[-2]
                        if username:
                            if username not in interactions:
                                interactions[username] = {"Post Likes": 0, "Story Likes": len(item.get("string_list_data", [])), "Comments": 0}
                            else:
                                interactions[username]["Story Likes"] += len(item.get("string_list_data", []))
                    except IndexError:
                        pass

# Process comments
comments_path = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")
if os.path.exists(comments_path):
    with open(comments_path, "r") as f:
        data = json.load(f)
        if "comments_reels_comments" in data:
            for item in data["comments_reels_comments"]:
                if "string_map_data" in item and "Media Owner" in item["string_map_data"] and "value" in item["string_map_data"]["Media Owner"]:
                    try:
                        username = item["string_map_data"]["Media Owner"]["value"].split("/")[-2]
                        if username:
                            if username not in interactions:
                                interactions[username] = {"Post Likes": 0, "Story Likes": 0, "Comments": 1}
                            else:
                                interactions[username]["Comments"] += 1
                    except IndexError:
                        pass

# Sort and write to CSV
sorted_interactions = sorted(interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)[:20]
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for username, counts in sorted_interactions:
        writer.writerow([username, counts.get("Post Likes", 0), counts.get("Story Likes", 0), counts.get("Comments", 0)])