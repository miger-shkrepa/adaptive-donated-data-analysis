import os
import json
import csv
from collections import defaultdict

# Define the root directory
root_dir = "root_dir"

# Initialize dictionaries to store interaction counts
post_likes = defaultdict(int)
story_likes = defaultdict(int)
comments = defaultdict(int)

# Helper function to process JSON files
def process_json_file(file_path, interaction_type):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                for entry in item.get('string_list_data', []):
                    interaction_type[entry.get('value', '')] += 1
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Process post likes
post_likes_path = os.path.join(root_dir, 'likes', 'liked_posts.json')
if os.path.exists(post_likes_path):
    process_json_file(post_likes_path, post_likes)

# Process story likes
story_likes_path = os.path.join(root_dir, 'story_activities_story_likes.json')
if os.path.exists(story_likes_path):
    process_json_file(story_likes_path, story_likes)

# Process comments
comments_path = os.path.join(root_dir, 'likes', 'liked_comments.json')
if os.path.exists(comments_path):
    process_json_file(comments_path, comments)

# Combine interaction counts
total_interactions = defaultdict(int)
for user in post_likes:
    total_interactions[user] += post_likes[user]
for user in story_likes:
    total_interactions[user] += story_likes[user]
for user in comments:
    total_interactions[user] += comments[user]

# Get top 20 accounts
top_20_accounts = sorted(total_interactions.items(), key=lambda x: x[1], reverse=True)[:20]

# Prepare CSV data
csv_data = [["User", "Post Likes", "Story Likes", "Comments"]]
for user, _ in top_20_accounts:
    csv_data.append([
        user,
        post_likes.get(user, 0),
        story_likes.get(user, 0),
        comments.get(user, 0)
    ])

# Write to CSV file
output_path = 'query_responses/results.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
try:
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)
except Exception as e:
    raise IOError(f"IOError: Failed to write to {output_path}. {str(e)}")