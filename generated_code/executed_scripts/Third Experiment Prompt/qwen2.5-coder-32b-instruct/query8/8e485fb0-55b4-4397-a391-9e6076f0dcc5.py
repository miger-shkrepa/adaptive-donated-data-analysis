import os
import csv
from collections import defaultdict

# Define the root directory
root_dir = "root_dir"

# Function to read JSON files and return their content
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            import json
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to count interactions from a JSON structure
def count_interactions(data, key):
    interaction_count = defaultdict(int)
    if isinstance(data, dict):
        for item in data.get(key, []):
            for entry in item.get('string_list_data', []):
                interaction_count[entry.get('value', '')] += 1
    return interaction_count

# Initialize interaction counters
post_likes_count = defaultdict(int)
story_likes_count = defaultdict(int)
comments_count = defaultdict(int)

# Path to the liked_posts.json file
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
if os.path.exists(liked_posts_path):
    liked_posts_data = read_json_file(liked_posts_path)
    post_likes_count.update(count_interactions(liked_posts_data, "likes_media_likes"))

# Path to the story_likes.json file
story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
if os.path.exists(story_likes_path):
    story_likes_data = read_json_file(story_likes_path)
    story_likes_count.update(count_interactions(story_likes_data, "story_activities_story_likes"))

# Path to the post_comments_1.json file
post_comments_path = os.path.join(root_dir, "your_instagram_activity", "comments", "post_comments_1.json")
if os.path.exists(post_comments_path):
    post_comments_data = read_json_file(post_comments_path)
    for item in post_comments_data:
        comments_count[item.get('string_map_data', {}).get('Media Owner', {}).get('value', '')] += 1

# Combine all interactions into a single dictionary
total_interactions = defaultdict(int)
for account in set(post_likes_count) | set(story_likes_count) | set(comments_count):
    total_interactions[account] = post_likes_count[account] + story_likes_count[account] + comments_count[account]

# Sort the accounts by total interactions in descending order
sorted_interactions = sorted(total_interactions.items(), key=lambda x: x[1], reverse=True)[:20]

# Prepare the CSV data
csv_data = [["User", "Post Likes", "Story Likes", "Comments"]]
for account in sorted_interactions:
    csv_data.append([
        account[0],
        str(post_likes_count[account[0]]),
        str(story_likes_count[account[0]]),
        str(comments_count[account[0]])
    ])

# Write the CSV file
output_path = "query_responses/results.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(csv_data)