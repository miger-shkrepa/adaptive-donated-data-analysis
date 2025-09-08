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
def read_json_file(file_path, key):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = eval(file.read())
            for item in data[key]:
                for entry in item['string_list_data']:
                    if 'value' in entry:
                        account = entry['value']
                        if key == 'likes_media_likes':
                            post_likes_count[account] += 1
                        elif key == 'likes_comment_likes':
                            comments_count[account] += 1
                        elif key == 'story_activities_story_likes':
                            story_likes_count[account] += 1
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while reading the file {file_path}: {e}")

# Read liked_posts.json
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
if os.path.exists(liked_posts_path):
    read_json_file(liked_posts_path, 'likes_media_likes')

# Read liked_comments.json
liked_comments_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_comments.json")
if os.path.exists(liked_comments_path):
    read_json_file(liked_comments_path, 'likes_comment_likes')

# Read story_likes.json
story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
if os.path.exists(story_likes_path):
    read_json_file(story_likes_path, 'story_activities_story_likes')

# Aggregate the interaction counts
interaction_counts = defaultdict(int)
for account in post_likes_count:
    interaction_counts[account] += post_likes_count[account]
for account in story_likes_count:
    interaction_counts[account] += story_likes_count[account]
for account in comments_count:
    interaction_counts[account] += comments_count[account]

# Sort the accounts by total interactions in descending order
sorted_interactions = sorted(interaction_counts.items(), key=lambda x: x[1], reverse=True)

# Prepare the top 20 accounts
top_20_accounts = sorted_interactions[:20]

# Write the results to a CSV file
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

print(f"Results have been saved to {output_path}")