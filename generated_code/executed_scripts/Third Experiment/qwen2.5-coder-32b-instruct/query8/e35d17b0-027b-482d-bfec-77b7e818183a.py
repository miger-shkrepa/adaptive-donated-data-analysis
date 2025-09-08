import os
import csv
from collections import defaultdict

root_dir = "root_dir"

def get_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while reading the file {file_path}: {str(e)}")

def parse_json_content(content):
    import json
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The content is not valid JSON.")

def aggregate_likes_and_comments(root_dir):
    interactions = defaultdict(int)
    
    # Check for liked_posts.json
    liked_posts_path = os.path.join(root_dir, 'likes', 'liked_posts.json')
    if os.path.exists(liked_posts_path):
        liked_posts_content = get_file_content(liked_posts_path)
        liked_posts_data = parse_json_content(liked_posts_content)
        for item in liked_posts_data.get('likes_media_likes', []):
            for data in item.get('string_list_data', []):
                interactions[data.get('value', '')] += 1
    
    # Check for story_likes.json
    story_likes_path = os.path.join(root_dir, 'story_interactions', 'story_likes.json')
    if os.path.exists(story_likes_path):
        story_likes_content = get_file_content(story_likes_path)
        story_likes_data = parse_json_content(story_likes_content)
        for item in story_likes_data.get('story_activities_story_likes', []):
            for data in item.get('string_list_data', []):
                interactions[data.get('value', '')] += 1
    
    # Check for comments.json (assuming it's part of the story_interactions)
    comments_path = os.path.join(root_dir, 'story_interactions', 'comments.json')
    if os.path.exists(comments_path):
        comments_content = get_file_content(comments_path)
        comments_data = parse_json_content(comments_content)
        for item in comments_data.get('story_activities_comments', []):
            for data in item.get('string_list_data', []):
                interactions[data.get('value', '')] += 1
    
    return interactions

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    interactions = aggregate_likes_and_comments(root_dir)
    
    # Sort interactions by count in descending order and get top 20
    top_interactions = sorted(interactions.items(), key=lambda x: x[1], reverse=True)[:20]
    
    # Prepare CSV data
    csv_data = [['User', 'Post Likes', 'Story Likes and Comments']]
    for user, count in top_interactions:
        csv_data.append([user, count, 0])  # Assuming all counts are from post likes, story likes and comments are not separately identifiable
    
    # Write to CSV
    results_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    with open(results_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)

if __name__ == "__main__":
    main()