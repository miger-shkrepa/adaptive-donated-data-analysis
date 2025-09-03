import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

results = []

# Liked posts
liked_posts_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
if os.path.exists(liked_posts_file):
    with open(liked_posts_file, "r") as f:
        liked_posts_data = json.load(f)
        for post in liked_posts_data["likes_media_likes"]:
            account = post["title"]
            post_views = 1
            video_views = 0
            results.append([account, post_views, video_views])

# Saved posts
saved_posts_file = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")
if os.path.exists(saved_posts_file):
    with open(saved_posts_file, "r") as f:
        saved_posts_data = json.load(f)
        for post in saved_posts_data["saved_saved_media"]:
            account = post["title"]
            post_views = 1
            video_views = 0
            results.append([account, post_views, video_views])

# Save results to CSV file
output_file = os.path.join("query_responses", "results.csv")
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Account", "Post Views", "Video Views"])
    writer.writerows(results)