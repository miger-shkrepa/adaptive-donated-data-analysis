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
        raise FileNotFoundError("FileNotFoundError: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON data.")

def process_data():
    user_interactions = defaultdict(int)
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        likes_dir = os.path.join(root_dir, "your_instagram_activity", "likes")
        media_dir = os.path.join(root_dir, "your_instagram_activity", "media")
        comments_dir = os.path.join(root_dir, "your_instagram_activity", "comments")

        if os.path.exists(likes_dir):
            liked_posts_file = os.path.join(likes_dir, "liked_posts.json")
            if os.path.exists(liked_posts_file):
                liked_posts_data = load_json_data(liked_posts_file)
                for item in liked_posts_data["likes_media_likes"]:
                    for data in item["string_list_data"]:
                        user_interactions[data["value"]] += 1

            liked_comments_file = os.path.join(likes_dir, "liked_comments.json")
            if os.path.exists(liked_comments_file):
                liked_comments_data = load_json_data(liked_comments_file)
                for item in liked_comments_data["likes_comment_likes"]:
                    for data in item["string_list_data"]:
                        user_interactions[data["value"]] += 1

        if os.path.exists(media_dir):
            stories_file = os.path.join(media_dir, "stories.json")
            if os.path.exists(stories_file):
                stories_data = load_json_data(stories_file)
                for item in stories_data["ig_stories"]:
                    user_interactions[item["title"]] += 1

        if os.path.exists(comments_dir):
            for subdir in os.listdir(comments_dir):
                subdir_path = os.path.join(comments_dir, subdir)
                if os.path.isdir(subdir_path):
                    for json_file in os.listdir(subdir_path):
                        if json_file.endswith(".json"):
                            file_path = os.path.join(subdir_path, json_file)
                            comments_data = load_json_data(file_path)
                            for message in comments_data["messages"]:
                                user_interactions[message["sender_name"]] += 1

        top_interactions = sorted(user_interactions.items(), key=lambda x: x[1], reverse=True)[:20]

        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user, count in top_interactions:
                writer.writerow({'User': user, 'Post Likes': 0, 'Story Likes': 0, 'Comments': count})

    except Exception as e:
        print(f"Error: {str(e)}")

process_data()