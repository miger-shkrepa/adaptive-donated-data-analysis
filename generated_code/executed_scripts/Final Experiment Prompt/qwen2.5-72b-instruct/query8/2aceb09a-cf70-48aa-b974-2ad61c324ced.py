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
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def process_data():
    post_likes = defaultdict(int)
    story_likes = defaultdict(int)
    comments = defaultdict(int)

    try:
        liked_posts_data = load_json_data(f"{root_dir}/your_instagram_activity/likes/liked_posts.json")
        for entry in liked_posts_data.get("likes_media_likes", []):
            title = entry.get("title")
            if title:
                post_likes[title] += 1
    except FileNotFoundError:
        print("Warning: liked_posts.json not found. Post likes will be set to 0.")

    try:
        story_likes_data = load_json_data(f"{root_dir}/your_instagram_activity/story_interactions/story_likes.json")
        for entry in story_likes_data.get("story_activities_story_likes", []):
            title = entry.get("title")
            if title:
                story_likes[title] += 1
    except FileNotFoundError:
        print("Warning: story_likes.json not found. Story likes will be set to 0.")

    try:
        reels_comments_data = load_json_data(f"{root_dir}/your_instagram_activity/comments/reels_comments.json")
        for entry in reels_comments_data.get("comments_reels_comments", []):
            media_owner = entry.get("string_map_data", {}).get("Media Owner", {}).get("value")
            if media_owner:
                comments[media_owner] += 1
    except FileNotFoundError:
        print("Warning: reels_comments.json not found. Comments will be set to 0.")

    interaction_counts = defaultdict(int)
    for account, count in post_likes.items():
        interaction_counts[account] += count
    for account, count in story_likes.items():
        interaction_counts[account] += count
    for account, count in comments.items():
        interaction_counts[account] += count

    top_accounts = sorted(interaction_counts.items(), key=lambda x: x[1], reverse=True)[:20]

    return top_accounts, post_likes, story_likes, comments

def save_to_csv(data, post_likes, story_likes, comments):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        if not data:
            return

        for user, _ in data:
            post_likes_count = post_likes.get(user, 0)
            story_likes_count = story_likes.get(user, 0)
            comments_count = comments.get(user, 0)
            writer.writerow({
                'User': user,
                'Post Likes': post_likes_count,
                'Story Likes': story_likes_count,
                'Comments': comments_count
            })

if __name__ == "__main__":
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    try:
        top_accounts, post_likes, story_likes, comments = process_data()
        save_to_csv(top_accounts, post_likes, story_likes, comments)
    except Exception as e:
        print(f"Error: {e}")