import os
import json
import csv
from collections import defaultdict

# Define the root directory
root_dir = "root_dir"

# Function to read JSON file and return its content
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to aggregate interactions from a JSON file
def aggregate_interactions(file_path, interaction_dict):
    if not os.path.exists(file_path):
        return
    
    data = read_json_file(file_path)
    
    if 'likes_media_likes' in data:
        for entry in data['likes_media_likes']:
            for item in entry.get('string_list_data', []):
                if 'value' in item:
                    interaction_dict[item['value']] += 1
    
    if 'story_activities_story_likes' in data:
        for entry in data['story_activities_story_likes']:
            for item in entry.get('string_list_data', []):
                if 'value' in item:
                    interaction_dict[item['value']] += 1
    
    if 'post_comments_1.json' in file_path:
        for entry in data:
            if 'string_map_data' in entry and 'Media Owner' in entry['string_map_data'] and 'value' in entry['string_map_data']['Media Owner']:
                interaction_dict[entry['string_map_data']['Media Owner']['value']] += 1

# Initialize a dictionary to store interaction counts
interaction_counts = defaultdict(int)

# Define paths to the relevant files
liked_posts_path = os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_posts.json')
story_likes_path = os.path.join(root_dir, 'your_instagram_activity', 'story_interactions', 'story_likes.json')
comments_path = os.path.join(root_dir, 'your_instagram_activity', 'comments', 'post_comments_1.json')

# Aggregate interactions from each file
aggregate_interactions(liked_posts_path, interaction_counts)
aggregate_interactions(story_likes_path, interaction_counts)
aggregate_interactions(comments_path, interaction_counts)

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

try:
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(csv_data)
except IOError:
    raise IOError(f"IOError: Failed to write to the file {output_path}.")