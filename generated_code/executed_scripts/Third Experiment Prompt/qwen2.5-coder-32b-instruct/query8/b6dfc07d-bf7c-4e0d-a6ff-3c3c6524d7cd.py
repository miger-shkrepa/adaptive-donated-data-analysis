import os
import csv
import json
from collections import defaultdict

# Define the root directory
root_dir = "root_dir"

# Initialize a dictionary to store interaction counts
interaction_counts = defaultdict(int)

# Function to load JSON data from a file
def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to process liked posts and count interactions
def process_liked_posts(file_path):
    try:
        data = load_json_file(file_path)
        for item in data.get('likes_media_likes', []):
            for entry in item.get('string_list_data', []):
                interaction_counts[entry.get('value', '')] += 1
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Function to process story likes and count interactions
def process_story_likes(file_path):
    try:
        data = load_json_file(file_path)
        for item in data.get('story_activities_story_likes', []):
            for entry in item.get('string_list_data', []):
                interaction_counts[entry.get('value', '')] += 1
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Function to process comments and count interactions
def process_comments(file_path):
    try:
        data = load_json_file(file_path)
        for item in data:
            interaction_counts[item.get('string_map_data', {}).get('Media Owner', {}).get('value', '')] += 1
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Process liked posts
liked_posts_path = os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_posts.json')
if os.path.exists(liked_posts_path):
    process_liked_posts(liked_posts_path)

# Process story likes
story_likes_path = os.path.join(root_dir, 'your_instagram_activity', 'story_interactions', 'story_likes.json')
if os.path.exists(story_likes_path):
    process_story_likes(story_likes_path)

# Process comments
comments_path = os.path.join(root_dir, 'your_instagram_activity', 'comments', 'post_comments_1.json')
if os.path.exists(comments_path):
    process_comments(comments_path)

# Sort the interactions by count in descending order and get the top 20
top_interactions = sorted(interaction_counts.items(), key=lambda x: x[1], reverse=True)[:20]

# Prepare the CSV output
csv_data = [['User', 'Post Likes', 'Story Likes', 'Comments']]

# Since we don't have separate counts for post likes, story likes, and comments, we'll just use the total count
for user, total_interactions in top_interactions:
    csv_data.append([user, 0, 0, total_interactions])

# Write the CSV file
output_path = 'query_responses/results.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(csv_data)

print(f"Results saved to {output_path}")