import os
import json
import csv

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")

def process_data():
    user_interactions = {}
    try:
        # Post Likes
        post_likes_path = os.path.join(root_dir, "post_likes.json")
        if os.path.exists(post_likes_path):
            post_likes_data = load_json_data(post_likes_path)
            for entry in post_likes_data.get("post_activities_post_likes", []):
                for string_data in entry.get("string_list_data", []):
                    username = string_data.get("value")
                    if username:
                        user_interactions[username] = user_interactions.get(username, 0) + 1

        # Story Likes
        story_likes_path = os.path.join(root_dir, "story_likes.json")
        if os.path.exists(story_likes_path):
            story_likes_data = load_json_data(story_likes_path)
            for entry in story_likes_data.get("story_activities_story_likes", []):
                for string_data in entry.get("string_list_data", []):
                    username = string_data.get("value")
                    if username:
                        user_interactions[username] = user_interactions.get(username, 0) + 1

        # Comments
        comments_path = os.path.join(root_dir, "comments.json")
        if os.path.exists(comments_path):
            comments_data = load_json_data(comments_path)
            for entry in comments_data.get("comments", []):
                for string_data in entry.get("string_list_data", []):
                    username = string_data.get("value")
                    if username:
                        user_interactions[username] = user_interactions.get(username, 0) + 1

        top_users = sorted(user_interactions.items(), key=lambda x: x[1], reverse=True)[:20]
        return top_users

    except FileNotFoundError as e:
        print(e)
        return []

def write_to_csv(data):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, count in data:
            writer.writerow({'User': user, 'Post Likes': count, 'Story Likes': count, 'Comments': count})

if not os.path.exists(root_dir):
    raise FileNotFoundError("Error: The root directory does not exist.")

top_users = process_data()
write_to_csv(top_users)