import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the data structures
post_likes = {}
story_likes = {}
comments = {}

# Process the JSON files
for filename in os.listdir(root_dir):
    if filename.endswith(".json"):
        with open(os.path.join(root_dir, filename), 'r') as file:
            data = eval(file.read())
            if 'likes' in data:
                for post in data['likes']['liked_posts.json']['structure']['likes_media_likes']:
                    post_id = post['title']
                    if post_id not in post_likes:
                        post_likes[post_id] = {'likes': 0, 'story_likes': 0, 'comments': 0}
                    post_likes[post_id]['likes'] += 1
            if 'saved' in data:
                for post in data['saved']['saved_posts.json']['structure']['saved_saved_media']:
                    post_id = post['title']
                    if post_id not in story_likes:
                        story_likes[post_id] = {'likes': 0, 'story_likes': 0, 'comments': 0}
                    story_likes[post_id]['story_likes'] += 1
                    if 'string_map_data' in post:
                        if 'Saved on' in post['string_map_data']:
                            comments[post_id] = comments.get(post_id, 0) + 1

# Find the top 20 accounts
top_accounts = sorted(post_likes.items(), key=lambda x: x[1]['likes'] + x[1]['story_likes'] + x[1].get('comments', 0), reverse=True)[:20]

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
    for account in top_accounts:
        writer.writerow([account[0], account[1].get('likes', 0), account[1].get('story_likes', 0), account[1].get('comments', 0)])