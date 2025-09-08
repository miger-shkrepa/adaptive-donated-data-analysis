import os
import json
import csv
from collections import defaultdict

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def get_interactions_count(file_path, interaction_key):
    try:
        data = load_json(file_path)
        interactions = data.get(interaction_key, [])
        return len(interactions)
    except (FileNotFoundError, ValueError) as e:
        print(e)
        return 0

def get_comments_count(file_path):
    try:
        data = load_json(file_path)
        messages = data.get("messages", [])
        return sum(1 for message in messages if "content" in message)
    except (FileNotFoundError, ValueError) as e:
        print(e)
        return 0

def get_top_interactions(root_dir):
    interactions = defaultdict(int)
    try:
        for user_dir in os.listdir(os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")):
            user_path = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox", user_dir)
            if os.path.isdir(user_path):
                for json_file in os.listdir(user_path):
                    if json_file.endswith(".json"):
                        file_path = os.path.join(user_path, json_file)
                        interactions[user_dir] += get_comments_count(file_path)

        likes_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        interactions["liked_posts"] = get_interactions_count(likes_path, "likes_media_likes")

        story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        interactions["story_likes"] = get_interactions_count(story_likes_path, "story_activities_story_likes")

        top_interactions = sorted(interactions.items(), key=lambda x: x[1], reverse=True)[:20]
        return top_interactions
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

def write_to_csv(data, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, count in data:
            writer.writerow({'User': user, 'Post Likes': count if user == 'liked_posts' else 0,
                             'Story Likes': count if user == 'story_likes' else 0,
                             'Comments': count if user not in ['liked_posts', 'story_likes'] else 0})

try:
    top_interactions = get_top_interactions(root_dir)
    write_to_csv(top_interactions, 'query_responses/results.csv')
except Exception as e:
    print(e)
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()