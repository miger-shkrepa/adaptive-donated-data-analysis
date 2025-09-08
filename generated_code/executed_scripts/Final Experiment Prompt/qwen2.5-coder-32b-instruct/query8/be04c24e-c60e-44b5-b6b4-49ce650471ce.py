import os
import json
import csv
from collections import defaultdict

# File input variable
root_dir = "root_dir"

# Function to load JSON data from a file
def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to count interactions from likes_media_likes
def count_post_likes(data):
    post_likes_count = defaultdict(int)
    for entry in data.get('likes_media_likes', []):
        for item in entry.get('string_list_data', []):
            post_likes_count[item['value']] += 1
    return post_likes_count

# Function to count interactions from story_activities_story_likes
def count_story_likes(data):
    story_likes_count = defaultdict(int)
    for entry in data.get('story_activities_story_likes', []):
        for item in entry.get('string_list_data', []):
            story_likes_count[entry['title']] += 1
    return story_likes_count

# Function to count interactions from comments_reels_comments
def count_comments(data):
    comments_count = defaultdict(int)
    for entry in data.get('comments_reels_comments', []):
        media_owner = entry['string_map_data'].get('Media Owner', {}).get('value', '')
        if media_owner:
            comments_count[media_owner] += 1
    return comments_count

# Main function to process the data and generate the CSV
def generate_csv(root_dir):
    # Define file paths
    post_likes_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
    story_likes_file = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
    comments_file = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")
    output_file = "query_responses/results.csv"

    # Initialize interaction counts
    post_likes_count = defaultdict(int)
    story_likes_count = defaultdict(int)
    comments_count = defaultdict(int)

    # Load and process post likes data
    if os.path.exists(post_likes_file):
        post_likes_data = load_json_file(post_likes_file)
        post_likes_count = count_post_likes(post_likes_data)
    else:
        print(f"Warning: The file {post_likes_file} does not exist. Skipping post likes.")

    # Load and process story likes data
    if os.path.exists(story_likes_file):
        story_likes_data = load_json_file(story_likes_file)
        story_likes_count = count_story_likes(story_likes_data)
    else:
        print(f"Warning: The file {story_likes_file} does not exist. Skipping story likes.")

    # Load and process comments data
    if os.path.exists(comments_file):
        comments_data = load_json_file(comments_file)
        comments_count = count_comments(comments_data)
    else:
        print(f"Warning: The file {comments_file} does not exist. Skipping comments.")

    # Aggregate all interactions
    all_interactions = defaultdict(lambda: {'Post Likes': 0, 'Story Likes': 0, 'Comments': 0})
    for user, count in post_likes_count.items():
        all_interactions[user]['Post Likes'] += count
    for user, count in story_likes_count.items():
        all_interactions[user]['Story Likes'] += count
    for user, count in comments_count.items():
        all_interactions[user]['Comments'] += count

    # Sort interactions by total count
    sorted_interactions = sorted(all_interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)

    # Write to CSV
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
            for user, counts in sorted_interactions[:20]:
                csvwriter.writerow([user, counts['Post Likes'], counts['Story Likes'], counts['Comments']])
    except Exception as e:
        raise Exception(f"Error: Failed to write to CSV file {output_file}. Reason: {str(e)}")

# Execute the main function
try:
    generate_csv(root_dir)
except Exception as e:
    print(e)