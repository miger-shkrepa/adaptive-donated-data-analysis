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

def process_data():
    user_interactions = defaultdict(int)
    try:
        # Process post likes
        post_likes_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        if os.path.exists(post_likes_file):
            post_likes_data = load_json_data(post_likes_file)
            for item in post_likes_data.get("likes_media_likes", []):
                for data in item.get("string_list_data", []):
                    user_interactions[data.get("value", "")] += 1
        else:
            print("Warning: Post likes data not found, treating its contribution as 0.")

        # Process story likes
        story_likes_file = os.path.join(root_dir, "story_interactions", "story_likes.json")
        if os.path.exists(story_likes_file):
            story_likes_data = load_json_data(story_likes_file)
            for item in story_likes_data.get("story_activities_story_likes", []):
                for data in item.get("string_list_data", []):
                    user_interactions[data.get("value", "")] += 1
        else:
            print("Warning: Story likes data not found, treating its contribution as 0.")

        # Process comments
        comments_file = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")
        if os.path.exists(comments_file):
            comments_data = load_json_data(comments_file)
            for item in comments_data.get("comments_reels_comments", []):
                media_owner = item.get("string_map_data", {}).get("Media Owner", {}).get("value", "")
                user_interactions[media_owner] += 1
        else:
            print("Warning: Comments data not found, treating its contribution as 0.")

    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

    return user_interactions

def write_to_csv(user_interactions):
    top_interactions = sorted(user_interactions.items(), key=lambda x: x[1], reverse=True)[:20]
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, count in top_interactions:
            writer.writerow({'User': user, 'Post Likes': 0, 'Story Likes': 0, 'Comments': count})

if not os.path.exists(root_dir):
    raise FileNotFoundError("Error: The root directory does not exist.")

try:
    interactions = process_data()
    write_to_csv(interactions)
except Exception as e:
    print(e)