import os
import csv
from collections import defaultdict

# Define the root directory
root_dir = "root_dir"

# Initialize dictionaries to store interaction counts
post_likes_count = defaultdict(int)
story_likes_count = defaultdict(int)
comments_count = defaultdict(int)

# Function to read and parse JSON files
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            import json
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to count interactions from a JSON structure
def count_interactions(data, interaction_count):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                for item in value:
                    if 'string_list_data' in item:
                        for entry in item['string_list_data']:
                            if 'href' in entry:
                                account = entry['href'].split('/')[-1]
                                interaction_count[account] += 1
    elif isinstance(data, list):
        for item in data:
            if 'string_list_data' in item:
                for entry in item['string_list_data']:
                    if 'href' in entry:
                        account = entry['href'].split('/')[-1]
                        interaction_count[account] += 1

# Process liked_posts.json
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
if os.path.exists(liked_posts_path):
    liked_posts_data = read_json_file(liked_posts_path)
    count_interactions(liked_posts_data, post_likes_count)

# Process liked_comments.json
liked_comments_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_comments.json")
if os.path.exists(liked_comments_path):
    liked_comments_data = read_json_file(liked_comments_path)
    count_interactions(liked_comments_data, comments_count)

# Process story_likes.json
story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
if os.path.exists(story_likes_path):
    story_likes_data = read_json_file(story_likes_path)
    count_interactions(story_likes_data, story_likes_count)

# Aggregate interaction counts
interaction_totals = defaultdict(int)
for account in set(post_likes_count) | set(story_likes_count) | set(comments_count):
    interaction_totals[account] = post_likes_count[account] + story_likes_count[account] + comments_count[account]

# Sort accounts by total interactions in descending order
sorted_interactions = sorted(interaction_totals.items(), key=lambda x: x[1], reverse=True)[:20]

# Write the results to a CSV file
output_path = 'query_responses/results.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
    for account in sorted_interactions:
        post_likes = post_likes_count[account[0]]
        story_likes = story_likes_count[account[0]]
        comments = comments_count[account[0]]
        csvwriter.writerow([account[0], post_likes, story_likes, comments])

print(f"Results have been saved to {output_path}")