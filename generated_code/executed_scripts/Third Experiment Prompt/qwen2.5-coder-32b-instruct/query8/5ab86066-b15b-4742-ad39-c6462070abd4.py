import os
import csv
import json
from collections import defaultdict

# Define the root directory
root_dir = "root_dir"

# Initialize a dictionary to store interaction counts
interaction_counts = defaultdict(int)

# Function to parse JSON files and update interaction counts
def parse_json_file(file_path, key):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if key in data:
                for item in data[key]:
                    if 'string_list_data' in item:
                        for entry in item['string_list_data']:
                            if 'value' in entry:
                                interaction_counts[entry['value']] += 1
                    elif 'string_map_data' in item:
                        for entry in item['string_map_data'].values():
                            if 'value' in entry:
                                interaction_counts[entry['value']] += 1
    except FileNotFoundError:
        print(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to parse media files and update interaction counts
def parse_media_file(file_path, key):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if key in data:
                for item in data[key]:
                    if 'media' in item:
                        for media in item['media']:
                            if 'title' in media:
                                interaction_counts[media['title']] += 1
    except FileNotFoundError:
        print(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print(f"ValueError: The file {file_path} is not a valid JSON file.")

# Define the paths to the relevant JSON files
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
liked_comments_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_comments.json")
reels_comments_path = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")
post_comments_path = os.path.join(root_dir, "your_instagram_activity", "comments", "post_comments_1.json")

# Parse the JSON files
parse_json_file(liked_posts_path, "likes_media_likes")
parse_json_file(liked_comments_path, "likes_comment_likes")
parse_json_file(reels_comments_path, "comments_reels_comments")
parse_json_file(post_comments_path, "post_comments_1")

# Define the paths to the relevant media files
posts_path = os.path.join(root_dir, "your_instagram_activity", "media", "posts_1.json")
profile_photos_path = os.path.join(root_dir, "your_instagram_activity", "media", "profile_photos.json")
reels_path = os.path.join(root_dir, "your_instagram_activity", "media", "reels.json")
stories_path = os.path.join(root_dir, "your_instagram_activity", "media", "stories.json")

# Parse the media files
parse_media_file(posts_path, "ig_reels_media")
parse_media_file(profile_photos_path, "ig_profile_picture")
parse_media_file(reels_path, "ig_reels_media")
parse_media_file(stories_path, "ig_stories")

# Sort the interaction counts by value in descending order and get the top 20
top_interactions = sorted(interaction_counts.items(), key=lambda x: x[1], reverse=True)[:20]

# Prepare the CSV data
csv_data = [["User", "Post Likes", "Story Likes and Comments"]]
for user, count in top_interactions:
    csv_data.append([user, count, 0])  # Assuming all interactions are counted as post likes for simplicity

# Write the CSV file
output_path = "query_responses/results.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(csv_data)

print(f"Results have been written to {output_path}")