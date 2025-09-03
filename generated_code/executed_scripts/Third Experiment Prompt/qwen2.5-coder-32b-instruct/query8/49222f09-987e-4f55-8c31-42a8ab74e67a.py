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

# Function to count interactions from a JSON structure
def count_interactions(data, key):
    interaction_count = defaultdict(int)
    if isinstance(data, dict):
        for item in data.get(key, []):
            if isinstance(item, dict):
                for entry in item.get('string_list_data', []):
                    if 'value' in entry:
                        interaction_count[entry['value']] += 1
    return interaction_count

# Initialize interaction counters
post_likes_count = defaultdict(int)
story_likes_count = defaultdict(int)
comments_count = defaultdict(int)

# Process post likes
try:
    post_likes_file_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
    post_likes_data = read_json_file(post_likes_file_path)
    post_likes_count.update(count_interactions(post_likes_data, 'likes_media_likes'))
except (FileNotFoundError, ValueError):
    pass

# Process story likes
try:
    story_likes_file_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
    story_likes_data = read_json_file(story_likes_file_path)
    story_likes_count.update(count_interactions(story_likes_data, 'story_activities_story_likes'))
except (FileNotFoundError, ValueError):
    pass

# Process comments
try:
    comments_file_path = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")
    comments_data = read_json_file(comments_file_path)
    comments_count.update(count_interactions(comments_data, 'comments_reels_comments'))
except (FileNotFoundError, ValueError):
    pass

# Aggregate interaction counts
total_interactions = defaultdict(int)
for account in set(post_likes_count) | set(story_likes_count) | set(comments_count):
    total_interactions[account] = post_likes_count[account] + story_likes_count[account] + comments_count[account]

# Sort accounts by total interactions in descending order
sorted_interactions = sorted(total_interactions.items(), key=lambda x: x[1], reverse=True)[:20]

# Prepare CSV data
csv_data = [["User", "Post Likes", "Story Likes", "Comments"]]
for account in sorted_interactions:
    csv_data.append([
        account[0],
        str(post_likes_count[account[0]]),
        str(story_likes_count[account[0]]),
        str(comments_count[account[0]])
    ])

# Write CSV file
output_path = "query_responses/results.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(csv_data)

print(f"Results have been saved to {output_path}")