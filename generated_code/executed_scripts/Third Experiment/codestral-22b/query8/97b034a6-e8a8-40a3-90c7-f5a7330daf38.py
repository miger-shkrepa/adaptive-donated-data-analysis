import os
import json
import csv
from collections import defaultdict

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the interaction counts
interactions = defaultdict(lambda: {'Post Likes': 0, 'Story Likes': 0, 'Comments': 0})

# Function to process JSON files
def process_json(file_path, interaction_type):
    with open(file_path, 'r') as f:
        data = json.load(f)
    for item in data:
        if 'string_list_data' in item:
            for interaction in item['string_list_data']:
                if 'value' in interaction:
                    user = interaction['value']
                    interactions[user][interaction_type] += 1
        elif 'string_map_data' in item:
            for key, value in item['string_map_data'].items():
                if key == 'value':
                    user = value
                    interactions[user][interaction_type] += 1

# Process liked posts
liked_posts_path = os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_posts.json')
if os.path.exists(liked_posts_path):
    process_json(liked_posts_path, 'Post Likes')

# Process story likes
story_likes_path = os.path.join(root_dir, 'your_instagram_activity', 'story_interactions', 'story_likes.json')
if os.path.exists(story_likes_path):
    process_json(story_likes_path, 'Story Likes')

# Process liked comments
liked_comments_path = os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_comments.json')
if os.path.exists(liked_comments_path):
    process_json(liked_comments_path, 'Comments')

# Sort the interactions dictionary by total interactions
sorted_interactions = sorted(interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
    for user, counts in sorted_interactions[:20]:
        writer.writerow([user, counts['Post Likes'], counts['Story Likes'], counts['Comments']])