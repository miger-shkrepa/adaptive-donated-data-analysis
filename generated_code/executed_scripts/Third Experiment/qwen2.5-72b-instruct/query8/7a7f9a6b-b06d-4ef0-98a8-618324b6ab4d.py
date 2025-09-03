import os
import json
import csv
from collections import defaultdict

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")

def process_likes(file_path, interaction_type):
    data = load_json_data(file_path)
    interactions = defaultdict(int)
    for item in data.get(interaction_type, []):
        for string_data in item.get('string_list_data', []):
            value = string_data.get('value')
            if value:
                interactions[value] += 1
    return interactions

def process_comments(file_path):
    data = load_json_data(file_path)
    interactions = defaultdict(int)
    for item in data.get('comments', []):
        for string_data in item.get('string_list_data', []):
            value = string_data.get('value')
            if value:
                interactions[value] += 1
    return interactions

def process_reels(file_path):
    data = load_json_data(file_path)
    interactions = defaultdict(int)
    for item in data.get('subscriptions_reels', []):
        username = item.get('string_map_data', {}).get('Benutzername', {}).get('value')
        if username:
            interactions[username] += 1
    return interactions

def aggregate_interactions():
    post_likes = {}
    story_likes = {}
    comments = {}
    reels = {}

    likes_dir = os.path.join(root_dir, 'likes')
    if os.path.exists(likes_dir):
        liked_posts_path = os.path.join(likes_dir, 'liked_posts.json')
        if os.path.exists(liked_posts_path):
            post_likes = process_likes(liked_posts_path, 'likes_media_likes')

        liked_comments_path = os.path.join(likes_dir, 'liked_comments.json')
        if os.path.exists(liked_comments_path):
            comments = process_likes(liked_comments_path, 'likes_comment_likes')

    story_activities_path = os.path.join(root_dir, 'story_activities_story_likes.json')
    if os.path.exists(story_activities_path):
        story_likes = process_likes(story_activities_path, 'story_activities_story_likes')

    subscriptions_dir = os.path.join(root_dir, 'subscriptions')
    if os.path.exists(subscriptions_dir):
        reels_path = os.path.join(subscriptions_dir, 'reels.json')
        if os.path.exists(reels_path):
            reels = process_reels(reels_path)

    all_interactions = defaultdict(int)
    for interaction_dict in [post_likes, story_likes, comments, reels]:
        for user, count in interaction_dict.items():
            all_interactions[user] += count

    top_interactions = sorted(all_interactions.items(), key=lambda x: x[1], reverse=True)[:20]

    return top_interactions

def write_to_csv(data):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, count in data:
            writer.writerow({'User': user, 'Post Likes': count, 'Story Likes': 0, 'Comments': 0})

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")
    top_interactions = aggregate_interactions()
    write_to_csv(top_interactions)
except Exception as e:
    print(f"An error occurred: {e}")