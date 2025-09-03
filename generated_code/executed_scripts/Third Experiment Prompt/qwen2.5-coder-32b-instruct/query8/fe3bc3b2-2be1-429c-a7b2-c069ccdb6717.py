import os
import csv
from collections import defaultdict

# Define the root directory
root_dir = "root_dir"

# Initialize dictionaries to store interaction counts
post_likes_count = defaultdict(int)
story_likes_count = defaultdict(int)
comments_count = defaultdict(int)

# Function to read JSON files and extract interaction data
def read_json_file(file_path, key, interaction_count):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = eval(file.read())
            for item in data[key]:
                for entry in item['string_list_data']:
                    if 'value' in entry:
                        interaction_count[entry['value']] += 1
    except FileNotFoundError:
        print(f"FileNotFoundError: {file_path} does not exist. Skipping this file.")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Function to read JSON files and extract interaction data for posts
def read_posts_json_file(file_path, interaction_count):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = eval(file.read())
            for item in data:
                for entry in item['string_list_data']:
                    if 'value' in entry:
                        interaction_count[entry['value']] += 1
    except FileNotFoundError:
        print(f"FileNotFoundError: {file_path} does not exist. Skipping this file.")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Process post likes
post_likes_dir = os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_posts.json')
if os.path.exists(post_likes_dir):
    read_json_file(post_likes_dir, 'likes_media_likes', post_likes_count)
else:
    print(f"FileNotFoundError: {post_likes_dir} does not exist. Skipping post likes.")

# Process story likes
story_likes_dir = os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_comments.json')
if os.path.exists(story_likes_dir):
    read_json_file(story_likes_dir, 'likes_comment_likes', story_likes_count)
else:
    print(f"FileNotFoundError: {story_likes_dir} does not exist. Skipping story likes.")

# Process comments
comments_dir = os.path.join(root_dir, 'your_instagram_activity', 'comments', 'post_comments_1.json')
if os.path.exists(comments_dir):
    read_posts_json_file(comments_dir, comments_count)
else:
    print(f"FileNotFoundError: {comments_dir} does not exist. Skipping comments.")

# Combine interaction counts
combined_counts = defaultdict(int)
for account in set(post_likes_count) | set(story_likes_count) | set(comments_count):
    combined_counts[account] = post_likes_count[account] + story_likes_count[account] + comments_count[account]

# Sort by total interactions and get top 20
top_20_accounts = sorted(combined_counts.items(), key=lambda x: x[1], reverse=True)[:20]

# Prepare CSV output
output_path = 'query_responses/results.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
    for account in top_20_accounts:
        post_likes = post_likes_count[account[0]]
        story_likes = story_likes_count[account[0]]
        comments = comments_count[account[0]]
        csvwriter.writerow([account[0], post_likes, story_likes, comments])

print(f"Results saved to {output_path}")