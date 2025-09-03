import os
import csv
import json
from collections import defaultdict

# Define the root directory
root_dir = "root_dir"

# Function to read JSON files and extract relevant data
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Error decoding JSON in file {file_path}: {str(e)}")
    except Exception as e:
        raise ValueError(f"ValueError: Error reading the file {file_path}: {str(e)}")

# Function to extract interactions from a JSON structure
def extract_interactions(data, key):
    interactions = defaultdict(int)
    if key in data:
        for item in data[key]:
            if 'string_list_data' in item:
                for entry in item['string_list_data']:
                    if 'value' in entry:
                        interactions[entry['value']] += 1
    return interactions

# Initialize dictionaries to store interactions
post_likes = defaultdict(int)
story_likes = defaultdict(int)
comments = defaultdict(int)

# Process post likes
try:
    post_likes_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
    if os.path.exists(post_likes_file):
        post_likes_data = read_json_file(post_likes_file)
        post_likes.update(extract_interactions(post_likes_data, "likes_media_likes"))
except Exception as e:
    print(f"Error processing post likes: {str(e)}")

# Process story likes
try:
    story_likes_file = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
    if os.path.exists(story_likes_file):
        story_likes_data = read_json_file(story_likes_file)
        story_likes.update(extract_interactions(story_likes_data, "story_activities_story_likes"))
except Exception as e:
    print(f"Error processing story likes: {str(e)}")

# Process comments
try:
    comments_file = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")
    if os.path.exists(comments_file):
        comments_data = read_json_file(comments_file)
        comments.update(extract_interactions(comments_data, "comments_reels_comments"))
except Exception as e:
    print(f"Error processing comments: {str(e)}")

# Combine interactions
combined_interactions = defaultdict(int)
for user in set(post_likes) | set(story_likes) | set(comments):
    combined_interactions[user] = post_likes[user] + story_likes[user] + comments[user]

# Sort interactions by frequency
sorted_interactions = sorted(combined_interactions.items(), key=lambda x: x[1], reverse=True)[:20]

# Write results to CSV
output_file = "query_responses/results.csv"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for user, total_interactions in sorted_interactions:
        csvwriter.writerow([user, post_likes[user], story_likes[user], comments[user]])

print(f"Results saved to {output_file}")