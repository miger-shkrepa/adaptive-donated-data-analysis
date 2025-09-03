import os
import csv
from collections import defaultdict
import json

# Define the root directory
root_dir = "root_dir"

# Function to read JSON files and extract data
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to extract interactions from JSON data
def extract_interactions(data, key):
    interactions = defaultdict(int)
    if key in data:
        for item in data[key]:
            if 'string_list_data' in item:
                for entry in item['string_list_data']:
                    if 'value' in entry:
                        interactions[entry['value']] += 1
            elif 'string_map_data' in item:
                for entry in item['string_map_data'].values():
                    if 'value' in entry:
                        interactions[entry['value']] += 1
    return interactions

# Initialize dictionaries to store interactions
post_likes = defaultdict(int)
story_likes = defaultdict(int)
comments = defaultdict(int)

# Process liked_posts.json
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
if os.path.exists(liked_posts_path):
    try:
        liked_posts_data = read_json_file(liked_posts_path)
        post_likes.update(extract_interactions(liked_posts_data, "likes_media_likes"))
    except (FileNotFoundError, ValueError) as e:
        print(e)

# Process story_likes.json
story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
if os.path.exists(story_likes_path):
    try:
        story_likes_data = read_json_file(story_likes_path)
        story_likes.update(extract_interactions(story_likes_data, "story_activities_story_likes"))
    except (FileNotFoundError, ValueError) as e:
        print(e)

# Process reels_comments.json
reels_comments_path = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")
if os.path.exists(reels_comments_path):
    try:
        reels_comments_data = read_json_file(reels_comments_path)
        comments.update(extract_interactions(reels_comments_data, "comments_reels_comments"))
    except (FileNotFoundError, ValueError) as e:
        print(e)

# Combine interactions
combined_interactions = defaultdict(int)
for account in set(post_likes) | set(story_likes) | set(comments):
    combined_interactions[account] = post_likes[account] + story_likes[account] + comments[account]

# Sort interactions by count in descending order
sorted_interactions = sorted(combined_interactions.items(), key=lambda x: x[1], reverse=True)[:20]

# Prepare CSV data
csv_data = [["User", "Post Likes", "Story Likes", "Comments"]]
for account, total_interactions in sorted_interactions:
    user = account
    post_likes_count = post_likes[user]
    story_likes_count = story_likes[user]
    comments_count = comments[user]
    csv_data.append([user, post_likes_count, story_likes_count, comments_count])

# Write CSV file
output_path = "query_responses/results.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(csv_data)

print(f"Results have been saved to {output_path}")